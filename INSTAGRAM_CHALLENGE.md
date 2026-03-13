# 🔐 Résoudre l'erreur "challenge_required"

## Pourquoi cette erreur ?

Instagram détecte une connexion suspecte et demande une vérification (captcha, code SMS, etc.).

## Solutions

### Solution 1 : Vérification manuelle (Recommandé)

1. **Connectez-vous à Instagram** depuis :
   - Votre téléphone (application officielle)
   - OU un navigateur web
   
2. **Complétez toutes les vérifications** demandées par Instagram

3. **Attendez 10-15 minutes**

4. **Réessayez** dans l'application Streamlit

### Solution 2 : Utiliser un compte moins sécurisé

1. Créez un **nouveau compte Instagram** dédié à l'automation
2. N'activez **PAS** l'authentification à deux facteurs (2FA)
3. Utilisez ce compte dans l'application

### Solution 3 : Session persistante (Déjà implémenté)

L'application sauvegarde maintenant votre session dans un fichier `session_USERNAME.json`.

Après la première connexion réussie, les connexions suivantes seront plus rapides et moins susceptibles de déclencher des vérifications.

### Solution 4 : Proxy/VPN

Si vous êtes sur un serveur cloud (Streamlit Cloud, Render, etc.) :

1. Instagram peut bloquer les IPs de datacenters
2. **Utilisez l'application en local** pour la première connexion
3. Le fichier de session sera créé
4. Uploadez ce fichier sur votre serveur cloud

### Solution 5 : Attendre

Instagram peut temporairement bloquer votre compte :

- Attendez **24-48 heures**
- Ne tentez **PAS** de vous connecter plusieurs fois rapidement
- Cela aggrave la situation

## Prévention

Pour éviter cette erreur à l'avenir :

1. ✅ Ne vous connectez/déconnectez pas trop souvent
2. ✅ Utilisez toujours la même IP si possible
3. ✅ Limitez le nombre de publications par jour (max 10-15)
4. ✅ Ajoutez des délais entre les actions
5. ❌ N'utilisez PAS votre compte personnel principal
6. ❌ N'utilisez PAS de VPN qui change constamment d'IP

## Note importante

L'automation Instagram viole les conditions d'utilisation d'Instagram. Utilisez à vos risques et périls.
