import os
import re
import random
from instagrapi import Client
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
        uname = username or INSTAGRAM_USERNAME
        pwd = password or INSTAGRAM_PASSWORD
        if not uname or not pwd:
            raise ValueError("Instagram credentials not configured.")
        _client.login(uname, pwd)
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
