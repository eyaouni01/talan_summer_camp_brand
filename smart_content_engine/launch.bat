@echo off
echo ========================================
echo   Smart Content Engine - Streamlit
echo ========================================
echo.

echo 🚀 Lancement de l'interface Streamlit...
echo.

REM Vérifier si le fichier .env existe
if not exist ".env" (
    echo ⚠️ Fichier .env non trouvé
    echo 📝 Création d'un template .env...
    echo # Configuration des API > .env
    echo GOOGLE_API_KEY=your_google_api_key_here >> .env
    echo LINKEDIN_ACCESS_TOKEN=your_linkedin_token_here >> .env
    echo. >> .env
    echo # Configuration LinkedIn (optionnel) >> .env
    echo LINKEDIN_CLIENT_ID=your_linkedin_client_id >> .env
    echo LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret >> .env
    echo ✅ Template .env créé
    echo ⚠️ N'oubliez pas de configurer vos clés API dans le fichier .env
    echo.
)

echo 🌐 Lancement de l'application en mode clair...
echo 📱 L'interface sera disponible dans votre navigateur
echo 🔗 URL: http://localhost:8501
echo.

REM Lancer Streamlit avec configuration du mode clair
streamlit run streamlit_app.py --server.port 8501 --server.address localhost --theme.base light

echo.
echo 👋 Application fermée
pause 