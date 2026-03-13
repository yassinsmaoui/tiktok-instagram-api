import os
import re
import random
import time
from instagrapi import Client
from instagrapi.exceptions import ChallengeRequired, LoginRequired
from config import (
    INSTAGRAM_USERNAME,
    INSTAGRAM_PASSWORD,
    VIDEO_FOLDER,
    INSTAGRAM_HASHTAGS,
)

_client: Client = None


def get_client(username: str = None, password: str = None) -> Client:
    """Return authenticated Instagram client (cached)."""
    global _client
    if _client is None:
        _client = Client()
        _client.delay_range = [2, 5]
        
        uname = username or INSTAGRAM_USERNAME
        pwd = password or INSTAGRAM_PASSWORD
        if not uname or not pwd:
            raise ValueError("Instagram credentials not configured.")
        
        # Try to load session from environment variable (Streamlit secrets)
        session_data = os.getenv(f"INSTAGRAM_SESSION_{uname.upper()}")
        if session_data:
            try:
                import json
                _client.set_settings(json.loads(session_data))
                _client.login(uname, pwd)
                return _client
            except:
                pass
        
        # Try to load session from file (local)
        session_file = f"session_{uname}.json"
        if os.path.exists(session_file):
            try:
                _client.load_settings(session_file)
                _client.login(uname, pwd)
                _client.get_timeline_feed()
                return _client
            except:
                pass
        
        # Fresh login
        try:
            _client.login(uname, pwd)
            _client.dump_settings(session_file)
        except ChallengeRequired as e:
            raise Exception("Instagram demande une vérification. Utilisez 'generate_session.py' en local pour créer une session, puis uploadez-la sur Streamlit Cloud.")
        except Exception as e:
            raise Exception(f"Erreur de connexion: {str(e)}")
    
    return _client


def reset_client():
    """Force re-login on next request."""
    global _client
    _client = None


def clean_caption(text: str) -> str:
    text = re.sub(r"http\S+", "", text)
    return text.strip()


def list_videos() -> list[str]:
    return [v for v in os.listdir(VIDEO_FOLDER) if v.endswith(".mp4")]


def post_video(video_filename: str = None, username: str = None, password: str = None) -> dict:
    """Post a video to Instagram Reels. Picks random if no filename given."""
    videos = list_videos()
    if not videos:
        raise FileNotFoundError("No videos found in the videos folder.")

    video = video_filename if video_filename else random.choice(videos)

    if video not in videos:
        raise FileNotFoundError(f"Video '{video}' not found.")

    caption = video.replace(".mp4", "")
    caption = clean_caption(caption)
    caption = caption + "\n\n" + " ".join(INSTAGRAM_HASHTAGS)

    video_path = os.path.join(VIDEO_FOLDER, video)

    cl = get_client(username, password)
    media = cl.clip_upload(video_path, caption)
    
    os.remove(video_path)

    return {
        "uploaded": video,
        "media_id": str(media.pk),
        "caption": caption,
    }
