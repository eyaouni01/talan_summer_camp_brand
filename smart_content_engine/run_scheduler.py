# ============================================================================
# 🚀 run_scheduler.py - Lanceur simple du scheduler
# ============================================================================
import asyncio
import os
from scheduler import ContentScheduler, schedule_from_reviewed_content

def main():
    """Interface principale du scheduler"""
    print("📅 Smart Content Scheduler")
    print("=" * 30)
    
    scheduler = ContentScheduler()
    
    while True:
        print("\n📋 Options disponibles:")
        print("1. 📅 Programmer un nouveau post")
        print("2. 📊 Voir les posts programmés")
        print("3. 🚀 Démarrer le scheduler")
        print("4. ⏹️ Arrêter le scheduler")
        print("5. ❌ Annuler un post")
        print("6. 🚪 Quitter")
        
        choice = input("\nVotre choix (1-6): ").strip()
        
        if choice == "1":
            print("\n" + "="*50)
            schedule_from_reviewed_content()
            
        elif choice == "2":
            posts = scheduler.list_scheduled_posts()
            if posts:
                print(f"\n📅 {len(posts)} posts programmés:")
                print("-" * 60)
                for post in posts:
                    schedule_dt = post["schedule_datetime"].replace('T', ' ')
                    platforms = ", ".join([p for p, enabled in post["platforms"].items() if enabled])
                    status_emoji = {"scheduled": "⏰", "published": "✅", "failed": "❌", "cancelled": "🚫"}
                    
                    print(f"{status_emoji.get(post['status'], '❓')} {post['id']}")
                    print(f"   📅 {schedule_dt}")
                    print(f"   🌐 {platforms}")
                    print(f"   📝 {post['preview']}")
                    print(f"   📊 {post['status']}")
                    print()
            else:
                print("\n📭 Aucun post programmé")
        
        elif choice == "3":
            if not scheduler.is_running:
                scheduler.start_scheduler()
                print("✅ Scheduler démarré!")
            else:
                print("⚠️ Scheduler déjà actif")
        
        elif choice == "4":
            if scheduler.is_running:
                scheduler.stop_scheduler()
                print("✅ Scheduler arrêté")
            else:
                print("⚠️ Scheduler pas actif")
        
        elif choice == "5":
            posts = scheduler.list_scheduled_posts()
            scheduled_posts = [p for p in posts if p["status"] == "scheduled"]
            
            if scheduled_posts:
                print("\n📅 Posts programmés à annuler:")
                for i, post in enumerate(scheduled_posts, 1):
                    schedule_dt = post["schedule_datetime"].replace('T', ' ')
                    print(f"{i}. {post['id']} - {schedule_dt}")
                
                try:
                    cancel_choice = int(input(f"\nChoisir le post à annuler (1-{len(scheduled_posts)}): "))
                    if 1 <= cancel_choice <= len(scheduled_posts):
                        post_id = scheduled_posts[cancel_choice-1]["id"]
                        if scheduler.cancel_scheduled_post(post_id):
                            print("✅ Post annulé avec succès")
                        else:
                            print("❌ Erreur lors de l'annulation")
                    else:
                        print("❌ Choix invalide")
                except ValueError:
                    print("❌ Veuillez entrer un nombre")
            else:
                print("\n📭 Aucun post programmé à annuler")
        
        elif choice == "6":
            if scheduler.is_running:
                scheduler.stop_scheduler()
            print("👋 Au revoir!")
            break
        
        else:
            print("❌ Choix invalide")

if __name__ == "__main__":
    main()