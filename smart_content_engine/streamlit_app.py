# ============================================================================
# 📄 streamlit_app.py - Interface Streamlit pour Smart Content Engine
# ============================================================================
import streamlit as st
import asyncio
import json
import os
from datetime import datetime
from PIL import Image
import time
from dotenv import load_dotenv

# Import des modules existants
from agents.content_agent import ContentAgent
from agents.reviewer_agent import ReviewerAgent
from agents.posting_agent import PostingAgent
from agents.agent_image_prompt import generate_image_prompt
from core.image_generator import ImageGenerator
from linkedin_auth import LinkedInAuth

# Chargement des variables d'environnement
load_dotenv()

# Configuration de la page
st.set_page_config(
    page_title="Smart Content Engine - LinkedIn",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "Smart Content Engine - Interface de création de contenu LinkedIn"
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

.action-icon {
    font-size: 16px;
    margin-right: 6px;
}

.action-text {
    font-size: 12px;
    color: #666666;
    font-weight: 500;
}

.linkedin-image {
    border-radius: 8px;
    margin: 15px 0;
    max-width: 100%;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
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

/* Amélioration des selectbox */
[data-testid="stSelectbox"] {
    border-radius: 6px;
}

/* Amélioration des text_input */
[data-testid="stTextInput"] {
    border-radius: 6px;
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
    background-color: #0077b5;
}
</style>
""", unsafe_allow_html=True)

class StreamlitContentEngine:
    def __init__(self):
        self.content_agent = ContentAgent()
        self.reviewer_agent = ReviewerAgent()
        self.posting_agent = PostingAgent()
        self.linkedin_auth = LinkedInAuth()
        
        # Initialisation des variables de session
        if 'current_step' not in st.session_state:
            st.session_state.current_step = 1
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
        if 'linkedin_token' not in st.session_state:
            # Charger automatiquement le token sauvegardé
            saved_token = self.linkedin_auth.load_saved_token()
            if saved_token:
                st.session_state.linkedin_token = saved_token
            else:
                st.session_state.linkedin_token = None

    def render_header(self):
        """Affiche l'en-tête de l'application"""
        st.title("🚀 Smart Content Engine - LinkedIn")
        st.markdown("### Création de contenu business intelligent")
        
        # Notification si un token LinkedIn est chargé
        if st.session_state.linkedin_token:
            st.success("🔗 Token LinkedIn chargé automatiquement - Publication disponible !")
        
        st.markdown("---")

    def render_steps_progress(self):
        """Affiche la barre de progression des étapes"""
        steps = [
            "🏢 Configuration Business",
            "📝 Préférences Contenu", 
            "🤖 Génération Contenu",
            "🔍 Review Contenu",
            "🎨 Génération Image",
            "📋 Preview LinkedIn",
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

    def step_business_config(self):
        """Étape 1: Configuration business"""
        st.header("🏢 Configuration de votre business")
        
        # Initialiser les valeurs par défaut
        if 'business_info' not in st.session_state:
            st.session_state.business_info = {
                "company_name": "",
                "business_sector": "technology",
                "target_audience": "professionals",
                "company_size": "medium"
            }
        
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
                target_audience = st.selectbox(
                    "🎯 Audience cible",
                    ["professionals", "entrepreneurs", "executives", "managers", "consultants", "freelancers"],
                    index=["professionals", "entrepreneurs", "executives", "managers", "consultants", "freelancers"].index(
                              st.session_state.business_info.get('target_audience', 'professionals')),
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
                st.session_state.current_step = 2
                st.rerun()
            elif submitted and not company_name:
                st.error("❌ Le nom de l'entreprise est requis!")

    def step_content_preferences(self):
        """Étape 2: Préférences de contenu"""
        st.header("📝 Préférences de contenu")
        
        # Initialiser les valeurs par défaut
        if 'content_preferences' not in st.session_state:
            st.session_state.content_preferences = {
                "language": "fr",
                "content_type": "thought_leadership",
                "topic": "",
                "cta_type": "engagement"
            }
        
        with st.form("content_preferences_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                language = st.selectbox(
                    "🌐 Langue du contenu",
                    ["fr", "en"],
                    index=0 if st.session_state.content_preferences.get('language') == 'fr' else 1,
                    key="lang_select"
                )
                
                content_type = st.selectbox(
                    "📈 Type de contenu",
                    ["thought_leadership", "company_update", "industry_insight", 
                     "product_showcase", "team_culture", "educational"],
                    index=["thought_leadership", "company_update", "industry_insight", 
                           "product_showcase", "team_culture", "educational"].index(
                               st.session_state.content_preferences.get('content_type', 'thought_leadership')),
                    key="content_type_select"
                )
            
            with col2:
                topic = st.text_input("💡 Sujet spécifique (optionnel)", 
                                    value=st.session_state.content_preferences.get('topic', ''),
                                    key="topic_input")
                
                cta_type = st.selectbox(
                    "🎯 Objectif du post",
                    ["engagement", "traffic", "lead_gen", "networking", "education"],
                    index=["engagement", "traffic", "lead_gen", "networking", "education"].index(
                               st.session_state.content_preferences.get('cta_type', 'engagement')),
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
                st.session_state.current_step = 3
                st.rerun()

    def step_content_generation(self):
        """Étape 3: Génération du contenu"""
        st.header("🤖 Génération du contenu")
        
        # Affichage de la configuration
        st.info(f"""
        **Configuration actuelle:**
        - Entreprise: {st.session_state.business_info.get('company_name')}
        - Secteur: {st.session_state.business_info.get('business_sector')}
        - Type: {st.session_state.content_preferences.get('content_type')}
        - Langue: {st.session_state.content_preferences.get('language')}
        """)
        
        if st.button("🚀 Générer le contenu", type="primary"):
            with st.spinner("🤖 Génération en cours..."):
                # Fusion des préférences
                preferences = {**st.session_state.business_info, **st.session_state.content_preferences}
                
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
                                st.session_state.current_step = 4
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
                    st.session_state.current_step = 4
                    st.rerun()
            with col2:
                if st.button("🔄 Régénérer"):
                    st.session_state.generated_content = None
                    st.rerun()

    def step_content_review(self):
        """Étape 4: Review du contenu"""
        st.header("🔍 Review du contenu")
        
        if st.button("🔍 Lancer la review", type="primary"):
            with st.spinner("🔍 Review en cours..."):
                try:
                    # Fusion des préférences
                    preferences = {**st.session_state.business_info, **st.session_state.content_preferences}
                    
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
                                st.session_state.current_step = 5
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
                    st.session_state.current_step = 5
                    st.rerun()
            with col2:
                if st.button("🔄 Régénérer"):
                    st.session_state.reviewed_content = None
                    st.rerun()

    def step_image_generation(self):
        """Étape 5: Génération d'image"""
        st.header("🎨 Génération d'image")
        
        # Options de taille d'image
        st.subheader("📏 Options de taille d'image")
        
        image_size = st.selectbox(
            "Choisissez la taille de l'image:",
            [
                ("1200x628", "LinkedIn Post (recommandé)"),
                ("1080x1080", "Carré Instagram"),
                ("1200x1200", "Carré LinkedIn"),
                ("800x600", "Petit format"),
                ("1600x900", "Format large")
            ],
            format_func=lambda x: x[1],
            index=0
        )
        
        selected_width, selected_height = map(int, image_size[0].split('x'))
        
        if st.button("🎨 Générer l'image", type="primary"):
            with st.spinner("🎨 Génération d'image en cours..."):
                try:
                    # Fusion des préférences
                    preferences = {**st.session_state.business_info, **st.session_state.content_preferences}
                    
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
                        
                        # Déterminer le format selon la taille
                        if selected_width == 1200 and selected_height == 628:
                            format_name = "LinkedIn Post (recommandé)"
                        elif selected_width == 1080 and selected_height == 1080:
                            format_name = "Carré Instagram"
                        elif selected_width == 1200 and selected_height == 1200:
                            format_name = "Carré LinkedIn"
                        else:
                            format_name = "Format personnalisé"
                        
                        # Afficher l'image avec une taille contrôlée
                        col1, col2, col3 = st.columns([1, 2, 1])
                        with col2:
                            st.image(image, caption=f"Image générée - {format_name} ({selected_width}x{selected_height})", width=400)
                        
                        # Informations sur la taille
                        st.info(f"📏 Taille: {image.size[0]}x{image.size[1]} pixels - {format_name}")
                        
                        # Boutons d'action
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("✅ Valider et continuer"):
                                st.session_state.current_step = 6
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
            
            # Déterminer le format selon la taille de l'image existante
            width, height = image.size
            if width == 1200 and height == 628:
                format_name = "LinkedIn Post (recommandé)"
            elif width == 1080 and height == 1080:
                format_name = "Carré Instagram"
            elif width == 1200 and height == 1200:
                format_name = "Carré LinkedIn"
            else:
                format_name = "Format personnalisé"
            
            # Afficher l'image avec une taille contrôlée
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(image, caption=f"Image générée - {format_name} ({width}x{height})", width=400)
            st.info(f"📏 Taille: {width}x{height} pixels - {format_name}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Valider et continuer"):
                    st.session_state.current_step = 6
                    st.rerun()
            with col2:
                if st.button("🔄 Régénérer"):
                    st.session_state.image_path = None
                    st.rerun()

    def step_linkedin_preview(self):
        """Étape 6: Preview LinkedIn"""
        st.header("📋 Preview LinkedIn")
        
        # Récupération du contenu final
        content_text = st.session_state.reviewed_content.get('content', st.session_state.reviewed_content) if isinstance(st.session_state.reviewed_content, dict) else st.session_state.reviewed_content
        
        # Preview LinkedIn réaliste
        st.markdown("""
        <div class="linkedin-preview">
            <div class="linkedin-header">
                <div class="linkedin-avatar">""" + st.session_state.business_info.get('company_name', 'A')[0].upper() + """</div>
                <div class="linkedin-user-info">
                    <div class="linkedin-name">""" + st.session_state.business_info.get('company_name', 'Votre entreprise') + """</div>
                    <div class="linkedin-time">Maintenant</div>
                </div>
                <div class="linkedin-menu">⋯</div>
            </div>
            <div class="linkedin-content">
                """ + content_text.replace('\n', '<br>') + """
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
        """, unsafe_allow_html=True)
        
        # Affichage de l'image si elle existe
        if st.session_state.image_path and os.path.exists(st.session_state.image_path):
            image = Image.open(st.session_state.image_path)
            # Afficher l'image avec une taille contrôlée
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(image, caption="Image du post LinkedIn", width=400)
            st.info(f"📏 Image optimisée pour LinkedIn: {image.size[0]}x{image.size[1]} pixels")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Boutons d'action
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Valider et continuer", type="primary"):
                st.session_state.current_step = 7
                st.rerun()
        with col2:
            if st.button("🔄 Retour à la génération"):
                st.session_state.current_step = 3
                st.rerun()

    def step_publication(self):
        """Étape 7: Publication LinkedIn"""
        st.header("📤 Publication LinkedIn")
        
        # Configuration LinkedIn
        st.subheader("🔐 Configuration LinkedIn")
        
        # Vérifier les clés LinkedIn
        client_id = os.getenv('LINKEDIN_CLIENT_ID')
        client_secret = os.getenv('LINKEDIN_CLIENT_SECRET')
        access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
        
        # Affichage du statut des clés
        col1, col2, col3 = st.columns(3)
        with col1:
            if client_id and client_id != "your_linkedin_client_id" and len(client_id) > 5:
                st.success("✅ Client ID configuré")
            else:
                st.error("❌ Client ID manquant ou invalide")
        
        with col2:
            if client_secret and client_secret != "your_linkedin_client_secret" and len(client_secret) > 5:
                st.success("✅ Client Secret configuré")
            else:
                st.error("❌ Client Secret manquant ou invalide")
        
        with col3:
            # Vérifier d'abord le token dans .env
            if access_token and access_token != "your_linkedin_token_here" and len(access_token) > 10:
                st.success("✅ Access Token configuré (.env)")
                st.session_state.linkedin_token = access_token
            else:
                # Vérifier s'il y a un token sauvegardé
                saved_token = self.linkedin_auth.load_saved_token()
                if saved_token:
                    st.success("✅ Access Token trouvé (fichier sauvegardé)")
                    st.session_state.linkedin_token = saved_token
                else:
                    st.warning("⚠️ Access Token manquant")
        
        # Options de publication
        st.subheader("📤 Options de publication")
        
        # Option 1: Publication LinkedIn
        if st.session_state.linkedin_token:
            st.success("✅ LinkedIn configuré - Publication disponible")
            
            # Récupération du contenu final
            content_text = st.session_state.reviewed_content.get('content', st.session_state.reviewed_content) if isinstance(st.session_state.reviewed_content, dict) else st.session_state.reviewed_content
            preferences = {**st.session_state.business_info, **st.session_state.content_preferences}
            
            # Ajouter le token à la session pour la publication
            preferences['linkedin_token'] = st.session_state.linkedin_token
            
            if st.button("📤 Publier sur LinkedIn", type="primary"):
                with st.spinner("📤 Publication en cours..."):
                    try:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        result = loop.run_until_complete(
                            self.posting_agent.post_to_linkedin_real(
                                content_text, 
                                preferences, 
                                image_path=st.session_state.image_path
                            )
                        )
                        loop.close()
                        
                        if result:
                            st.success("✅ Contenu publié sur LinkedIn avec succès!")
                            st.info(f"🔗 URL du post: {result.get('post_url', 'Non disponible')}")
                            
                            # Bouton pour recommencer
                            if st.button("🔄 Créer un nouveau post"):
                                # Reset de toutes les variables
                                for key in ['current_step', 'business_info', 'content_preferences', 
                                           'generated_content', 'reviewed_content', 'image_path']:
                                    if key in st.session_state:
                                        del st.session_state[key]
                                st.session_state.current_step = 1
                                st.rerun()
                        else:
                            st.error("❌ Échec de la publication sur LinkedIn")
                            
                    except Exception as e:
                        st.error(f"❌ Erreur lors de la publication: {e}")
        
        # Option 2: Configuration LinkedIn
        elif client_id and client_secret and (not access_token or access_token == "your_linkedin_token_here"):
            st.info("🔐 Configuration LinkedIn requise")
            
            if st.button("🔐 Configurer LinkedIn"):
                try:
                    token = self.linkedin_auth.authenticate()
                    if token:
                        st.session_state.linkedin_token = token
                        st.success("✅ LinkedIn configuré avec succès!")
                        st.rerun()
                    else:
                        st.error("❌ Configuration LinkedIn échouée")
                except Exception as e:
                    st.error(f"❌ Erreur de configuration: {e}")
        
        # Option 3: Sauvegarde locale
        else:
            st.warning("⚠️ LinkedIn non configuré")
            st.success("💡 Pas de problème ! Vous pouvez sauvegarder le contenu pour publication manuelle")
            st.info("📋 Le contenu et l'image seront sauvegardés localement pour que vous puissiez les publier manuellement sur LinkedIn")
            
            # Récupération du contenu final
            content_text = st.session_state.reviewed_content.get('content', st.session_state.reviewed_content) if isinstance(st.session_state.reviewed_content, dict) else st.session_state.reviewed_content
            preferences = {**st.session_state.business_info, **st.session_state.content_preferences}
            
            if st.button("💾 Sauvegarder le contenu", type="primary"):
                try:
                    # Sauvegarder le contenu
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    
                    # Créer le dossier si nécessaire
                    os.makedirs("data/posted_content", exist_ok=True)
                    
                    # Sauvegarder le contenu
                    content_data = {
                        "timestamp": timestamp,
                        "content": content_text,
                        "image_path": st.session_state.image_path,
                        "preferences": preferences,
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
                        # Reset de toutes les variables
                        for key in ['current_step', 'business_info', 'content_preferences', 
                                   'generated_content', 'reviewed_content', 'image_path']:
                            if key in st.session_state:
                                del st.session_state[key]
                        st.session_state.current_step = 1
                        st.rerun()
                        
                except Exception as e:
                    st.error(f"❌ Erreur lors de la sauvegarde: {e}")
        
        # Instructions pour configurer LinkedIn
        if not client_id or not client_secret:
            st.subheader("📋 Instructions pour configurer LinkedIn")
            st.markdown("""
            Pour configurer LinkedIn, ajoutez ces variables dans votre fichier `.env` :
            
            ```env
            LINKEDIN_CLIENT_ID=votre_client_id
            LINKEDIN_CLIENT_SECRET=votre_client_secret
            LINKEDIN_ACCESS_TOKEN=votre_access_token
            ```
            
            **Étapes pour obtenir les clés :**
            1. Créez une application LinkedIn Developer
            2. Configurez les permissions OAuth2
            3. Obtenez le Client ID et Client Secret
            4. Générez un Access Token
            """)
        
        # Test de connexion LinkedIn (optionnel)
        if st.button("🧪 Tester la connexion LinkedIn", help="Vérifier que la connexion LinkedIn fonctionne"):
            try:
                # Utiliser le token de la session (qui peut venir du fichier sauvegardé)
                token_to_test = st.session_state.linkedin_token or access_token
                
                if token_to_test and token_to_test != "your_linkedin_token_here":
                    # Test simple de l'API LinkedIn
                    headers = {
                        'Authorization': f'Bearer {token_to_test}',
                        'Content-Type': 'application/json'
                    }
                    
                    # Test de l'API de profil
                    response = requests.get(
                        'https://api.linkedin.com/v2/me',
                        headers=headers
                    )
                    
                    if response.status_code == 200:
                        profile_data = response.json()
                        st.success("✅ Connexion LinkedIn réussie!")
                        st.info(f"👤 Connecté en tant que: {profile_data.get('localizedFirstName', '')} {profile_data.get('localizedLastName', '')}")
                    else:
                        st.error(f"❌ Erreur de connexion LinkedIn: {response.status_code}")
                else:
                    st.warning("⚠️ Access Token non configuré")
                    
            except Exception as e:
                st.error(f"❌ Erreur lors du test: {e}")

    def run(self):
        """Exécute l'application Streamlit"""
        self.render_header()
        self.render_steps_progress()
        
        # Navigation entre les étapes
        if st.session_state.current_step == 1:
            self.step_business_config()
        elif st.session_state.current_step == 2:
            self.step_content_preferences()
        elif st.session_state.current_step == 3:
            self.step_content_generation()
        elif st.session_state.current_step == 4:
            self.step_content_review()
        elif st.session_state.current_step == 5:
            self.step_image_generation()
        elif st.session_state.current_step == 6:
            self.step_linkedin_preview()
        elif st.session_state.current_step == 7:
            self.step_publication()

# Point d'entrée de l'application
if __name__ == "__main__":
    app = StreamlitContentEngine()
    app.run() 