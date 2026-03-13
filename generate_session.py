import os
from instagrapi import Client

print("=== Générateur de session Instagram ===\n")

username = input("Nom d'utilisateur Instagram: ")
password = input("Mot de passe Instagram: ")

print("\nConnexion en cours...")

try:
    cl = Client()
    cl.delay_range = [2, 5]
    cl.login(username, password)
    
    session_file = f"session_{username}.json"
    cl.dump_settings(session_file)
    
    print(f"\n✅ Session créée avec succès!")
    print(f"📁 Fichier: {session_file}")
    print(f"\nUploadez ce fichier sur Streamlit Cloud:")
    print("1. Allez dans votre app Streamlit")
    print("2. Settings → Secrets")
    print("3. Ajoutez le contenu du fichier dans les secrets")
    
    with open(session_file, 'r') as f:
        print(f"\n--- Copiez ce contenu dans Streamlit Secrets ---")
        print(f.read())
    
except Exception as e:
    print(f"\n❌ Erreur: {str(e)}")
    print("\nSi vous avez 'challenge_required':")
    print("1. Connectez-vous sur Instagram (téléphone/navigateur)")
    print("2. Complétez toutes les vérifications")
    print("3. Attendez 15 minutes")
    print("4. Réessayez ce script")

input("\nAppuyez sur Entrée pour quitter...")
