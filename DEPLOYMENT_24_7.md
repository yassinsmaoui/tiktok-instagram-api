# 🚀 Déploiement 24/7 - Guide Complet

## Architecture recommandée

Pour une automation 24h/24 :

### Option 1 : API FastAPI sur Render + Interface Streamlit

**1. Déployez l'API FastAPI sur Render.com**
- L'API tourne 24h/24 avec le planificateur
- Gère les téléchargements et publications automatiques
- URL : `https://votre-app.onrender.com`

**2. Déployez Streamlit séparément**
- Interface de contrôle uniquement
- Se connecte à l'API FastAPI
- Pas besoin de tourner 24h/24

**Étapes :**

1. **Sur Render.com :**
   - New → Web Service
   - Connectez votre repo GitHub
   - Build Command : `pip install -r requirements.txt`
   - Start Command : `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Variables d'environnement :
     ```
     TIKTOK_USERNAME=zasai26
     INSTAGRAM_USERNAME=votre_username
     INSTAGRAM_PASSWORD=votre_password
     VIDEO_FOLDER=videos
     STATE_FILE=downloaded.json
     ```

2. **Sur Streamlit Cloud :**
   - Changez `streamlit_app.py` pour utiliser l'API Render
   - Dans les secrets, ajoutez :
     ```toml
     API_URL = "https://votre-app.onrender.com"
     ```

---

### Option 2 : Serveur VPS (Recommandé pour 24/7)

**Fournisseurs gratuits/pas chers :**
- Oracle Cloud (Always Free - 2 VMs)
- Google Cloud (300$ crédit gratuit)
- AWS EC2 (12 mois gratuit)
- DigitalOcean (5$/mois)

**Installation sur VPS :**

```bash
# 1. Installer Python
sudo apt update
sudo apt install python3 python3-pip python3-venv ffmpeg -y

# 2. Cloner le repo
git clone https://github.com/yassinsmaoui/tiktok-instagram-api.git
cd tiktok-instagram-api

# 3. Créer venv et installer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Configurer .env
nano .env
# Ajoutez vos credentials

# 5. Lancer avec systemd (service permanent)
sudo nano /etc/systemd/system/tiktok-instagram.service
```

**Fichier service :**
```ini
[Unit]
Description=TikTok Instagram Automation
After=network.target

[Service]
Type=simple
User=votre_user
WorkingDirectory=/home/votre_user/tiktok-instagram-api
Environment="PATH=/home/votre_user/tiktok-instagram-api/venv/bin"
ExecStart=/home/votre_user/tiktok-instagram-api/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

**Activer le service :**
```bash
sudo systemctl daemon-reload
sudo systemctl enable tiktok-instagram.service
sudo systemctl start tiktok-instagram.service
sudo systemctl status tiktok-instagram.service
```

---

### Option 3 : Railway.app (Plus simple)

1. Connectez votre repo GitHub
2. Railway détecte automatiquement FastAPI
3. Ajoutez les variables d'environnement
4. Déployez
5. L'app tourne 24h/24 automatiquement

**Avantage :** Pas de configuration complexe
**Inconvénient :** 5$ de crédit/mois (gratuit)

---

### Option 4 : Fly.io

```bash
# Installer Fly CLI
curl -L https://fly.io/install.sh | sh

# Se connecter
fly auth login

# Déployer
fly launch
fly secrets set INSTAGRAM_USERNAME=xxx INSTAGRAM_PASSWORD=xxx
fly deploy
```

---

## Comparaison

| Plateforme | Gratuit | 24/7 | Complexité | Recommandé |
|------------|---------|------|------------|------------|
| Streamlit Cloud | ✅ | ❌ | Facile | Interface uniquement |
| Render.com | ✅ (750h) | ⚠️ (se met en veille) | Facile | Oui |
| Railway.app | ⚠️ (5$/mois) | ✅ | Facile | Oui |
| Fly.io | ✅ | ✅ | Moyen | Oui |
| VPS Oracle | ✅ | ✅ | Difficile | Le meilleur |

---

## Configuration du Planificateur

Une fois l'API déployée 24/7, configurez les heures de publication :

**Via l'interface Streamlit :**
1. Onglet "Planificateur"
2. Entrez les heures : `09:00,15:00,21:00`
3. Cliquez "Démarrer"

**Via l'API directement :**
```bash
curl -X POST https://votre-app.onrender.com/scheduler/times \
  -H "Content-Type: application/json" \
  -d '{"times": ["09:00", "15:00", "21:00"]}'

curl -X POST https://votre-app.onrender.com/scheduler/start
```

---

## Monitoring

Pour garder l'app active sur Render (éviter la mise en veille) :

1. Inscrivez-vous sur https://uptimerobot.com (gratuit)
2. Créez un monitor HTTP(S)
3. URL : `https://votre-app.onrender.com/`
4. Intervalle : 5 minutes
5. L'app ne se mettra plus en veille

---

## Recommandation finale

**Pour débuter :** Railway.app ou Render.com + UptimeRobot
**Pour du sérieux :** VPS Oracle Cloud (gratuit à vie)
**Interface :** Streamlit Cloud (connecté à l'API)
