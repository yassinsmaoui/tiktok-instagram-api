import streamlit as st
import os
import sys
from datetime import datetime
import json

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services import tiktok_service, instagram_service, scheduler_service
from config import VIDEO_FOLDER, STATE_FILE

st.set_page_config(page_title="TikTok → Instagram Automation", page_icon="🎬", layout="wide")

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

st.title("🎬 TikTok → Instagram Automation")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    st.info("Application autonome - Pas besoin d'API externe")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📥 TikTok", "📱 Instagram", "📤 Publier", "⏰ Planificateur", "🎥 Vidéos"])

# Tab 1: TikTok Download
with tab1:
    st.header("📥 Télécharger des vidéos TikTok")
    
    col1, col2 = st.columns(2)
    
    with col1:
        tiktok_username = st.text_input("Nom d'utilisateur TikTok", value=os.getenv("TIKTOK_USERNAME", "zasai26"))
        max_videos = st.number_input("Nombre de vidéos à télécharger", min_value=1, max_value=100, value=10)
        
        if st.button("🚀 Démarrer le téléchargement", use_container_width=True):
            with st.spinner("Téléchargement en cours..."):
                try:
                    result = tiktok_service.download_videos(tiktok_username)
                    st.success(f"✅ {len(result['new_downloads'])} nouvelles vidéos téléchargées")
                    if result['errors']:
                        st.warning(f"⚠️ {len(result['errors'])} erreurs")
                except Exception as e:
                    st.error(f"❌ Erreur: {str(e)}")
    
    with col2:
        if st.button("🔍 Vérifier le statut", use_container_width=True):
            try:
                downloaded_ids = tiktok_service.get_downloaded_ids()
                st.metric("Total téléchargés", len(downloaded_ids))
            except Exception as e:
                st.error(f"❌ Erreur: {str(e)}")

# Tab 2: Instagram Login
with tab2:
    st.header("📱 Connexion Instagram")
    
    col1, col2 = st.columns(2)
    
    with col1:
        insta_username = st.text_input("Nom d'utilisateur Instagram", 
                                       value=os.getenv("INSTAGRAM_USERNAME", ""))
        insta_password = st.text_input("Mot de passe Instagram", 
                                       type="password",
                                       value=os.getenv("INSTAGRAM_PASSWORD", ""))
        
        if st.button("🔐 Se connecter", use_container_width=True):
            if insta_username and insta_password:
                with st.spinner("Connexion en cours..."):
                    try:
                        instagram_service.get_client(insta_username, insta_password)
                        st.session_state.logged_in = True
                        st.session_state.insta_username = insta_username
                        st.session_state.insta_password = insta_password
                        st.success("✅ Connecté avec succès")
                    except Exception as e:
                        st.error(f"❌ Erreur: {str(e)}")
            else:
                st.warning("⚠️ Veuillez remplir tous les champs")
    
    with col2:
        st.write("")
        st.write("")
        if st.button("🚪 Se déconnecter", use_container_width=True):
            try:
                instagram_service.reset_client()
                st.session_state.logged_in = False
                st.success("✅ Déconnecté")
            except Exception as e:
                st.error(f"❌ Erreur: {str(e)}")
        
        if st.session_state.logged_in:
            st.success(f"✅ Connecté en tant que: {st.session_state.get('insta_username', 'N/A')}")

# Tab 3: Post Video
with tab3:
    st.header("📤 Publier une vidéo sur Instagram")
    
    if not st.session_state.logged_in:
        st.warning("⚠️ Veuillez vous connecter à Instagram d'abord")
    else:
        videos = instagram_service.list_videos()
        
        if videos:
            video_choice = st.selectbox("Choisir une vidéo", ["Aléatoire"] + videos)
            caption = st.text_area("Légende (optionnel)", height=100)
            
            if st.button("📤 Publier maintenant", use_container_width=True):
                with st.spinner("Publication en cours..."):
                    try:
                        video_id = None if video_choice == "Aléatoire" else video_choice
                        result = instagram_service.post_video(
                            video_filename=video_id,
                            username=st.session_state.insta_username,
                            password=st.session_state.insta_password
                        )
                        st.success(f"✅ Vidéo publiée: {result['uploaded']}")
                        st.info(f"Media ID: {result['media_id']}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Erreur: {str(e)}")
        else:
            st.info("ℹ️ Aucune vidéo disponible. Téléchargez des vidéos TikTok d'abord.")

# Tab 4: Scheduler
with tab4:
    st.header("⏰ Planificateur automatique")
    
    if not st.session_state.logged_in:
        st.warning("⚠️ Veuillez vous connecter à Instagram d'abord")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Configuration")
            post_times = st.text_input("Heures de publication (séparées par des virgules)", 
                                       placeholder="09:00,15:00,21:00",
                                       value="09:00,15:00,21:00")
            
            if st.button("💾 Mettre à jour les heures", use_container_width=True):
                if post_times:
                    times_list = [t.strip() for t in post_times.split(",")]
                    try:
                        scheduler_service.scheduler_service.update_schedule(times_list)
                        st.success("✅ Heures mises à jour")
                    except Exception as e:
                        st.error(f"❌ Erreur: {str(e)}")
                else:
                    st.warning("⚠️ Veuillez entrer des heures")
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("▶️ Démarrer", use_container_width=True):
                    try:
                        scheduler_service.scheduler_service.start()
                        st.success("✅ Planificateur démarré")
                    except Exception as e:
                        st.error(f"❌ Erreur: {str(e)}")
            
            with col_b:
                if st.button("⏸️ Arrêter", use_container_width=True):
                    try:
                        scheduler_service.scheduler_service.stop()
                        st.success("✅ Planificateur arrêté")
                    except Exception as e:
                        st.error(f"❌ Erreur: {str(e)}")
        
        with col2:
            st.subheader("Statut")
            if st.button("🔄 Actualiser le statut", use_container_width=True):
                try:
                    status = scheduler_service.scheduler_service.get_status()
                    st.metric("État", "🟢 Actif" if status.get("is_running") else "🔴 Inactif")
                    if status.get("next_run_time"):
                        st.info(f"⏰ Prochaine exécution: {status['next_run_time']}")
                    if status.get("scheduled_times"):
                        st.write("📅 Heures programmées:", ", ".join(status['scheduled_times']))
                except Exception as e:
                    st.error(f"❌ Erreur: {str(e)}")
            
            st.write("")
            if st.button("⚡ Publier maintenant (manuel)", use_container_width=True):
                with st.spinner("Publication en cours..."):
                    try:
                        result = instagram_service.post_video(
                            username=st.session_state.insta_username,
                            password=st.session_state.insta_password
                        )
                        st.success(f"✅ Vidéo publiée: {result['uploaded']}")
                    except Exception as e:
                        st.error(f"❌ Erreur: {str(e)}")

# Tab 5: Videos
with tab5:
    st.header("🎥 Vidéos locales")
    
    if st.button("🔄 Actualiser la liste", use_container_width=True):
        st.rerun()
    
    try:
        videos = instagram_service.list_videos()
        
        if videos:
            st.success(f"📊 {len(videos)} vidéo(s) disponible(s)")
            
            for video in videos:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.text(f"📹 {video}")
                with col2:
                    if st.button("🗑️ Supprimer", key=f"del_{video}"):
                        try:
                            video_path = os.path.join(VIDEO_FOLDER, video)
                            os.remove(video_path)
                            st.success(f"✅ {video} supprimée")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Erreur: {str(e)}")
        else:
            st.info("ℹ️ Aucune vidéo disponible")
    except Exception as e:
        st.error(f"❌ Erreur: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit")
