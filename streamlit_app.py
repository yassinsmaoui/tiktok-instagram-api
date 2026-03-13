import streamlit as st
import requests
import os
from datetime import datetime

st.set_page_config(page_title="TikTok → Instagram Automation", page_icon="🎬", layout="wide")

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("🎬 TikTok → Instagram Automation")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    api_url = st.text_input("API URL", value=API_URL)
    st.markdown("---")
    st.info("Cette interface contrôle l'API FastAPI d'automation TikTok → Instagram")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📥 TikTok", "📱 Instagram", "📤 Publier", "⏰ Planificateur", "🎥 Vidéos"])

# Tab 1: TikTok Download
with tab1:
    st.header("📥 Télécharger des vidéos TikTok")
    
    col1, col2 = st.columns(2)
    
    with col1:
        max_videos = st.number_input("Nombre de vidéos à télécharger", min_value=1, max_value=100, value=10)
        
        if st.button("🚀 Démarrer le téléchargement", use_container_width=True):
            with st.spinner("Téléchargement en cours..."):
                try:
                    response = requests.post(f"{api_url}/tiktok/download", json={"max_videos": max_videos})
                    if response.status_code == 200:
                        st.success(response.json().get("message", "Téléchargement démarré"))
                    else:
                        st.error(f"Erreur: {response.text}")
                except Exception as e:
                    st.error(f"Erreur de connexion: {str(e)}")
    
    with col2:
        if st.button("🔍 Vérifier le statut", use_container_width=True):
            try:
                response = requests.get(f"{api_url}/tiktok/download/status")
                if response.status_code == 200:
                    data = response.json()
                    st.metric("Statut", data.get("status", "N/A"))
                    col_a, col_b = st.columns(2)
                    col_a.metric("Téléchargés", data.get("downloaded", 0))
                    col_b.metric("Erreurs", data.get("errors", 0))
                else:
                    st.error(f"Erreur: {response.text}")
            except Exception as e:
                st.error(f"Erreur de connexion: {str(e)}")

# Tab 2: Instagram Login
with tab2:
    st.header("📱 Connexion Instagram")
    
    col1, col2 = st.columns(2)
    
    with col1:
        insta_username = st.text_input("Nom d'utilisateur Instagram", key="insta_user")
        insta_password = st.text_input("Mot de passe Instagram", type="password", key="insta_pass")
        
        if st.button("🔐 Se connecter", use_container_width=True):
            if insta_username and insta_password:
                with st.spinner("Connexion en cours..."):
                    try:
                        response = requests.post(f"{api_url}/instagram/login", 
                                                json={"username": insta_username, "password": insta_password})
                        if response.status_code == 200:
                            st.success(response.json().get("message", "Connecté avec succès"))
                        else:
                            st.error(f"Erreur: {response.text}")
                    except Exception as e:
                        st.error(f"Erreur de connexion: {str(e)}")
            else:
                st.warning("Veuillez remplir tous les champs")
    
    with col2:
        st.write("")
        st.write("")
        if st.button("🚪 Se déconnecter", use_container_width=True):
            try:
                response = requests.post(f"{api_url}/instagram/logout")
                if response.status_code == 200:
                    st.success(response.json().get("message", "Déconnecté"))
                else:
                    st.error(f"Erreur: {response.text}")
            except Exception as e:
                st.error(f"Erreur de connexion: {str(e)}")

# Tab 3: Post Video
with tab3:
    st.header("📤 Publier une vidéo sur Instagram")
    
    video_id = st.text_input("ID de la vidéo (optionnel - laissez vide pour une vidéo aléatoire)")
    caption = st.text_area("Légende (optionnel)", height=100)
    
    if st.button("📤 Publier maintenant", use_container_width=True):
        with st.spinner("Publication en cours..."):
            try:
                payload = {}
                if video_id:
                    payload["video_id"] = video_id
                if caption:
                    payload["caption"] = caption
                
                response = requests.post(f"{api_url}/instagram/post", json=payload)
                if response.status_code == 200:
                    data = response.json()
                    st.success(data.get("message", "Vidéo publiée avec succès"))
                    if "uploaded" in data:
                        st.info(f"Vidéo publiée: {data['uploaded']}")
                else:
                    st.error(f"Erreur: {response.text}")
            except Exception as e:
                st.error(f"Erreur de connexion: {str(e)}")

# Tab 4: Scheduler
with tab4:
    st.header("⏰ Planificateur automatique")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Configuration")
        post_times = st.text_input("Heures de publication (séparées par des virgules)", 
                                   placeholder="09:00,15:00,21:00")
        
        if st.button("💾 Mettre à jour les heures", use_container_width=True):
            if post_times:
                times_list = [t.strip() for t in post_times.split(",")]
                try:
                    response = requests.put(f"{api_url}/scheduler/times", json={"times": times_list})
                    if response.status_code == 200:
                        st.success(response.json().get("message", "Heures mises à jour"))
                    else:
                        st.error(f"Erreur: {response.text}")
                except Exception as e:
                    st.error(f"Erreur de connexion: {str(e)}")
            else:
                st.warning("Veuillez entrer des heures")
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("▶️ Démarrer", use_container_width=True):
                try:
                    response = requests.post(f"{api_url}/scheduler/start")
                    if response.status_code == 200:
                        st.success(response.json().get("message", "Planificateur démarré"))
                    else:
                        st.error(f"Erreur: {response.text}")
                except Exception as e:
                    st.error(f"Erreur de connexion: {str(e)}")
        
        with col_b:
            if st.button("⏸️ Arrêter", use_container_width=True):
                try:
                    response = requests.post(f"{api_url}/scheduler/stop")
                    if response.status_code == 200:
                        st.success(response.json().get("message", "Planificateur arrêté"))
                    else:
                        st.error(f"Erreur: {response.text}")
                except Exception as e:
                    st.error(f"Erreur de connexion: {str(e)}")
    
    with col2:
        st.subheader("Statut")
        if st.button("🔄 Actualiser le statut", use_container_width=True):
            try:
                response = requests.get(f"{api_url}/scheduler/status")
                if response.status_code == 200:
                    data = response.json()
                    st.metric("État", "🟢 Actif" if data.get("is_running") else "🔴 Inactif")
                    if data.get("next_run_time"):
                        st.info(f"Prochaine exécution: {data['next_run_time']}")
                    if data.get("scheduled_times"):
                        st.write("Heures programmées:", ", ".join(data['scheduled_times']))
                else:
                    st.error(f"Erreur: {response.text}")
            except Exception as e:
                st.error(f"Erreur de connexion: {str(e)}")
        
        st.write("")
        if st.button("⚡ Publier maintenant (manuel)", use_container_width=True):
            with st.spinner("Publication en cours..."):
                try:
                    response = requests.post(f"{api_url}/scheduler/trigger")
                    if response.status_code == 200:
                        st.success(response.json().get("message", "Publication déclenchée"))
                    else:
                        st.error(f"Erreur: {response.text}")
                except Exception as e:
                    st.error(f"Erreur de connexion: {str(e)}")

# Tab 5: Videos
with tab5:
    st.header("🎥 Vidéos locales")
    
    if st.button("🔄 Actualiser la liste", use_container_width=True):
        st.rerun()
    
    try:
        response = requests.get(f"{api_url}/videos/")
        if response.status_code == 200:
            data = response.json()
            videos = data.get("videos", [])
            
            if videos:
                st.success(f"{len(videos)} vidéo(s) disponible(s)")
                
                for video in videos:
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.text(f"📹 {video}")
                    with col2:
                        if st.button("📥 Télécharger", key=f"dl_{video}"):
                            st.info(f"URL: {api_url}/videos/{video}")
                    with col3:
                        if st.button("🗑️ Supprimer", key=f"del_{video}"):
                            try:
                                del_response = requests.delete(f"{api_url}/videos/{video}")
                                if del_response.status_code == 200:
                                    st.success(f"{video} supprimée")
                                    st.rerun()
                                else:
                                    st.error(f"Erreur: {del_response.text}")
                            except Exception as e:
                                st.error(f"Erreur: {str(e)}")
            else:
                st.info("Aucune vidéo disponible")
        else:
            st.error(f"Erreur: {response.text}")
    except Exception as e:
        st.error(f"Erreur de connexion: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit & FastAPI")
