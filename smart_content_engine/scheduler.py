# ============================================================================
# 📅 scheduler.py - Version corrigée avec support des images
# ============================================================================
import os
import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import schedule
import time
from threading import Thread

from agents.posting_agent import PostingAgent
from linkedin_auth import LinkedInAuth
from facebook_auth import FacebookAuth

class ContentScheduler:
    """
    Gestionnaire de publication programmée pour LinkedIn et Facebook
    Version corrigée avec support des images
    """
    
    def __init__(self):
        self.posting_agent = PostingAgent()
        self.linkedin_auth = LinkedInAuth()
        self.facebook_auth = FacebookAuth()
        self.scheduled_posts = []
        self.is_running = False
        
        # Créer le dossier pour les posts programmés
        os.makedirs("data/scheduled_posts", exist_ok=True)
        
        # Charger les posts programmés existants
        self.load_scheduled_posts()
    
    def schedule_post(self, content_file_path: str, schedule_datetime: datetime, platforms: Dict[str, bool]) -> str:
        """
        Programme un post pour une date/heure spécifique
        
        Args:
            content_file_path: Chemin vers le fichier JSON du contenu
            schedule_datetime: Date et heure de publication
            platforms: {"linkedin": bool, "facebook": bool}
        
        Returns:
            ID du post programmé
        """
        # Charger le contenu depuis le fichier
        with open(content_file_path, 'r', encoding='utf-8') as f:
            content_data = json.load(f)
        
        # Générer un ID unique
        post_id = f"scheduled_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # ✅ CORRECTION 1: Inclure le chemin de l'image dans les données programmées
        scheduled_post = {
            "id": post_id,
            "content": content_data["content"],
            "preferences": content_data["preferences"],
            "image_path": content_data.get("image_path"),  # 🔧 Ajout du chemin de l'image
            "schedule_datetime": schedule_datetime.isoformat(),
            "platforms": platforms,
            "status": "scheduled",
            "created_at": datetime.now().isoformat(),
            "attempts": 0,
            "max_attempts": 3
        }
        
        # Vérifier que l'image existe si spécifiée
        if scheduled_post["image_path"]:
            if os.path.exists(scheduled_post["image_path"]):
                print(f"🖼️ Image trouvée: {scheduled_post['image_path']}")
            else:
                print(f"⚠️ Attention: Image non trouvée à {scheduled_post['image_path']}")
                scheduled_post["image_path"] = None
        
        # Sauvegarder le post programmé
        self._save_scheduled_post(scheduled_post)
        self.scheduled_posts.append(scheduled_post)
        
        print(f"✅ Post programmé pour {schedule_datetime.strftime('%d/%m/%Y à %H:%M')}")
        print(f"📋 ID: {post_id}")
        print(f"🌐 Plateformes: {', '.join([p for p, enabled in platforms.items() if enabled])}")
        
        return post_id
    
    def _save_scheduled_post(self, scheduled_post: Dict):
        """Sauvegarde un post programmé sur disque"""
        filename = f"data/scheduled_posts/{scheduled_post['id']}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(scheduled_post, f, ensure_ascii=False, indent=2)
    
    async def _publish_scheduled_post(self, post: Dict):
        """Publie un post programmé - VERSION CORRIGÉE avec images"""
        print(f"📤 Publication du post programmé: {post['id']}")
        
        try:
            content_text = post["content"]
            preferences = post["preferences"]
            platforms = post["platforms"]
            image_path = post.get("image_path")  # 🔧 Récupération du chemin de l'image
            
            # ✅ CORRECTION 2: Vérifier à nouveau l'existence de l'image au moment de la publication
            if image_path and not os.path.exists(image_path):
                print(f"⚠️ Image non trouvée lors de la publication: {image_path}")
                image_path = None
            
            success_count = 0
            results = {}
            
            # Publication LinkedIn
            if platforms.get("linkedin", False):
                try:
                    # Récupérer le token LinkedIn
                    linkedin_token = preferences.get('linkedin_token') or os.getenv('LINKEDIN_ACCESS_TOKEN')
                    
                    if linkedin_token:
                        # ✅ CORRECTION 3: Passer le chemin de l'image à la fonction de publication
                        result = await self.posting_agent.post_to_linkedin_real(
                            content_text, 
                            preferences,
                            image_path=image_path  # 🔧 Image incluse maintenant
                        )
                        
                        if result:
                            success_count += 1
                            results["linkedin"] = "success"
                            if image_path:
                                print(f"✅ Publié sur LinkedIn avec image: {result.get('post_url', 'N/A')}")
                            else:
                                print(f"✅ Publié sur LinkedIn (texte seul): {result.get('post_url', 'N/A')}")
                        else:
                            results["linkedin"] = "failed"
                            print("❌ Échec publication LinkedIn")
                    else:
                        results["linkedin"] = "no_token"
                        print("⚠️ Pas de token LinkedIn")
                        
                except Exception as e:
                    results["linkedin"] = f"error: {str(e)}"
                    print(f"❌ Erreur LinkedIn: {e}")
            
            # Publication Facebook
            if platforms.get("facebook", False):
                try:
                    # Récupérer le token Facebook
                    facebook_token = preferences.get('facebook_token') or os.getenv('FACEBOOK_ACCESS_TOKEN')
                    
                    if facebook_token:
                        # ✅ CORRECTION 4: Passer le chemin de l'image à la fonction de publication
                        result = await self.posting_agent.post_to_facebook_real(
                            content_text, 
                            preferences,
                            image_path=image_path  # 🔧 Image incluse maintenant
                        )
                        
                        if result:
                            success_count += 1
                            results["facebook"] = "success"
                            if image_path:
                                print(f"✅ Publié sur Facebook avec image: {result.get('post_url', 'N/A')}")
                            else:
                                print(f"✅ Publié sur Facebook (texte seul): {result.get('post_url', 'N/A')}")
                        else:
                            results["facebook"] = "failed"
                            print("❌ Échec publication Facebook")
                    else:
                        results["facebook"] = "no_token"
                        print("⚠️ Pas de token Facebook")
                        
                except Exception as e:
                    results["facebook"] = f"error: {str(e)}"
                    print(f"❌ Erreur Facebook: {e}")
            
            # Mettre à jour le statut du post
            if success_count > 0:
                post["status"] = "published"
                post["published_at"] = datetime.now().isoformat()
                post["results"] = results
                post["published_with_image"] = bool(image_path)  # 🔧 Tracker si publié avec image
                print(f"🎉 Post {post['id']} publié avec succès sur {success_count} plateforme(s)")
                if image_path:
                    print(f"🖼️ Image incluse: {os.path.basename(image_path)}")
            else:
                post["attempts"] += 1
                if post["attempts"] >= post["max_attempts"]:
                    post["status"] = "failed"
                    print(f"❌ Post {post['id']} marqué comme échoué après {post['attempts']} tentatives")
                else:
                    # Reprogrammer pour plus tard (dans 10 minutes)
                    new_schedule = datetime.now() + timedelta(minutes=10)
                    post["schedule_datetime"] = new_schedule.isoformat()
                    print(f"⏰ Post {post['id']} reprogrammé pour {new_schedule.strftime('%H:%M')}")
            
            # Sauvegarder les changements
            self._save_scheduled_post(post)
            
        except Exception as e:
            print(f"❌ Erreur publication post {post['id']}: {e}")
            post["status"] = "error"
            post["error"] = str(e)
            self._save_scheduled_post(post)
    
    # ✅ CORRECTION 5: Améliorer l'affichage des posts programmés
    def list_scheduled_posts(self) -> List[Dict]:
        """Liste tous les posts programmés avec info sur les images"""
        return [
            {
                "id": post["id"],
                "schedule_datetime": post["schedule_datetime"],
                "platforms": post["platforms"],
                "status": post["status"],
                "has_image": bool(post.get("image_path")),  # 🔧 Info sur l'image
                "image_path": post.get("image_path", "Aucune"),
                "preview": post["content"][:100] + "..." if len(post["content"]) > 100 else post["content"]
            }
            for post in self.scheduled_posts
        ]
    
    # Le reste du code reste identique...
    async def check_and_publish(self):
        """Vérifie et publie les posts dont l'heure est arrivée"""
        now = datetime.now()
        posts_to_publish = []
        
        for post in self.scheduled_posts:
            schedule_time = datetime.fromisoformat(post["schedule_datetime"])
            
            # Vérifier si c'est l'heure de publier (avec marge de 1 minute)
            if schedule_time <= now and post["status"] == "scheduled":
                posts_to_publish.append(post)
        
        # Publier les posts
        for post in posts_to_publish:
            await self._publish_scheduled_post(post)
    
    def load_scheduled_posts(self):
        """Charge tous les posts programmés depuis le disque"""
        self.scheduled_posts = []
        
        if not os.path.exists("data/scheduled_posts"):
            return
        
        for filename in os.listdir("data/scheduled_posts"):
            if filename.endswith('.json'):
                try:
                    with open(f"data/scheduled_posts/{filename}", 'r', encoding='utf-8') as f:
                        post_data = json.load(f)
                    
                    # Ne charger que les posts non publiés et non expirés
                    if post_data["status"] == "scheduled":
                        schedule_time = datetime.fromisoformat(post_data["schedule_datetime"])
                        if schedule_time > datetime.now():
                            self.scheduled_posts.append(post_data)
                        else:
                            # Marquer comme expiré si la date est passée
                            post_data["status"] = "expired"
                            self._save_scheduled_post(post_data)
                            
                except Exception as e:
                    print(f"⚠️ Erreur chargement {filename}: {e}")
        
        print(f"📅 {len(self.scheduled_posts)} posts programmés chargés")
    
    def start_scheduler(self):
        """Démarre le scheduler en arrière-plan"""
        if self.is_running:
            print("⚠️ Scheduler déjà en cours d'exécution")
            return
        
        self.is_running = True
        
        def scheduler_thread():
            """Thread pour le scheduler"""
            while self.is_running:
                try:
                    # Vérifier les posts à publier toutes les minutes
                    asyncio.run(self.check_and_publish())
                    time.sleep(60)  # Attendre 1 minute
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print(f"⚠️ Erreur scheduler: {e}")
                    time.sleep(60)
        
        # Démarrer le thread
        self.scheduler_thread = Thread(target=scheduler_thread, daemon=True)
        self.scheduler_thread.start()
        
        print("🚀 Scheduler démarré! Vérification toutes les minutes...")
    
    def stop_scheduler(self):
        """Arrête le scheduler"""
        self.is_running = False
        print("⏹️ Scheduler arrêté")
    
    def cancel_scheduled_post(self, post_id: str) -> bool:
        """Annule un post programmé"""
        for post in self.scheduled_posts:
            if post["id"] == post_id and post["status"] == "scheduled":
                post["status"] = "cancelled"
                post["cancelled_at"] = datetime.now().isoformat()
                self._save_scheduled_post(post)
                self.scheduled_posts.remove(post)
                print(f"❌ Post {post_id} annulé")
                return True
        
        print(f"⚠️ Post {post_id} non trouvé ou déjà traité")
        return False


# ============================================================================
# 🔧 Fonction corrigée pour interface utilisateur
# ============================================================================

def schedule_from_reviewed_content():
    """Interface pour programmer un contenu depuis reviewed_content - VERSION CORRIGÉE"""
    scheduler = ContentScheduler()
    
    # Lister les contenus disponibles
    reviewed_dir = "data/reviewed_content"
    if not os.path.exists(reviewed_dir):
        print("❌ Aucun contenu trouvé dans data/reviewed_content")
        return
    
    files = [f for f in os.listdir(reviewed_dir) if f.endswith('.json')]
    if not files:
        print("❌ Aucun fichier de contenu trouvé")
        return
    
    print("📋 Contenus disponibles:")
    for i, filename in enumerate(files, 1):
        # Charger un aperçu du contenu
        try:
            with open(os.path.join(reviewed_dir, filename), 'r', encoding='utf-8') as f:
                data = json.load(f)
            preview = data["content"][:80] + "..." if len(data["content"]) > 80 else data["content"]
            timestamp = data.get("timestamp", "N/A")
            
            # ✅ CORRECTION 6: Afficher info sur l'image
            image_info = ""
            if data.get("image_path"):
                if os.path.exists(data["image_path"]):
                    image_info = " 🖼️"
                else:
                    image_info = " ⚠️ (image manquante)"
            
            print(f"{i}. {filename} ({timestamp}){image_info}")
            print(f"   📝 {preview}")
        except:
            print(f"{i}. {filename} (erreur lecture)")
    
    # Sélection du fichier
    while True:
        try:
            choice = int(input(f"\nChoisissez un contenu (1-{len(files)}): "))
            if 1 <= choice <= len(files):
                selected_file = os.path.join(reviewed_dir, files[choice-1])
                break
            else:
                print("❌ Choix invalide")
        except ValueError:
            print("❌ Veuillez entrer un nombre")
    
    # ✅ CORRECTION 7: Vérifier et confirmer l'image avant programmation
    with open(selected_file, 'r', encoding='utf-8') as f:
        content_data = json.load(f)
    
    if content_data.get("image_path"):
        if os.path.exists(content_data["image_path"]):
            print(f"🖼️ Ce contenu inclut une image: {content_data['image_path']}")
        else:
            print(f"⚠️ Attention: Image manquante - {content_data['image_path']}")
            keep_going = input("Continuer sans image? (o/n): ").strip().lower()
            if keep_going not in ['o', 'oui', 'y', 'yes']:
                print("❌ Programmation annulée")
                return
    else:
        print("📝 Ce contenu ne contient pas d'image")
    
    # Sélection des plateformes
    print("\n🌐 Plateformes de publication:")
    print("1. LinkedIn seulement")
    print("2. Facebook seulement")
    print("3. LinkedIn + Facebook")
    
    while True:
        platform_choice = input("Choisissez (1-3): ").strip()
        if platform_choice in ["1", "2", "3"]:
            platforms = {
                "1": {"linkedin": True, "facebook": False},
                "2": {"linkedin": False, "facebook": True},
                "3": {"linkedin": True, "facebook": True}
            }[platform_choice]
            break
        print("❌ Choix invalide")
    
    # Sélection date/heure
    print("\n⏰ Programmation:")
    print("1. Dans 1 heure")
    print("2. Dans 2 heures") 
    print("3. Demain à 9h")
    print("4. Date/heure personnalisée")
    
    while True:
        time_choice = input("Choisissez (1-4): ").strip()
        
        if time_choice == "1":
            schedule_time = datetime.now() + timedelta(hours=1)
            break
        elif time_choice == "2":
            schedule_time = datetime.now() + timedelta(hours=2)
            break
        elif time_choice == "3":
            tomorrow = datetime.now() + timedelta(days=1)
            schedule_time = tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)
            break
        elif time_choice == "4":
            try:
                date_str = input("Date (DD/MM/YYYY): ").strip()
                time_str = input("Heure (HH:MM): ").strip()
                
                # Parser la date et l'heure
                day, month, year = map(int, date_str.split('/'))
                hour, minute = map(int, time_str.split(':'))
                
                schedule_time = datetime(year, month, day, hour, minute)
                
                if schedule_time <= datetime.now():
                    print("❌ La date doit être dans le futur")
                    continue
                
                break
            except ValueError:
                print("❌ Format invalide. Utilisez DD/MM/YYYY et HH:MM")
        else:
            print("❌ Choix invalide")
    
    # Programmer le post
    post_id = scheduler.schedule_post(selected_file, schedule_time, platforms)
    
    # Démarrer le scheduler si pas déjà actif
    if not scheduler.is_running:
        start_scheduler = input("\n🚀 Démarrer le scheduler maintenant? (o/n): ").strip().lower()
        if start_scheduler in ['o', 'oui', 'y', 'yes']:
            scheduler.start_scheduler()
            print("💡 Le scheduler vérifie les posts toutes les minutes.")
            print("💡 Gardez ce script en cours d'exécution pour les publications automatiques.")
    
    return scheduler


# ============================================================================
# 🛠️ Script de diagnostic pour vérifier les posts programmés
# ============================================================================

def diagnose_scheduled_posts():
    """Diagnostic des posts programmés pour vérifier les images"""
    print("🔍 Diagnostic des posts programmés")
    print("=" * 40)
    
    scheduler = ContentScheduler()
    posts = scheduler.list_scheduled_posts()
    
    if not posts:
        print("📭 Aucun post programmé")
        return
    
    for post in posts:
        print(f"\n📋 Post ID: {post['id']}")
        print(f"📅 Programmé: {datetime.fromisoformat(post['schedule_datetime']).strftime('%d/%m/%Y à %H:%M')}")
        print(f"🌐 Plateformes: {', '.join([p for p, enabled in post['platforms'].items() if enabled])}")
        print(f"📊 Statut: {post['status']}")
        
        if post['has_image']:
            if os.path.exists(post['image_path']):
                print(f"🖼️ Image: ✅ {post['image_path']}")
            else:
                print(f"🖼️ Image: ❌ MANQUANTE - {post['image_path']}")
        else:
            print("🖼️ Image: Aucune")
        
        print(f"📝 Aperçu: {post['preview']}")


if __name__ == "__main__":
    # Interface interactive améliorée
    print("📅 Système de publication programmée - Version Corrigée")
    print("=" * 55)
    print("1. Programmer un nouveau post")
    print("2. Diagnostic des posts programmés")
    print("3. Lister les posts programmés")
    
    choice = input("\nChoisissez une option (1-3): ").strip()
    
    if choice == "1":
        scheduler = schedule_from_reviewed_content()
        if scheduler and scheduler.is_running:
            try:
                print("\n⌛ Scheduler actif. Appuyez sur Ctrl+C pour arrêter...")
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                scheduler.stop_scheduler()
                print("\n👋 Scheduler arrêté. Au revoir!")
    
    elif choice == "2":
        diagnose_scheduled_posts()
    
    elif choice == "3":
        scheduler = ContentScheduler()
        posts = scheduler.list_scheduled_posts()
        
        if posts:
            for post in posts:
                print(f"\n📋 {post['id']} - {post['status']}")
                print(f"📅 {datetime.fromisoformat(post['schedule_datetime']).strftime('%d/%m/%Y à %H:%M')}")
                if post['has_image']:
                    print("🖼️ Avec image")
        else:
            print("📭 Aucun post programmé")
    
    else:
        print("❌ Choix invalide")