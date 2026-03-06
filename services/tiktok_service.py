import yt_dlp
import os
import re
import json
from config import VIDEO_FOLDER, STATE_FILE, TIKTOK_USERNAME

os.makedirs(VIDEO_FOLDER, exist_ok=True)


def load_state() -> set:
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()


def save_state(ids: set):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(list(ids), f, ensure_ascii=False, indent=2)


def clean_filename(text: str) -> str:
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r'[\\/*?:"<>|]', "", text)
    return text.strip()[:100]


def download_videos(username: str = None) -> dict:
    """Download all videos from a TikTok account. Returns summary."""
    target = username or TIKTOK_USERNAME
    downloaded_ids = load_state()
    new_downloads = []
    errors = []

    def hook(d):
        if d["status"] == "finished":
            info = d["info_dict"]
            vid = info.get("id")
            caption = info.get("description") or "video"
            caption = clean_filename(caption)

            old_file = d["filename"]
            new_file = os.path.join(VIDEO_FOLDER, caption + ".mp4")

            if not os.path.exists(new_file):
                os.rename(old_file, new_file)

            downloaded_ids.add(vid)
            save_state(downloaded_ids)
            new_downloads.append({"id": vid, "filename": caption + ".mp4"})

    ydl_opts = {
        "format": "mp4",
        "outtmpl": f"{VIDEO_FOLDER}/%(id)s.%(ext)s",
        "progress_hooks": [hook],
        "ignoreerrors": True,
    }

    url = f"https://www.tiktok.com/@{target}"

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        errors.append(str(e))

    return {
        "username": target,
        "new_downloads": new_downloads,
        "total_downloaded": len(downloaded_ids),
        "errors": errors,
    }


def get_downloaded_ids() -> list:
    return list(load_state())
