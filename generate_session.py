import os
import json
from instagrapi import Client

print("=== Générateur de session Instagram pour Streamlit ===\n")

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
    
    # Read session file
    with open(session_file, 'r') as f:
        session_content = f.read()
    
    # Create TOML format
    toml_key = f"INSTAGRAM_SESSION_{username.upper()}"
    
    print(f"\n{'='*60}")
    print("COPIEZ CE CONTENU DANS STREAMLIT SECRETS:")
    print(f"{'='*60}\n")
    print(f'{toml_key} = """{session_content}"""')
    print(f"\n{'='*60}")
    
    # Save to file for easy copy
    toml_file = f"streamlit_secrets_{username}.txt"
    with open(toml_file, 'w') as f:
        f.write(f'{toml_key} = """{session_content}"""')
    
    print(f"\n💾 Sauvegardé dans: {toml_file}")
    print("\nÉtapes suivantes:")
    print("1. Ouvrez le fichier .txt créé")
    print("2. Copiez tout le contenu")
    print("3. Allez sur Streamlit Cloud → Settings → Secrets")
    print("4. Collez le contenu")
    print("5. Cliquez Save")
    
except Exception as e:
    print(f"\n❌ Erreur: {str(e)}")
    print("\nSi vous avez 'challenge_required':")
    print("1. Ouvrez Instagram sur votre téléphone")
    print("2. Complétez toutes les vérifications")
    print("3. Attendez 15-30 minutes")
    print("4. Réessayez ce script")
    print("\nOU créez un nouveau compte Instagram sans 2FA")

input("\nAppuyez sur Entrée pour quitter...")
