# ============================================================================
# 📄 streamlit_app.py - Interface Streamlit pour Smart Content Engine Multi-Plateformes
# ============================================================================
import streamlit as st
import asyncio
import json
import os
from datetime import datetime, timedelta
from PIL import Image
import time
from dotenv import load_dotenv
import requests

# Import des modules existants
from agents.content_agent import ContentAgent
from agents.reviewer_agent import ReviewerAgent
from agents.posting_agent import PostingAgent
from agents.agent_image_prompt import generate_image_prompt
from core.image_generator import ImageGenerator
from linkedin_auth import LinkedInAuth
from facebook_auth import FacebookAuth
from scheduler import ContentScheduler

# Chargement des variables d'environnement
load_dotenv()

# Configuration de la page
st.set_page_config(
    page_title="Smart Content Engine - Multi-Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "Smart Content Engine - Interface de création de contenu LinkedIn + Facebook"
    }
)

# CSS personnalisé pour forcer le mode clair et améliorer l'apparence
st.markdown("""
<style>
/* Forcer le mode clair */
[data-testid="stAppViewContainer"] {
    background-color: #ffffff !important;
}

[data-testid="stSidebar"] {
    background-color: #f0f2f6 !important;
}

/* Styles pour les étapes */
.step-container {
    background-color: #f8f9fa;
    padding: 1rem;
    border-radius: 10px;
    margin: 1rem 0;
    border-left: 4px solid #0077b5;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.step-completed {
    border-left-color: #28a745;
    background-color: #d4edda;
}

.step-current {
    border-left-color: #ffc107;
    background-color: #fff3cd;
}

.step-pending {
    border-left-color: #dc3545;
    background-color: #f8d7da;
}

/* Preview LinkedIn réaliste */
.linkedin-preview {
    background-color: #ffffff;
    border: 1px solid #e1e5e9;
    border-radius: 8px;
    padding: 0;
    margin: 20px 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.linkedin-header {
    display: flex;
    align-items: center;
    padding: 16px 20px 12px 20px;
    border-bottom: 1px solid #f0f0f0;
}

.linkedin-avatar {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background-color: #0077b5;
    margin-right: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: bold;
    font-size: 18px;
    flex-shrink: 0;
}

.linkedin-user-info {
    flex: 1;
}

.linkedin-name {
    font-weight: 600;
    color: #191919;
    font-size: 14px;
    line-height: 1.2;
}

.linkedin-time {
    color: #666666;
    font-size: 12px;
    margin-top: 2px;
}

.linkedin-menu {
    color: #666666;
    font-size: 18px;
    cursor: pointer;
    padding: 4px;
    border-radius: 4px;
    transition: background-color 0.2s;
}

.linkedin-menu:hover {
    background-color: #f0f0f0;
}

.linkedin-content {
    padding: 12px 20px 16px 20px;
    line-height: 1.6;
    color: #191919;
    font-size: 14px;
    word-wrap: break-word;
}

.linkedin-actions {
    display: flex;
    border-top: 1px solid #f0f0f0;
    padding: 8px 0;
}

.linkedin-action {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 8px 0;
    cursor: pointer;
    border-radius: 4px;
    margin: 0 4px;
    transition: background-color 0.2s;
}

.linkedin-action:hover {
    background-color: #f0f0f0;
}

/* Preview Facebook réaliste */
.facebook-preview {
    background-color: #ffffff;
    border: 1px solid #dadde1;
    border-radius: 8px;
    padding: 0;
    margin: 20px 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.facebook-header {
    display: flex;
    align-items: center;
    padding: 16px 20px 12px 20px;
    border-bottom: 1px solid #f0f0f0;
}

.facebook-avatar {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background-color: #1877f2;
    margin-right: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: bold;
    font-size: 18px;
    flex-shrink: 0;
}

.facebook-user-info {
    flex: 1;
}

.facebook-name {
    font-weight: 600;
    color: #050505;
    font-size: 14px;
    line-height: 1.2;
}

.facebook-time {
    color: #65676b;
    font-size: 12px;
    margin-top: 2px;
}

.facebook-content {
    padding: 12px 20px 16px 20px;
    line-height: 1.6;
    color: #050505;
    font-size: 14px;
    word-wrap: break-word;
}

.facebook-actions {
    display: flex;
    border-top: 1px solid #ced0d4;
    padding: 8px 12px;
}

.facebook-action {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 8px 0;
    cursor: pointer;
    border-radius: 4px;
    margin: 0 4px;
    transition: background-color 0.2s;
}

.facebook-action:hover {
    background-color: #f0f2f5;
}

.action-icon {
    font-size: 16px;
    margin-right: 6px;
}

.action-text {
    font-size: 12px;
    color: #65676b;
    font-weight: 500;
}

/* Platform selector */
.platform-selector {
    display: flex;
    gap: 10px;
    margin: 20px 0;
    justify-content: center;
}

.platform-button {
    padding: 10px 20px;
    border: 2px solid #e1e5e9;
    border-radius: 8px;
    background-color: white;
    cursor: pointer;
    transition: all 0.3s ease;
    font-weight: 500;
}

.platform-button.linkedin {
    border-color: #0077b5;
    color: #0077b5;
}

.platform-button.facebook {
    border-color: #1877f2;
    color: #1877f2;
}

.platform-button.both {
    background: linear-gradient(135deg, #0077b5 0%, #1877f2 100%);
    color: white;
    border: none;
}

.platform-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

/* Boutons personnalisés */
.regenerate-btn {
    background-color: #ff6b6b;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    margin: 5px;
    transition: background-color 0.3s ease;
}

.regenerate-btn:hover {
    background-color: #ff5252;
}

/* Amélioration des formulaires */
[data-testid="stForm"] {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 8px;
    border: 1px solid #e1e5e9;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

/* Amélioration des boutons */
[data-testid="stButton"] > button {
    border-radius: 6px;
    font-weight: 500;
    transition: all 0.3s ease;
}

/* Mode clair forcé pour tous les éléments */
* {
    color-scheme: light !important;
}

/* Amélioration de la barre de progression */
[data-testid="stProgressBar"] {
    background-color: #e9ecef;
}

[data-testid="stProgressBar"] > div {
    background: linear-gradient(90deg, #0077b5 0%, #1877f2 100%);
}
</style>
""", unsafe_allow_html=True)

class StreamlitContentEngine:
    def __init__(self):
        self.content_agent = ContentAgent()
        self.reviewer_agent = ReviewerAgent()
        self.posting_agent = PostingAgent()
        self.linkedin_auth = LinkedInAuth()
        self.facebook_auth = FacebookAuth()
        self.scheduler = ContentScheduler()
        
        # Initialisation des variables de session
        if 'current_step' not in st.session_state:
            st.session_state.current_step = 1
        if 'publication_mode' not in st.session_state:
            st.session_state.publication_mode = None
        if 'platforms' not in st.session_state:
            st.session_state.platforms = {}
        if 'business_info' not in st.session_state:
            st.session_state.business_info = {
                "company_name": "",
                "business_sector": "technology",
                "target_audience": "professionals",
                "company_size": "medium"
            }
        if 'content_preferences' not in st.session_state:
            st.session_state.content_preferences = {
                "language": "fr",
                "content_type": "thought_leadership",
                "topic": "",
                "cta_type": "engagement"
            }
        if 'generated_content' not in st.session_state:
            st.session_state.generated_content = None
        if 'reviewed_content' not in st.session_state:
            st.session_state.reviewed_content = None
        if 'image_path' not in st.session_state:
            st.session_state.image_path = None
        if 'schedule_datetime' not in st.session_state:
            st.session_state.schedule_datetime = None
        if 'linkedin_token' not in st.session_state:
            # Charger automatiquement le token sauvegardé
            saved_token = self.linkedin_auth.load_saved_token()
            if saved_token:
                st.session_state.linkedin_token = saved_token
            else:
                st.session_state.linkedin_token = None
        if 'facebook_token' not in st.session_state:
            # Charger automatiquement le token Facebook sauvegardé
            saved_token = self.facebook_auth.load_saved_token()
            if saved_token:
                st.session_state.facebook_token = saved_token
            else:
                st.session_state.facebook_token = None

    def render_header(self):
        """Affiche l'en-tête de l'application"""
        st.title("🚀 Smart Content Engine - Multi-Platform")
        st.markdown("### Création de contenu business intelligent pour LinkedIn & Facebook")
        
        # Notifications des tokens chargés
        col1, col2 = st.columns(2)
        with col1:
            if st.session_state.linkedin_token:
                st.success("🔗 LinkedIn configuré - Publication disponible !")
            else:
                st.warning("⚠️ LinkedIn non configuré")
        
        with col2:
            if st.session_state.facebook_token:
                st.success("📘 Facebook configuré - Publication disponible !")
            else:
                st.warning("⚠️ Facebook non configuré")
        
        st.markdown("---")

    def render_steps_progress(self):
        """Affiche la barre de progression des étapes"""
        steps = [
            "📅 Mode Publication",
            "🌐 Plateformes",
            "🏢 Configuration Business",
            "📝 Préférences Contenu", 
            "🤖 Génération Contenu",
            "🔍 Review Contenu",
            "🎨 Génération Image",
            "📋 Preview",
            "📤 Publication"
        ]
        
        # Création des colonnes pour les étapes
        cols = st.columns(len(steps))
        
        for i, (col, step) in enumerate(zip(cols, steps)):
            with col:
                if i + 1 < st.session_state.current_step:
                    # Étape terminée
                    st.markdown(f"✅ {step}")
                elif i + 1 == st.session_state.current_step:
                    # Étape actuelle
                    st.markdown(f"🔄 **{step}**")
                else:
                    # Étape à venir
                    st.markdown(f"⏳ {step}")

    def step_publication_mode(self):
        """Étape 1: Mode de publication"""
        st.header("📅 Mode de publication")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🚀 Publication Immédiate")
            st.write("Publier votre contenu immédiatement après création et review")
            if st.button("Choisir Publication Immédiate", key="immediate", use_container_width=True):
                st.session_state.publication_mode = "immediate"
                st.success("✅ Publication immédiate sélectionnée!")
                time.sleep(1)
                st.session_state.current_step = 2
                st.rerun()
        
        with col2:
            st.markdown("### ⏰ Publication Programmée")
            st.write("Programmer votre contenu pour une publication ultérieure")
            if st.button("Choisir Publication Programmée", key="scheduled", use_container_width=True):
                st.session_state.publication_mode = "scheduled"
                st.success("✅ Publication programmée sélectionnée!")
                time.sleep(1)
                st.session_state.current_step = 2
                st.rerun()

    def step_platform_selection(self):
        """Étape 2: Sélection des plateformes"""
        st.header("🌐 Sélection des plateformes")
        
        st.markdown("""
        <div class="platform-selector">
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 💼 LinkedIn Seulement")
            st.write("Focus professionnel et networking B2B")
            if st.button("LinkedIn Seulement", key="linkedin_only", use_container_width=True):
                st.session_state.platforms = {"linkedin": True, "facebook": False}
                st.success("✅ LinkedIn sélectionné!")
                time.sleep(1)
                st.session_state.current_step = 3
                st.rerun()
        
        with col2:
            st.markdown("### 📘 Facebook Seulement")
            st.write("Focus social media et engagement communautaire")
            if st.button("Facebook Seulement", key="facebook_only", use_container_width=True):
                st.session_state.platforms = {"linkedin": False, "facebook": True}
                st.success("✅ Facebook sélectionné!")
                time.sleep(1)
                st.session_state.current_step = 3
                st.rerun()
        
        with col3:
            st.markdown("### 🚀 Multi-Plateformes")
            st.write("Portée maximale avec LinkedIn + Facebook")
            if st.button("LinkedIn + Facebook", key="both_platforms", use_container_width=True):
                st.session_state.platforms = {"linkedin": True, "facebook": True}
                st.success("✅ Multi-plateformes sélectionné!")
                time.sleep(1)
                st.session_state.current_step = 3
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

    def step_business_config(self):
        """Étape 3: Configuration business"""
        st.header("🏢 Configuration de votre business")
        
        with st.form("business_config_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                company_name = st.text_input("📛 Nom de votre entreprise", 
                                           value=st.session_state.business_info.get('company_name', ''),
                                           key="company_name_input")
                
                business_sector = st.selectbox(
                    "🏭 Secteur d'activité",
                    ["technology", "marketing", "finance", "consulting", "healthcare", 
                     "education", "retail", "manufacturing", "real_estate", "autre"],
                    index=["technology", "marketing", "finance", "consulting", "healthcare", 
                           "education", "retail", "manufacturing", "real_estate", "autre"].index(
                               st.session_state.business_info.get('business_sector', 'technology')),
                    key="business_sector_select"
                )
                
                if business_sector == "autre":
                    business_sector = st.text_input("📝 Précisez votre secteur", key="custom_sector_input")
            
            with col2:
                # Adapter les options d'audience selon les plateformes sélectionnées
                platforms = st.session_state.platforms
                audience_options = ["professionals", "entrepreneurs", "executives", "managers", "consultants", "freelancers"]
                
                if platforms.get("facebook"):
                    audience_options.extend(["customers", "community"])
                
                target_audience = st.selectbox(
                    "🎯 Audience cible",
                    audience_options,
                    index=audience_options.index(st.session_state.business_info.get('target_audience', 'professionals')) 
                    if st.session_state.business_info.get('target_audience') in audience_options else 0,
                    key="target_audience_select"
                )
                
                company_size = st.selectbox(
                    "👥 Taille de l'entreprise",
                    ["freelance", "startup", "sme", "medium", "enterprise"],
                    index=["freelance", "startup", "sme", "medium", "enterprise"].index(
                              st.session_state.business_info.get('company_size', 'medium')),
                    key="company_size_select"
                )
            
            submitted = st.form_submit_button("✅ Valider la configuration")
            
            if submitted and company_name:
                # Mettre à jour les informations business
                st.session_state.business_info.update({
                    "company_name": company_name,
                    "business_sector": business_sector,
                    "target_audience": target_audience,
                    "company_size": company_size
                })
                st.session_state.current_step = 4
                st.rerun()
            elif submitted and not company_name:
                st.error("❌ Le nom de l'entreprise est requis!")

    def step_content_preferences(self):
        """Étape 4: Préférences de contenu"""
        st.header("📝 Préférences de contenu")
        
        with st.form("content_preferences_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                language = st.selectbox(
                    "🌐 Langue du contenu",
                    ["fr", "en"],
                    index=0 if st.session_state.content_preferences.get('language') == 'fr' else 1,
                    key="lang_select"
                )
                
                # Adapter les types de contenu selon les plateformes
                platforms = st.session_state.platforms
                content_types = ["thought_leadership", "company_update", "industry_insight", 
                               "product_showcase", "team_culture", "educational"]
                
                if platforms.get("facebook"):
                    content_types.extend(["promotional", "community_event"])
                
                content_type_labels = {
                    "thought_leadership": "Leadership/Expertise",
                    "company_update": "Actualités entreprise",
                    "industry_insight": "Insights secteur",
                    "product_showcase": "Produit/Service",
                    "team_culture": "Équipe/Culture",
                    "educational": "Éducatif/Conseils",
                    "promotional": "Promotionnel/Marketing",
                    "community_event": "Événement communauté"
                }
                
                content_type = st.selectbox(
                    "📈 Type de contenu",
                    content_types,
                    index=content_types.index(st.session_state.content_preferences.get('content_type', 'thought_leadership'))
                    if st.session_state.content_preferences.get('content_type') in content_types else 0,
                    format_func=lambda x: content_type_labels.get(x, x),
                    key="content_type_select"
                )
            
            with col2:
                topic = st.text_input("💡 Sujet spécifique (optionnel)", 
                                    value=st.session_state.content_preferences.get('topic', ''),
                                    key="topic_input")
                
                # Adapter les CTA selon les plateformes
                cta_options = ["engagement", "traffic", "lead_gen", "networking", "education"]
                if platforms.get("facebook"):
                    cta_options.extend(["sales", "brand_awareness"])
                
                cta_labels = {
                    "engagement": "Engagement (likes, commentaires)",
                    "traffic": "Trafic vers site web",
                    "lead_gen": "Génération de leads",
                    "networking": "Networking professionnel",
                    "education": "Éducation/Sensibilisation",
                    "sales": "Ventes/Conversion",
                    "brand_awareness": "Notoriété de marque"
                }
                
                cta_type = st.selectbox(
                    "🎯 Objectif du post",
                    cta_options,
                    index=cta_options.index(st.session_state.content_preferences.get('cta_type', 'engagement'))
                    if st.session_state.content_preferences.get('cta_type') in cta_options else 0,
                    format_func=lambda x: cta_labels.get(x, x),
                    key="cta_type_select"
                )
            
            submitted = st.form_submit_button("✅ Valider les préférences")
            
            if submitted:
                # Mettre à jour les préférences
                st.session_state.content_preferences.update({
                    "language": language,
                    "content_type": content_type,
                    "topic": topic if topic else None,
                    "cta_type": cta_type
                })
                st.session_state.current_step = 5
                st.rerun()

    def step_content_generation(self):
        """Étape 5: Génération du contenu"""
        st.header("🤖 Génération du contenu")
        
        # Affichage de la configuration
        platforms = st.session_state.platforms
        selected_platforms = [p for p, enabled in platforms.items() if enabled]
        
        st.info(f"""
        **Configuration actuelle:**
        - Entreprise: {st.session_state.business_info.get('company_name')}
        - Secteur: {st.session_state.business_info.get('business_sector')}
        - Plateformes: {', '.join(selected_platforms).title()}
        - Type: {st.session_state.content_preferences.get('content_type')}
        - Langue: {st.session_state.content_preferences.get('language')}
        - Mode: {st.session_state.publication_mode}
        """)
        
        if st.button("🚀 Générer le contenu", type="primary"):
            with st.spinner("🤖 Génération en cours..."):
                # Fusion des préférences
                preferences = {**st.session_state.business_info, **st.session_state.content_preferences}
                preferences['platforms'] = platforms
                
                # Adapter le style selon les plateformes
                if platforms.get("facebook") and not platforms.get("linkedin"):
                    preferences['platform_style'] = 'facebook'
                    preferences['content_style'] = 'conversational'
                elif platforms.get("linkedin") and platforms.get("facebook"):
                    preferences['platform_style'] = 'hybrid'
                    preferences['content_style'] = 'professional_friendly'
                else:
                    preferences['platform_style'] = 'linkedin'
                    preferences['content_style'] = 'professional'
                
                # Génération du contenu
                try:
                    # Utilisation d'asyncio pour la génération
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    content = loop.run_until_complete(
                        self.content_agent.generate_business_content(preferences)
                    )
                    loop.close()
                    
                    if content:
                        st.session_state.generated_content = content
                        st.success("✅ Contenu généré avec succès!")
                        
                        # Affichage du contenu généré
                        st.subheader("📝 Contenu généré:")
                        st.text_area("Contenu", content, height=200, disabled=True)
                        
                        # Boutons d'action
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("✅ Valider et continuer"):
                                st.session_state.current_step = 6
                                st.rerun()
                        with col2:
                            if st.button("🔄 Régénérer"):
                                st.session_state.generated_content = None
                                st.rerun()
                    else:
                        st.error("❌ Échec de la génération du contenu")
                        
                except Exception as e:
                    st.error(f"❌ Erreur lors de la génération: {e}")
        
        elif st.session_state.generated_content:
            st.subheader("📝 Contenu généré:")
            st.text_area("Contenu", st.session_state.generated_content, height=200, disabled=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Valider et continuer"):
                    st.session_state.current_step = 6
                    st.rerun()
            with col2:
                if st.button("🔄 Régénérer"):
                    st.session_state.generated_content = None
                    st.rerun()

    def step_content_review(self):
        """Étape 6: Review du contenu"""
        st.header("🔍 Review du contenu")
        
        if st.button("🔍 Lancer la review", type="primary"):
            with st.spinner("🔍 Review en cours..."):
                try:
                    # Fusion des préférences
                    preferences = {**st.session_state.business_info, **st.session_state.content_preferences}
                    preferences['platforms'] = st.session_state.platforms
                    
                    # Review du contenu
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    reviewed_content = loop.run_until_complete(
                        self.reviewer_agent.review_business_content(
                            st.session_state.generated_content, preferences
                        )
                    )
                    loop.close()
                    
                    if reviewed_content:
                        st.session_state.reviewed_content = reviewed_content
                        st.success("✅ Contenu reviewé avec succès!")
                        
                        # Affichage du contenu reviewé
                        st.subheader("📝 Contenu reviewé:")
                        content_text = reviewed_content.get('content', reviewed_content) if isinstance(reviewed_content, dict) else reviewed_content
                        st.text_area("Contenu reviewé", content_text, height=200, disabled=True)
                        
                        # Boutons d'action
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("✅ Valider et continuer"):
                                st.session_state.current_step = 7
                                st.rerun()
                        with col2:
                            if st.button("🔄 Régénérer"):
                                st.session_state.reviewed_content = None
                                st.rerun()
                    else:
                        st.error("❌ Échec de la review du contenu")
                        
                except Exception as e:
                    st.error(f"❌ Erreur lors de la review: {e}")
        
        elif st.session_state.reviewed_content:
            st.subheader("📝 Contenu reviewé:")
            content_text = st.session_state.reviewed_content.get('content', st.session_state.reviewed_content) if isinstance(st.session_state.reviewed_content, dict) else st.session_state.reviewed_content
            st.text_area("Contenu reviewé", content_text, height=200, disabled=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Valider et continuer"):
                    st.session_state.current_step = 7
                    st.rerun()
            with col2:
                if st.button("🔄 Régénérer"):
                    st.session_state.reviewed_content = None
                    st.rerun()

    def step_image_generation(self):
        """Étape 7: Génération d'image"""
        st.header("🎨 Génération d'image")
        
        # Options de taille d'image adaptées aux plateformes
        st.subheader("📏 Options de taille d'image")
        
        platforms = st.session_state.platforms
        image_options = []
        
        if platforms.get("linkedin"):
            image_options.extend([
                ("1200x628", "LinkedIn Post (recommandé)"),
                ("1200x1200", "Carré LinkedIn")
            ])
        
        if platforms.get("facebook"):
            image_options.extend([
                ("1200x630", "Facebook Post (recommandé)"),
                ("1080x1080", "Carré Facebook")
            ])
        
        # Options génériques
        image_options.extend([
            ("800x600", "Petit format"),
            ("1600x900", "Format large")
        ])
        
        # Supprimer les doublons
        seen = set()
        unique_options = []
        for option in image_options:
            if option[0] not in seen:
                seen.add(option[0])
                unique_options.append(option)
        
        image_size = st.selectbox(
            "Choisissez la taille de l'image:",
            unique_options,
            format_func=lambda x: x[1],
            index=0
        )
        
        selected_width, selected_height = map(int, image_size[0].split('x'))
        
        if st.button("🎨 Générer l'image", type="primary"):
            with st.spinner("🎨 Génération d'image en cours..."):
                try:
                    # Fusion des préférences
                    preferences = {**st.session_state.business_info, **st.session_state.content_preferences}
                    preferences['platforms'] = platforms
                    
                    # Génération du prompt d'image
                    content_text = st.session_state.reviewed_content.get('content', st.session_state.reviewed_content) if isinstance(st.session_state.reviewed_content, dict) else st.session_state.reviewed_content
                    prompt_image = generate_image_prompt(content_text, preferences)
                    
                    st.info(f"📌 Prompt généré: {prompt_image}")
                    st.info(f"📏 Taille sélectionnée: {selected_width}x{selected_height} pixels")
                    
                    # Génération de l'image
                    image_generator = ImageGenerator()
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    image_path = f"assets/generated_image_{timestamp}.png"
                    
                    # Génération avec la taille sélectionnée
                    image_generator.generate_image(prompt_image, output_path=image_path, num_inference_steps=20, width=selected_width, height=selected_height)
                    
                    if os.path.exists(image_path):
                        st.session_state.image_path = image_path
                        st.success("✅ Image générée avec succès!")
                        
                        # Affichage de l'image
                        st.subheader("🖼️ Image générée:")
                        image = Image.open(image_path)
                        
                        # Afficher l'image avec une taille contrôlée
                        col1, col2, col3 = st.columns([1, 2, 1])
                        with col2:
                            st.image(image, caption=f"Image générée - {image_size[1]} ({selected_width}x{selected_height})", width=400)
                        
                        # Informations sur la taille et compatibilité
                        st.info(f"📏 Taille: {image.size[0]}x{image.size[1]} pixels - {image_size[1]}")
                        
                        # Indications de compatibilité
                        if platforms.get("linkedin") and platforms.get("facebook"):
                            if selected_width == 1200 and selected_height in [628, 630]:
                                st.success("✅ Format optimal pour LinkedIn et Facebook")
                            elif selected_width == 1080 and selected_height == 1080:
                                st.success("✅ Format carré compatible avec les deux plateformes")
                        elif platforms.get("linkedin"):
                            if selected_width == 1200 and selected_height == 628:
                                st.success("✅ Format optimal pour LinkedIn")
                        elif platforms.get("facebook"):
                            if selected_width == 1200 and selected_height == 630:
                                st.success("✅ Format optimal pour Facebook")
                        
                        # Boutons d'action
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("✅ Valider et continuer"):
                                st.session_state.current_step = 8
                                st.rerun()
                        with col2:
                            if st.button("🔄 Régénérer"):
                                st.session_state.image_path = None
                                st.rerun()
                    else:
                        st.error("❌ Échec de la génération d'image")
                        
                except Exception as e:
                    st.error(f"❌ Erreur lors de la génération d'image: {e}")
        
        elif st.session_state.image_path and os.path.exists(st.session_state.image_path):
            st.subheader("🖼️ Image générée:")
            image = Image.open(st.session_state.image_path)
            
            # Afficher l'image avec une taille contrôlée
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(image, caption=f"Image générée ({image.size[0]}x{image.size[1]})", width=400)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Valider et continuer"):
                    st.session_state.current_step = 8
                    st.rerun()
            with col2:
                if st.button("🔄 Régénérer"):
                    st.session_state.image_path = None
                    st.rerun()

    def render_social_preview(self, platform, content_text, company_name):
        """Génère un aperçu réaliste pour une plateforme donnée"""
        if platform == "linkedin":
            return f"""
            <div class="linkedin-preview">
                <div class="linkedin-header">
                    <div class="linkedin-avatar">{company_name[0].upper()}</div>
                    <div class="linkedin-user-info">
                        <div class="linkedin-name">{company_name}</div>
                        <div class="linkedin-time">Maintenant</div>
                    </div>
                    <div class="linkedin-menu">⋯</div>
                </div>
                <div class="linkedin-content">
                    {content_text.replace(chr(10), '<br>')}
                </div>
                <div class="linkedin-actions">
                    <div class="linkedin-action">
                        <span class="action-icon">👍</span>
                        <span class="action-text">J'aime</span>
                    </div>
                    <div class="linkedin-action">
                        <span class="action-icon">💬</span>
                        <span class="action-text">Commenter</span>
                    </div>
                    <div class="linkedin-action">
                        <span class="action-icon">🔄</span>
                        <span class="action-text">Republier</span>
                    </div>
                    <div class="linkedin-action">
                        <span class="action-icon">📤</span>
                        <span class="action-text">Envoyer</span>
                    </div>
                </div>
            </div>
            """
        elif platform == "facebook":
            return f"""
            <div class="facebook-preview">
                <div class="facebook-header">
                    <div class="facebook-avatar">{company_name[0].upper()}</div>
                    <div class="facebook-user-info">
                        <div class="facebook-name">{company_name}</div>
                        <div class="facebook-time">Maintenant</div>
                    </div>
                </div>
                <div class="facebook-content">
                    {content_text.replace(chr(10), '<br>')}
                </div>
                <div class="facebook-actions">
                    <div class="facebook-action">
                        <span class="action-icon">👍</span>
                        <span class="action-text">J'aime</span>
                    </div>
                    <div class="facebook-action">
                        <span class="action-icon">💬</span>
                        <span class="action-text">Commenter</span>
                    </div>
                    <div class="facebook-action">
                        <span class="action-icon">📤</span>
                        <span class="action-text">Partager</span>
                    </div>
                </div>
            </div>
            """

    def step_preview(self):
        """Étape 8: Preview multi-plateformes"""
        st.header("📋 Preview Multi-Plateformes")
        
        # Récupération du contenu final
        content_text = st.session_state.reviewed_content.get('content', st.session_state.reviewed_content) if isinstance(st.session_state.reviewed_content, dict) else st.session_state.reviewed_content
        company_name = st.session_state.business_info.get('company_name', 'Votre entreprise')
        platforms = st.session_state.platforms
        
        # Preview pour chaque plateforme sélectionnée
        if platforms.get("linkedin"):
            st.subheader("💼 Aperçu LinkedIn")
            st.markdown(self.render_social_preview("linkedin", content_text, company_name), unsafe_allow_html=True)
            
        if platforms.get("facebook"):
            st.subheader("📘 Aperçu Facebook")
            st.markdown(self.render_social_preview("facebook", content_text, company_name), unsafe_allow_html=True)
        
        # Affichage de l'image si elle existe
        if st.session_state.image_path and os.path.exists(st.session_state.image_path):
            st.subheader("🖼️ Image du post")
            image = Image.open(st.session_state.image_path)
            
            # Afficher l'image avec une taille contrôlée
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(image, caption=f"Image optimisée ({image.size[0]}x{image.size[1]})", width=400)
            
            # Indications de compatibilité
            width, height = image.size
            compatibility_info = []
            
            if platforms.get("linkedin"):
                if width == 1200 and height == 628:
                    compatibility_info.append("✅ Optimal pour LinkedIn")
                elif width == 1200 and height == 1200:
                    compatibility_info.append("✅ Carré LinkedIn")
                else:
                    compatibility_info.append("⚠️ Non optimal pour LinkedIn")
                    
            if platforms.get("facebook"):
                if width == 1200 and height == 630:
                    compatibility_info.append("✅ Optimal pour Facebook")
                elif width == 1080 and height == 1080:
                    compatibility_info.append("✅ Carré Facebook")
                else:
                    compatibility_info.append("⚠️ Non optimal pour Facebook")
            
            if compatibility_info:
                st.info(" | ".join(compatibility_info))
        
        # Boutons d'action
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Valider et publier", type="primary"):
                st.session_state.current_step = 9
                st.rerun()
        with col2:
            if st.button("🔄 Retour à la génération"):
                st.session_state.current_step = 5
                st.rerun()

    def step_schedule_selection(self):
        """Étape pour sélectionner la date/heure de publication programmée"""
        st.header("⏰ Programmation de la publication")
        
        col1, col2 = st.columns(2)
        
        with col1:
            schedule_date = st.date_input(
                "📅 Date de publication",
                value=datetime.now().date() + timedelta(days=1),
                min_value=datetime.now().date()
            )
        
        with col2:
            schedule_time = st.time_input(
                "🕒 Heure de publication",
                value=datetime.now().time().replace(second=0, microsecond=0)
            )
        
        # Combiner date et heure
        schedule_datetime = datetime.combine(schedule_date, schedule_time)
        
        st.info(f"📅 Publication programmée pour: {schedule_datetime.strftime('%d/%m/%Y à %H:%M')}")
        
        # Vérifier que la date est dans le futur
        if schedule_datetime <= datetime.now():
            st.error("❌ La date de publication doit être dans le futur")
            return
        
        # Boutons d'action
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Programmer la publication", type="primary"):
                st.session_state.schedule_datetime = schedule_datetime
                st.session_state.current_step = 9
                st.rerun()
        with col2:
            if st.button("🔄 Retour au preview"):
                st.session_state.current_step = 8
                st.rerun()

    def step_publication(self):
        """Étape 9: Publication multi-plateformes"""
        st.header("📤 Publication Multi-Plateformes")
        
        platforms = st.session_state.platforms
        selected_platforms = [p for p, enabled in platforms.items() if enabled]
        
        # Affichage du mode de publication
        if st.session_state.publication_mode == "scheduled" and st.session_state.schedule_datetime:
            st.info(f"⏰ Mode: Publication programmée pour {st.session_state.schedule_datetime.strftime('%d/%m/%Y à %H:%M')}")
            
            # Permettre la modification de l'heure
            if st.button("🕒 Modifier l'heure de publication"):
                st.session_state.current_step = 8.5  # Étape intermédiaire pour la programmation
                st.rerun()
        else:
            st.info("🚀 Mode: Publication immédiate")
        
        # Configuration des plateformes
        st.subheader("🔐 Configuration des plateformes")
        
        # Vérification LinkedIn
        if platforms.get("linkedin"):
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.session_state.linkedin_token:
                    st.success("✅ LinkedIn configuré - Prêt pour publication")
                else:
                    st.warning("⚠️ LinkedIn non configuré")
            with col2:
                if not st.session_state.linkedin_token:
                    if st.button("🔐 Config LinkedIn"):
                        try:
                            token = self.linkedin_auth.authenticate()
                            if token:
                                st.session_state.linkedin_token = token
                                st.success("✅ LinkedIn configuré!")
                                st.rerun()
                        except Exception as e:
                            st.error(f"❌ Erreur: {e}")
        
        # Vérification Facebook
        if platforms.get("facebook"):
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.session_state.facebook_token:
                    st.success("✅ Facebook configuré - Prêt pour publication")
                else:
                    st.warning("⚠️ Facebook non configuré")
            with col2:
                if not st.session_state.facebook_token:
                    if st.button("🔐 Config Facebook"):
                        try:
                            token = self.facebook_auth.authenticate()
                            if token:
                                st.session_state.facebook_token = token
                                st.success("✅ Facebook configuré!")
                                st.rerun()
                        except Exception as e:
                            st.error(f"❌ Erreur: {e}")
        
        st.markdown("---")
        
        # Options de publication
        st.subheader("📤 Options de publication")
        
        # Récupération du contenu
        content_text = st.session_state.reviewed_content.get('content', st.session_state.reviewed_content) if isinstance(st.session_state.reviewed_content, dict) else st.session_state.reviewed_content
        preferences = {**st.session_state.business_info, **st.session_state.content_preferences}
        preferences['platforms'] = platforms
        
        # Ajouter les tokens
        if st.session_state.linkedin_token:
            preferences['linkedin_token'] = st.session_state.linkedin_token
        if st.session_state.facebook_token:
            preferences['facebook_token'] = st.session_state.facebook_token
        
        # Boutons de publication
        publication_ready = False
        
        if platforms.get("linkedin") and platforms.get("facebook"):
            # Publication sur les deux plateformes
            if st.session_state.linkedin_token and st.session_state.facebook_token:
                publication_ready = True
                if st.button("🚀 Publier sur LinkedIn + Facebook", type="primary"):
                    self.publish_to_platforms(content_text, preferences, ["linkedin", "facebook"])
            else:
                st.error("❌ Configuration requise pour les deux plateformes")
        
        elif platforms.get("linkedin"):
            # Publication LinkedIn uniquement
            if st.session_state.linkedin_token:
                publication_ready = True
                if st.button("💼 Publier sur LinkedIn", type="primary"):
                    self.publish_to_platforms(content_text, preferences, ["linkedin"])
            else:
                st.error("❌ Configuration LinkedIn requise")
        
        elif platforms.get("facebook"):
            # Publication Facebook uniquement
            if st.session_state.facebook_token:
                publication_ready = True
                if st.button("📘 Publier sur Facebook", type="primary"):
                    self.publish_to_platforms(content_text, preferences, ["facebook"])
            else:
                st.error("❌ Configuration Facebook requise")
        
        # Option de sauvegarde si pas de publication possible
        if not publication_ready:
            st.markdown("---")
            st.info("💡 Pas de problème ! Vous pouvez sauvegarder le contenu pour publication manuelle")
            
            if st.button("💾 Sauvegarder le contenu", type="secondary"):
                self.save_content_locally(content_text, preferences)
        
        # Test des connexions
        st.markdown("---")
        st.subheader("🧪 Tests de connexion")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if platforms.get("linkedin") and st.button("🧪 Tester LinkedIn"):
                self.test_platform_connection("linkedin")
        
        with col2:
            if platforms.get("facebook") and st.button("🧪 Tester Facebook"):
                self.test_platform_connection("facebook")

    def publish_to_platforms(self, content_text, preferences, target_platforms):
        """Publie le contenu sur les plateformes sélectionnées"""
        results = {}
        
        with st.spinner(f"📤 Publication sur {', '.join(target_platforms).title()}..."):
            try:
                for platform in target_platforms:
                    st.info(f"🚀 Publication sur {platform.title()}...")
                    
                    if platform == "linkedin":
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        
                        if st.session_state.publication_mode == "scheduled":
                            # Publication programmée
                            result = loop.run_until_complete(
                                self.scheduler.schedule_linkedin_post(
                                    content_text,
                                    preferences,
                                    st.session_state.schedule_datetime,
                                    image_path=st.session_state.image_path
                                )
                            )
                        else:
                            # Publication immédiate
                            result = loop.run_until_complete(
                                self.posting_agent.post_to_linkedin_real(
                                    content_text, 
                                    preferences, 
                                    image_path=st.session_state.image_path
                                )
                            )
                        loop.close()
                        results["linkedin"] = result
                    
                    elif platform == "facebook":
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        
                        if st.session_state.publication_mode == "scheduled":
                            # Publication programmée
                            result = loop.run_until_complete(
                                self.scheduler.schedule_facebook_post(
                                    content_text,
                                    preferences,
                                    st.session_state.schedule_datetime,
                                    image_path=st.session_state.image_path
                                )
                            )
                        else:
                            # Publication immédiate
                            result = loop.run_until_complete(
                                self.posting_agent.post_to_facebook_real(
                                    content_text, 
                                    preferences, 
                                    image_path=st.session_state.image_path
                                )
                            )
                        loop.close()
                        results["facebook"] = result
                
                # Affichage des résultats
                success_count = 0
                for platform, result in results.items():
                    if result:
                        st.success(f"✅ {platform.title()} : Publication réussie!")
                        if isinstance(result, dict) and 'post_url' in result:
                            st.info(f"🔗 Lien {platform.title()}: {result['post_url']}")
                        success_count += 1
                    else:
                        st.error(f"❌ {platform.title()} : Échec de la publication")
                
                if success_count == len(target_platforms):
                    st.balloons()
                    st.success(f"🎉 Publication réussie sur toutes les plateformes ({success_count}/{len(target_platforms)})!")
                elif success_count > 0:
                    st.warning(f"⚠️ Publication partielle ({success_count}/{len(target_platforms)} plateformes)")
                else:
                    st.error("❌ Échec de toutes les publications")
                
                # Bouton pour recommencer
                if st.button("🔄 Créer un nouveau post"):
                    self.reset_session()
                    
            except Exception as e:
                st.error(f"❌ Erreur lors de la publication: {e}")

    def save_content_locally(self, content_text, preferences):
        """Sauvegarde le contenu localement"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Créer le dossier si nécessaire
            os.makedirs("data/posted_content", exist_ok=True)
            
            # Préparer les données
            content_data = {
                "timestamp": timestamp,
                "content": content_text,
                "image_path": st.session_state.image_path,
                "preferences": preferences,
                "platforms": st.session_state.platforms,
                "publication_mode": st.session_state.publication_mode,
                "schedule_datetime": st.session_state.schedule_datetime.isoformat() if st.session_state.schedule_datetime else None,
                "status": "ready_for_manual_posting"
            }
            
            filename = f"data/posted_content/offline_content_{timestamp}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(content_data, f, ensure_ascii=False, indent=2)
            
            st.success("✅ Contenu sauvegardé avec succès!")
            st.info(f"📁 Fichier: {filename}")
            
            if st.session_state.image_path and os.path.exists(st.session_state.image_path):
                st.info(f"🖼️ Image: {st.session_state.image_path}")
            
            # Bouton pour recommencer
            if st.button("🔄 Créer un nouveau post"):
                self.reset_session()
                
        except Exception as e:
            st.error(f"❌ Erreur lors de la sauvegarde: {e}")

    def test_platform_connection(self, platform):
        """Test la connexion à une plateforme"""
        try:
            if platform == "linkedin" and st.session_state.linkedin_token:
                headers = {
                    'Authorization': f'Bearer {st.session_state.linkedin_token}',
                    'Content-Type': 'application/json'
                }
                
                response = requests.get('https://api.linkedin.com/v2/me', headers=headers)
                
                if response.status_code == 200:
                    profile_data = response.json()
                    st.success("✅ LinkedIn : Connexion réussie!")
                    st.info(f"👤 Connecté en tant que: {profile_data.get('localizedFirstName', '')} {profile_data.get('localizedLastName', '')}")
                else:
                    st.error(f"❌ LinkedIn : Erreur {response.status_code}")
            
            elif platform == "facebook" and st.session_state.facebook_token:
                # Test simple de l'API Facebook
                response = requests.get(
                    'https://graph.facebook.com/me',
                    params={'access_token': st.session_state.facebook_token}
                )
                
                if response.status_code == 200:
                    profile_data = response.json()
                    st.success("✅ Facebook : Connexion réussie!")
                    st.info(f"👤 Connecté en tant que: {profile_data.get('name', 'Utilisateur')}")
                else:
                    st.error(f"❌ Facebook : Erreur {response.status_code}")
            
            else:
                st.warning(f"⚠️ {platform.title()} : Token non configuré")
                
        except Exception as e:
            st.error(f"❌ Erreur lors du test {platform}: {e}")

    def reset_session(self):
        """Remet à zéro la session pour recommencer"""
        keys_to_reset = [
            'current_step', 'publication_mode', 'platforms', 'business_info', 
            'content_preferences', 'generated_content', 'reviewed_content', 
            'image_path', 'schedule_datetime'
        ]
        
        for key in keys_to_reset:
            if key in st.session_state:
                del st.session_state[key]
        
        st.session_state.current_step = 1
        st.rerun()

    def render_sidebar(self):
        """Affiche la barre latérale avec les informations de session"""
        with st.sidebar:
            st.header("📊 Session Info")
            
            # Étape actuelle
            st.info(f"Étape: {st.session_state.current_step}/9")
            
            # Mode de publication
            if hasattr(st.session_state, 'publication_mode') and st.session_state.publication_mode:
                mode_icon = "🚀" if st.session_state.publication_mode == "immediate" else "⏰"
                st.info(f"{mode_icon} Mode: {st.session_state.publication_mode}")
            
            # Plateformes sélectionnées
            if hasattr(st.session_state, 'platforms') and st.session_state.platforms:
                platforms = st.session_state.platforms
                selected = [p for p, enabled in platforms.items() if enabled]
                if selected:
                    st.info(f"🌐 Plateformes: {', '.join(selected).title()}")
            
            # Configuration business
            if hasattr(st.session_state, 'business_info') and st.session_state.business_info.get('company_name'):
                st.info(f"🏢 Entreprise: {st.session_state.business_info['company_name']}")
            
            # Statuts des tokens
            st.subheader("🔐 Connexions")
            if st.session_state.linkedin_token:
                st.success("✅ LinkedIn")
            else:
                st.error("❌ LinkedIn")
                
            if st.session_state.facebook_token:
                st.success("✅ Facebook")
            else:
                st.error("❌ Facebook")
            
            # Bouton de reset
            st.markdown("---")
            if st.button("🔄 Recommencer", use_container_width=True):
                self.reset_session()

    def run(self):
        """Exécute l'application Streamlit"""
        self.render_header()
        self.render_sidebar()
        self.render_steps_progress()
        
        # Navigation entre les étapes
        if st.session_state.current_step == 1:
            self.step_publication_mode()
        elif st.session_state.current_step == 2:
            self.step_platform_selection()
        elif st.session_state.current_step == 3:
            self.step_business_config()
        elif st.session_state.current_step == 4:
            self.step_content_preferences()
        elif st.session_state.current_step == 5:
            self.step_content_generation()
        elif st.session_state.current_step == 6:
            self.step_content_review()
        elif st.session_state.current_step == 7:
            self.step_image_generation()
        elif st.session_state.current_step == 8:
            self.step_preview()
        elif st.session_state.current_step == 8.5:
            self.step_schedule_selection()
        elif st.session_state.current_step == 9:
            self.step_publication()

    def test_platform_connection(self, platform):
        """Test la connexion à une plateforme"""
        try:
            if platform == "linkedin" and st.session_state.linkedin_token:
                headers = {
                    'Authorization': f'Bearer {st.session_state.linkedin_token}',
                    'Content-Type': 'application/json'
                }
                
                response = requests.get('https://api.linkedin.com/v2/me', headers=headers)
                
                if response.status_code == 200:
                    profile_data = response.json()
                    st.success("✅ LinkedIn : Connexion réussie!")
                    st.info(f"👤 Connecté en tant que: {profile_data.get('localizedFirstName', '')} {profile_data.get('localizedLastName', '')}")
                else:
                    st.error(f"❌ LinkedIn : Erreur {response.status_code}")
            
            elif platform == "facebook" and st.session_state.facebook_token:
                # Test simple de l'API Facebook
                response = requests.get(
                    'https://graph.facebook.com/me',
                    params={'access_token': st.session_state.facebook_token}
                )
                
                if response.status_code == 200:
                    profile_data = response.json()
                    st.success("✅ Facebook : Connexion réussie!")
                    st.info(f"👤 Connecté en tant que: {profile_data.get('name', 'Utilisateur')}")
                else:
                    st.error(f"❌ Facebook : Erreur {response.status_code}")
            
            else:
                st.warning(f"⚠️ {platform.title()} : Token non configuré")
                
        except Exception as e:
            st.error(f"❌ Erreur lors du test {platform}: {e}")

    def save_content_locally(self, content_text, preferences):
        """Sauvegarde le contenu localement"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Créer le dossier si nécessaire
            os.makedirs("data/posted_content", exist_ok=True)
            
            # Préparer les données
            content_data = {
                "timestamp": timestamp,
                "content": content_text,
                "image_path": st.session_state.image_path,
                "preferences": preferences,
                "platforms": st.session_state.platforms,
                "publication_mode": st.session_state.publication_mode,
                "schedule_datetime": st.session_state.schedule_datetime.isoformat() if st.session_state.schedule_datetime else None,
                "status": "ready_for_manual_posting"
            }
            
            filename = f"data/posted_content/offline_content_{timestamp}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(content_data, f, ensure_ascii=False, indent=2)
            
            st.success("✅ Contenu sauvegardé avec succès!")
            st.info(f"📁 Fichier: {filename}")
            
            if st.session_state.image_path and os.path.exists(st.session_state.image_path):
                st.info(f"🖼️ Image: {st.session_state.image_path}")
            
            # Bouton pour recommencer
            if st.button("🔄 Créer un nouveau post"):
                self.reset_session()
                
        except Exception as e:
            st.error(f"❌ Erreur lors de la sauvegarde: {e}")

    def publish_to_platforms(self, content_text, preferences, target_platforms):
        """Publie le contenu sur les plateformes sélectionnées"""
        results = {}
        
        with st.spinner(f"📤 Publication sur {', '.join(target_platforms).title()}..."):
            try:
                for platform in target_platforms:
                    st.info(f"🚀 Publication sur {platform.title()}...")
                    
                    if platform == "linkedin":
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        
                        if st.session_state.publication_mode == "scheduled":
                            # Publication programmée
                            result = loop.run_until_complete(
                                self.scheduler.schedule_linkedin_post(
                                    content_text,
                                    preferences,
                                    st.session_state.schedule_datetime,
                                    image_path=st.session_state.image_path
                                )
                            )
                        else:
                            # Publication immédiate
                            result = loop.run_until_complete(
                                self.posting_agent.post_to_linkedin_real(
                                    content_text, 
                                    preferences, 
                                    image_path=st.session_state.image_path
                                )
                            )
                        loop.close()
                        results["linkedin"] = result
                    
                    elif platform == "facebook":
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        
                        if st.session_state.publication_mode == "scheduled":
                            # Publication programmée
                            result = loop.run_until_complete(
                                self.scheduler.schedule_facebook_post(
                                    content_text,
                                    preferences,
                                    st.session_state.schedule_datetime,
                                    image_path=st.session_state.image_path
                                )
                            )
                        else:
                            # Publication immédiate
                            result = loop.run_until_complete(
                                self.posting_agent.post_to_facebook_real(
                                    content_text, 
                                    preferences, 
                                    image_path=st.session_state.image_path
                                )
                            )
                        loop.close()
                        results["facebook"] = result
                
                # Affichage des résultats
                success_count = 0
                for platform, result in results.items():
                    if result:
                        st.success(f"✅ {platform.title()} : Publication réussie!")
                        if isinstance(result, dict) and 'post_url' in result:
                            st.info(f"🔗 Lien {platform.title()}: {result['post_url']}")
                        success_count += 1
                    else:
                        st.error(f"❌ {platform.title()} : Échec de la publication")
                
                if success_count == len(target_platforms):
                    st.balloons()
                    st.success(f"🎉 Publication réussie sur toutes les plateformes ({success_count}/{len(target_platforms)})!")
                elif success_count > 0:
                    st.warning(f"⚠️ Publication partielle ({success_count}/{len(target_platforms)} plateformes)")
                else:
                    st.error("❌ Échec de toutes les publications")
                
                # Bouton pour recommencer
                if st.button("🔄 Créer un nouveau post"):
                    self.reset_session()
                    
            except Exception as e:
                st.error(f"❌ Erreur lors de la publication: {e}")

    def reset_session(self):
        """Remet à zéro la session pour recommencer"""
        keys_to_reset = [
            'current_step', 'publication_mode', 'platforms', 'business_info', 
            'content_preferences', 'generated_content', 'reviewed_content', 
            'image_path', 'schedule_datetime'
        ]
        
        for key in keys_to_reset:
            if key in st.session_state:
                del st.session_state[key]
        
        # Réinitialiser les valeurs par défaut
        st.session_state.current_step = 1
        st.session_state.business_info = {
            "company_name": "",
            "business_sector": "technology",
            "target_audience": "professionals",
            "company_size": "medium"
        }
        st.session_state.content_preferences = {
            "language": "fr",
            "content_type": "thought_leadership",
            "topic": "",
            "cta_type": "engagement"
        }
        st.rerun()

    def render_sidebar(self):
        """Affiche la barre latérale avec les informations de session"""
        with st.sidebar:
            st.header("📊 Session Info")
            
            # Étape actuelle
            st.info(f"Étape: {st.session_state.current_step}/9")
            
            # Mode de publication
            if hasattr(st.session_state, 'publication_mode') and st.session_state.publication_mode:
                mode_icon = "🚀" if st.session_state.publication_mode == "immediate" else "⏰"
                mode_label = "Immédiate" if st.session_state.publication_mode == "immediate" else "Programmée"
                st.info(f"{mode_icon} Mode: {mode_label}")
            
            # Plateformes sélectionnées
            if hasattr(st.session_state, 'platforms') and st.session_state.platforms:
                platforms = st.session_state.platforms
                selected = [p for p, enabled in platforms.items() if enabled]
                if selected:
                    platform_icons = {"linkedin": "💼", "facebook": "📘"}
                    platform_list = [f"{platform_icons.get(p, '🌐')} {p.title()}" for p in selected]
                    st.info("🌐 Plateformes:\n" + "\n".join(platform_list))
            
            # Configuration business
            if hasattr(st.session_state, 'business_info') and st.session_state.business_info.get('company_name'):
                st.info(f"🏢 Entreprise: {st.session_state.business_info['company_name']}")
                st.info(f"🏭 Secteur: {st.session_state.business_info.get('business_sector', 'N/A')}")
            
            # Préférences de contenu
            if hasattr(st.session_state, 'content_preferences') and st.session_state.content_preferences:
                prefs = st.session_state.content_preferences
                if prefs.get('content_type'):
                    content_type_labels = {
                        "thought_leadership": "Leadership",
                        "company_update": "Actualités",
                        "industry_insight": "Insights",
                        "product_showcase": "Produit",
                        "team_culture": "Culture",
                        "educational": "Éducatif",
                        "promotional": "Promotionnel",
                        "community_event": "Événement"
                    }
                    st.info(f"📈 Type: {content_type_labels.get(prefs['content_type'], prefs['content_type'])}")
                
                if prefs.get('language'):
                    lang_label = "🇫🇷 Français" if prefs['language'] == 'fr' else "🇺🇸 Anglais"
                    st.info(f"🌐 Langue: {lang_label}")
            
            # Statuts des connexions
            st.subheader("🔐 Connexions")
            
            # LinkedIn
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.session_state.linkedin_token:
                    st.success("✅ LinkedIn")
                else:
                    st.error("❌ LinkedIn")
            with col2:
                if st.button("🧪", key="test_linkedin_sidebar", help="Tester LinkedIn"):
                    self.test_platform_connection("linkedin")
            
            # Facebook
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.session_state.facebook_token:
                    st.success("✅ Facebook")
                else:
                    st.error("❌ Facebook")
            with col2:
                if st.button("🧪", key="test_facebook_sidebar", help="Tester Facebook"):
                    self.test_platform_connection("facebook")
            
            # Statut du contenu
            if st.session_state.current_step > 5:
                st.subheader("📝 Contenu")
                if st.session_state.generated_content:
                    st.success("✅ Contenu généré")
                if st.session_state.reviewed_content:
                    st.success("✅ Contenu reviewé")
                if st.session_state.image_path and os.path.exists(st.session_state.image_path):
                    st.success("✅ Image générée")
            
            # Programmation
            if st.session_state.publication_mode == "scheduled" and hasattr(st.session_state, 'schedule_datetime') and st.session_state.schedule_datetime:
                st.subheader("⏰ Programmation")
                st.info(f"📅 {st.session_state.schedule_datetime.strftime('%d/%m/%Y')}")
                st.info(f"🕒 {st.session_state.schedule_datetime.strftime('%H:%M')}")
            
            # Actions rapides
            st.markdown("---")
            st.subheader("⚡ Actions")
            
            # Bouton de reset
            if st.button("🔄 Recommencer", use_container_width=True, type="secondary"):
                self.reset_session()
            
            # Navigation rapide (si applicable)
            if st.session_state.current_step > 3:
                st.markdown("**🚀 Navigation rapide:**")
                if st.button("📝 Retour génération", key="quick_nav_gen"):
                    st.session_state.current_step = 5
                    st.rerun()
                
                if st.session_state.current_step > 6 and st.button("🎨 Retour image", key="quick_nav_img"):
                    st.session_state.current_step = 7
                    st.rerun()

# Point d'entrée de l'application
if __name__ == "__main__":
    app = StreamlitContentEngine()
    app.run()