# 🚀 Guide de Déploiement Gratuit

## Option 1: Render.com (Recommandé)

### Étapes:
1. Créez un compte sur https://render.com
2. Connectez votre dépôt GitHub
3. Cliquez sur "New +" → "Web Service"
4. Sélectionnez votre repo
5. Render détectera automatiquement `render.yaml`
6. Ajoutez vos variables d'environnement:
   - `TIKTOK_USERNAME`
   - `INSTAGRAM_USERNAME`
   - `INSTAGRAM_PASSWORD`
7. Cliquez sur "Create Web Service"

**Plan gratuit:** 750h/mois, se met en veille après 15min d'inactivité

---

## Option 2: Railway.app

### Étapes:
1. Créez un compte sur https://railway.app
2. Cliquez sur "New Project" → "Deploy from GitHub repo"
3. Sélectionnez votre repo
4. Railway détectera automatiquement le `Procfile`
5. Ajoutez vos variables d'environnement dans Settings → Variables:
   ```
   TIKTOK_USERNAME=zasai26
   INSTAGRAM_USERNAME=votre_username
   INSTAGRAM_PASSWORD=votre_password
   VIDEO_FOLDER=videos
   STATE_FILE=downloaded.json
   ```
6. Le déploiement démarre automatiquement

**Plan gratuit:** $5 de crédit/mois (~500h)

---

## Option 3: Fly.io

### Étapes:
1. Installez Fly CLI: https://fly.io/docs/hands-on/install-flyctl/
2. Créez un compte: `fly auth signup`
3. Dans le dossier du projet:
   ```bash
   fly launch
   fly secrets set TIKTOK_USERNAME=zasai26
   fly secrets set INSTAGRAM_USERNAME=votre_username
   fly secrets set INSTAGRAM_PASSWORD=votre_password
   fly deploy
   ```

**Plan gratuit:** 3 machines partagées, 160GB/mois

---

## Option 4: Koyeb

### Étapes:
1. Créez un compte sur https://koyeb.com
2. Cliquez sur "Create App"
3. Sélectionnez "GitHub" et votre repo
4. Koyeb détectera le Dockerfile
5. Ajoutez les variables d'environnement
6. Déployez

**Plan gratuit:** 1 service web, se met en veille après inactivité

---

## ⚠️ Important

- Les plans gratuits ont des limitations (RAM, CPU, temps d'activité)
- Les services se mettent en veille après inactivité
- Le stockage des vidéos est temporaire (utilisez un stockage externe si nécessaire)
- Pour un service 24/7, utilisez un service de ping (comme UptimeRobot) pour garder l'app active

---

## 📦 Avant de déployer

1. Créez un repo GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/votre-username/tiktok-instagram-api.git
   git push -u origin main
   ```

2. Assurez-vous que `.env` est dans `.gitignore` (déjà fait)

3. Les variables d'environnement seront configurées sur la plateforme d'hébergement
