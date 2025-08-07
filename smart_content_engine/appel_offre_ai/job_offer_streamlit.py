#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface Streamlit pour la génération et publication d'offres d'emploi LinkedIn
"""

import streamlit as st
import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime

# Ajout du chemin parent pour les imports (à adapter selon votre structure)
sys.path.append(str(Path(__file__).parent.parent))

# Imports de vos modules (à adapter selon votre structure)
try:
    from core.offer_creator import OfferCreator
    from core.linkedin_publisher import LinkedInPublisher
    from core.role_detector import detect_roles
except ImportError:
    st.error("⚠️ Modules core non trouvés. Vérifiez la structure de votre projet.")
    st.stop()

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Générateur d'Offres LinkedIn",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé optimisé pour le mode clair
st.markdown("""
<style>
    /* Force le mode clair */
    .stApp {
        background-color: #ffffff;
        color: #262730;
    }
    
    /* Header principal */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
    }
    
    /* Cards des étapes - mode clair */
    .step-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #e3e8ff;
        border-left: 5px solid #667eea;
        margin-bottom: 1rem;
        box-shadow: 0 2px 10px rgba(102, 126, 234, 0.1);
        color: #262730;
    }
    
    /* Cards de succès - mode clair */
    .success-card {
        background: linear-gradient(135deg, #f0fff4 0%, #dcfce7 100%);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #bbf7d0;
        border-left: 4px solid #22c55e;
        margin: 0.5rem 0;
        color: #166534;
        box-shadow: 0 2px 8px rgba(34, 197, 94, 0.1);
    }
    
    /* Cards d'avertissement - mode clair */
    .warning-card {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #fed7aa;
        border-left: 4px solid #f59e0b;
        margin: 0.5rem 0;
        color: #92400e;
        box-shadow: 0 2px 8px rgba(245, 158, 11, 0.1);
    }
    
    /* Cards d'erreur - mode clair */
    .error-card {
        background: linear-gradient(135deg, #fef2f2 0%, #fecaca 100%);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #fca5a5;
        border-left: 4px solid #ef4444;
        margin: 0.5rem 0;
        color: #991b1b;
        box-shadow: 0 2px 8px rgba(239, 68, 68, 0.1);
    }
    
    /* Barre de progression */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Sidebar en mode clair */
    .css-1d391kg {
        background-color: #f8f9ff;
    }
    
    /* Boutons personnalisés */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Input fields en mode clair */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: #ffffff;
        border: 2px solid #e3e8ff;
        color: #262730;
        border-radius: 8px;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Expanders en mode clair */
    .streamlit-expanderHeader {
        background-color: #f8f9ff;
        color: #262730;
        border: 1px solid #e3e8ff;
    }
    
    /* Métriques et info boxes */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f0f4ff 100%);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #e3e8ff;
        text-align: center;
        box-shadow: 0 2px 10px rgba(102, 126, 234, 0.05);
    }
</style>
""", unsafe_allow_html=True)

class StreamlitJobOfferApp:
    def __init__(self):
        """Initialise l'application Streamlit"""
        self.output_dir = "generated_offers"
        self.config_file = "config/linkedin_config.json"
        
        # Créer les dossiers nécessaires
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs("config", exist_ok=True)
        os.makedirs("data/posted_content", exist_ok=True)
        
        # Initialiser les objets core
        if 'offer_creator' not in st.session_state:
            st.session_state.offer_creator = OfferCreator()
        if 'linkedin_publisher' not in st.session_state:
            st.session_state.linkedin_publisher = LinkedInPublisher()
    
    def load_linkedin_config(self):
        """Charge la configuration LinkedIn"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return None
        except Exception as e:
            st.error(f"Erreur lecture config: {e}")
            return None
    
    def save_linkedin_config(self, token):
        """Sauvegarde la configuration LinkedIn"""
        config = {
            "access_token": token,
            "created_at": datetime.now().isoformat(),
            "scopes": ["w_member_social", "r_liteprofile"]
        }
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            st.error(f"Erreur sauvegarde config: {e}")
            return False
    
    def render_header(self):
        """Affiche l'en-tête de l'application"""
        st.markdown("""
        <div class="main-header">
            <h1>🚀 Générateur d'Offres d'Emploi LinkedIn</h1>
            <p>Analysez votre projet • Détectez les profils • Générez et publiez vos offres</p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_sidebar_config(self):
        """Affiche la configuration LinkedIn dans la sidebar"""
        st.sidebar.header("⚙️ Configuration LinkedIn")
        
        config = self.load_linkedin_config()
        
        if config and config.get('access_token'):
            st.sidebar.success("✅ Token LinkedIn configuré")
            st.sidebar.write(f"📅 Créé le : {config.get('created_at', 'N/A')[:10]}")
            
            if st.sidebar.button("🔄 Renouveler le token"):
                if os.path.exists(self.config_file):
                    os.remove(self.config_file)
                st.experimental_rerun()
        else:
            st.sidebar.warning("⚠️ Token LinkedIn requis")
            
            with st.sidebar.expander("📘 Comment obtenir un token"):
                st.write("""
                1. Allez sur https://developer.linkedin.com/
                2. Créez une application
                3. Obtenez votre access_token avec les scopes :
                   - w_member_social
                   - r_liteprofile
                """)
            
            token = st.sidebar.text_input(
                "🔑 Access Token LinkedIn",
                type="password",
                placeholder="Entrez votre token..."
            )
            
            if st.sidebar.button("💾 Sauvegarder"):
                if token:
                    if self.save_linkedin_config(token):
                        st.sidebar.success("✅ Token sauvegardé !")
                        st.experimental_rerun()
                else:
                    st.sidebar.error("❌ Token requis")
    
    def step_1_project_analysis(self):
        """Étape 1: Analyse du projet"""
        st.markdown('<div class="step-card">', unsafe_allow_html=True)
        st.header("📊 Étape 1: Analyse du Projet")
        
        st.write("Décrivez votre projet en détail pour une détection optimale des profils nécessaires.")
        
        project_description = st.text_area(
            "📝 Description du projet",
            placeholder="Ex: Développement d'une plateforme e-commerce avec IA pour la recommandation personnalisée, utilisant React, Python, AWS...",
            height=150,
            key="project_description"
        )
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            analyze_btn = st.button("🔍 Analyser le projet", type="primary")
        
        if analyze_btn and project_description:
            with st.spinner("🤖 Analyse en cours..."):
                try:
                    detected_roles = detect_roles(project_description)
                    st.session_state.project_description = project_description
                    st.session_state.detected_roles = detected_roles
                    st.session_state.step_1_complete = True
                    
                    st.markdown('<div class="success-card">', unsafe_allow_html=True)
                    st.success("✅ Analyse terminée avec succès !")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"❌ Erreur lors de l'analyse : {e}")
                    # Utiliser des rôles par défaut
                    default_roles = """
Rôles recommandés pour ce projet :
1. Data Scientist - Analyse et modélisation des données
2. Développeur Full-Stack - Développement de la plateforme  
3. DevOps Engineer - Infrastructure et déploiement
4. Product Manager - Gestion de produit et stratégie
                    """
                    st.session_state.detected_roles = default_roles
                    st.session_state.step_1_complete = True
        
        elif analyze_btn and not project_description:
            st.error("❌ Veuillez décrire votre projet")
        
        # Afficher les résultats si disponibles
        if hasattr(st.session_state, 'detected_roles'):
            st.subheader("🎯 Profils détectés")
            st.write(st.session_state.detected_roles)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        return hasattr(st.session_state, 'step_1_complete')
    
    def step_2_role_selection(self):
        """Étape 2: Sélection des rôles"""
        if not hasattr(st.session_state, 'step_1_complete'):
            st.info("👆 Complétez d'abord l'analyse du projet")
            return False
        
        st.markdown('<div class="step-card">', unsafe_allow_html=True)
        st.header("👥 Étape 2: Sélection des Profils à Recruter")
        
        st.write("Sélectionnez les profils pour lesquels vous souhaitez générer des offres d'emploi.")
        
        # Afficher les rôles détectés comme référence
        with st.expander("📋 Rôles suggérés par l'IA"):
            st.write(st.session_state.detected_roles)
        
        # Interface pour saisir les rôles
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Initialiser la liste des rôles sélectionnés
            if 'selected_roles' not in st.session_state:
                st.session_state.selected_roles = []
            
            new_role = st.text_input(
                "✏️ Ajouter un rôle",
                placeholder="Ex: Data Scientist",
                key="new_role_input"
            )
            
            if st.button("➕ Ajouter") and new_role:
                if new_role not in st.session_state.selected_roles:
                    st.session_state.selected_roles.append(new_role)
                    st.success(f"✅ Ajouté: {new_role}")
                    # Clear input
                    st.session_state.new_role_input = ""
                else:
                    st.warning("⚠️ Rôle déjà ajouté")
        
        with col2:
            # Suggestions rapides
            st.write("**Suggestions rapides:**")
            quick_roles = [
                "Data Scientist",
                "Développeur Full-Stack", 
                "DevOps Engineer",
                "Product Manager",
                "UI/UX Designer"
            ]
            
            for role in quick_roles:
                if st.button(f"+ {role}", key=f"quick_{role}"):
                    if role not in st.session_state.selected_roles:
                        st.session_state.selected_roles.append(role)
        
        # Afficher les rôles sélectionnés
        if st.session_state.selected_roles:
            st.subheader("📊 Rôles sélectionnés:")
            
            for i, role in enumerate(st.session_state.selected_roles):
                col_role, col_remove = st.columns([3, 1])
                with col_role:
                    st.write(f"**{i+1}.** {role}")
                with col_remove:
                    if st.button("🗑️", key=f"remove_{i}"):
                        st.session_state.selected_roles.remove(role)
                        st.experimental_rerun()
            
            st.session_state.step_2_complete = True
        else:
            st.info("ℹ️ Aucun rôle sélectionné")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        return len(st.session_state.selected_roles) > 0
    
    def step_3_offer_generation(self):
        """Étape 3: Génération des offres"""
        if not hasattr(st.session_state, 'step_2_complete'):
            st.info("👆 Sélectionnez d'abord les rôles à recruter")
            return False
        
        st.markdown('<div class="step-card">', unsafe_allow_html=True)
        st.header("🎨 Étape 3: Génération des Offres")
        
        st.write(f"Génération d'offres pour {len(st.session_state.selected_roles)} rôle(s) sélectionné(s).")
        
        if st.button("🚀 Générer les offres", type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            generated_offers = []
            
            for i, role in enumerate(st.session_state.selected_roles):
                progress = (i + 1) / len(st.session_state.selected_roles)
                progress_bar.progress(progress)
                status_text.text(f"🔄 Génération pour {role}...")
                
                try:
                    offer = st.session_state.offer_creator.create_offer(
                        role, 
                        st.session_state.project_description, 
                        self.output_dir
                    )
                    
                    if offer and os.path.exists(offer.get('image', '')):
                        generated_offers.append(offer)
                        st.success(f"✅ Offre générée pour {role}")
                    else:
                        st.error(f"❌ Erreur génération pour {role}")
                        
                except Exception as e:
                    st.error(f"❌ Erreur pour {role}: {e}")
                
                time.sleep(1)  # Pause pour l'UX
            
            progress_bar.progress(1.0)
            status_text.text(f"✅ Génération terminée: {len(generated_offers)} offres créées")
            
            st.session_state.generated_offers = generated_offers
            st.session_state.step_3_complete = True
            
            # Afficher les résultats
            if generated_offers:
                st.subheader("📋 Offres générées:")
                
                for offer in generated_offers:
                    with st.expander(f"📄 {offer['role']}"):
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.write("**Texte de l'offre:**")
                            st.write(offer['text'][:200] + "...")
                        
                        with col2:
                            if os.path.exists(offer['image']):
                                st.image(offer['image'], caption=f"Image pour {offer['role']}")
                            else:
                                st.write("⚠️ Image non disponible")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        return hasattr(st.session_state, 'step_3_complete')
    
    def step_4_linkedin_publishing(self):
        """Étape 4: Publication sur LinkedIn"""
        if not hasattr(st.session_state, 'step_3_complete'):
            st.info("👆 Générez d'abord les offres d'emploi")
            return
        
        st.markdown('<div class="step-card">', unsafe_allow_html=True)
        st.header("📤 Étape 4: Publication sur LinkedIn")
        
        config = self.load_linkedin_config()
        
        if not config or not config.get('access_token'):
            st.markdown('<div class="warning-card">', unsafe_allow_html=True)
            st.warning("⚠️ Token LinkedIn requis. Configurez-le dans la barre latérale.")
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            return
        
        offers = st.session_state.get('generated_offers', [])
        
        if not offers:
            st.error("❌ Aucune offre générée à publier")
            st.markdown('</div>', unsafe_allow_html=True)
            return
        
        st.write(f"Prêt à publier {len(offers)} offre(s) sur LinkedIn.")
        
        # Sélection des offres à publier
        st.subheader("📋 Sélectionnez les offres à publier:")
        
        offers_to_publish = []
        for i, offer in enumerate(offers):
            if st.checkbox(f"📄 {offer['role']}", value=True, key=f"publish_{i}"):
                offers_to_publish.append(offer)
        
        if offers_to_publish:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                if st.button("🚀 Publier sur LinkedIn", type="primary"):
                    self.publish_offers_to_linkedin(offers_to_publish, config['access_token'])
            
            with col2:
                st.info(f"📊 {len(offers_to_publish)} offre(s) sélectionnée(s)")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def publish_offers_to_linkedin(self, offers, access_token):
        """Publie les offres sélectionnées sur LinkedIn"""
        st.subheader("📤 Publication en cours...")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        published_count = 0
        
        for i, offer in enumerate(offers):
            progress = (i + 1) / len(offers)
            progress_bar.progress(progress)
            status_text.text(f"📤 Publication de {offer['role']}...")
            
            try:
                result = st.session_state.linkedin_publisher.post_content_with_image(
                    content=offer['text'],
                    access_token=access_token,
                    image_path=offer['image']
                )
                
                if result and result.get('status') == 'success':
                    published_count += 1
                    st.success(f"✅ {offer['role']} publié avec succès")
                    if result.get('post_url'):
                        st.write(f"🔗 [Voir le post]({result['post_url']})")
                else:
                    st.error(f"❌ Échec publication pour {offer['role']}")
                
                # Pause entre publications
                if i < len(offers) - 1:
                    for countdown in range(30, 0, -1):
                        status_text.text(f"⏳ Pause de {countdown}s avant prochaine publication...")
                        time.sleep(1)
                
            except Exception as e:
                st.error(f"❌ Erreur publication {offer['role']}: {e}")
        
        progress_bar.progress(1.0)
        status_text.text("✅ Publication terminée")
        
        st.markdown('<div class="success-card">', unsafe_allow_html=True)
        st.success(f"🎉 Publication terminée: {published_count}/{len(offers)} offres publiées")
        st.markdown('</div>', unsafe_allow_html=True)
    
    def run(self):
        """Lance l'application Streamlit"""
        self.render_header()
        self.render_sidebar_config()
        
        # Étapes de l'application
        step_1_ok = self.step_1_project_analysis()
        
        if step_1_ok:
            step_2_ok = self.step_2_role_selection()
            
            if step_2_ok:
                step_3_ok = self.step_3_offer_generation()
                
                if step_3_ok:
                    self.step_4_linkedin_publishing()
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #666; padding: 1rem;'>
            🚀 Générateur d'Offres LinkedIn • Développé avec Streamlit
        </div>
        """, unsafe_allow_html=True)

def main():
    """Point d'entrée principal"""
    app = StreamlitJobOfferApp()
    app.run()

if __name__ == "__main__":
    main()