# 🎬 TikTok → Instagram Automation

Application Streamlit pour automatiser le téléchargement de vidéos TikTok et leur publication sur Instagram Reels.

## 🚀 Déploiement sur Streamlit Cloud

1. Fork ce repository
2. Allez sur https://share.streamlit.io/
3. Connectez votre compte GitHub
4. Sélectionnez ce repository
5. Fichier principal : `streamlit_app.py`
6. Ajoutez les secrets dans Settings → Secrets :

```toml
TIKTOK_USERNAME = "zasai26"
INSTAGRAM_USERNAME = "votre_username"
INSTAGRAM_PASSWORD = "votre_password"
VIDEO_FOLDER = "videos"
STATE_FILE = "downloaded.json"
API_URL = "http://localhost:8000"
```

## 📦 Installation locale

```bash
pip install -r requirements.txt
```

## 🏃 Lancer l'application

### Option 1 : Tout en un
```bash
start_app.bat
```

### Option 2 : Séparément
Terminal 1 - API :
```bash
start_api.bat
```

Terminal 2 - Streamlit :
```bash
start_streamlit.bat
```

## 📚 Documentation

- **Streamlit** : http://localhost:8501
- **API FastAPI** : http://localhost:8000
- **API Docs** : http://localhost:8000/docs

## ⚙️ Fonctionnalités

- 📥 Téléchargement automatique de vidéos TikTok
- 📱 Connexion Instagram
- 📤 Publication de vidéos sur Instagram Reels
- ⏰ Planificateur automatique
- 🎥 Gestion des vidéos locales

## 🔧 Technologies

- **Frontend** : Streamlit
- **Backend** : FastAPI
- **TikTok** : yt-dlp
- **Instagram** : instagrapi
- **Scheduler** : APScheduler
