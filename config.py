import os
from dotenv import load_dotenv

load_dotenv()

TIKTOK_USERNAME = os.getenv("TIKTOK_USERNAME", "zasai26")
INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME", "")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD", "")
VIDEO_FOLDER = os.getenv("VIDEO_FOLDER", "videos")
STATE_FILE = os.getenv("STATE_FILE", "downloaded.json")

INSTAGRAM_HASHTAGS = [
    "#reels",
    "#viral",
    "#explorepage",
    "#instagramreels",
    "#trending",
    "#fyp"
]

# Schedule times (HH:MM)
POST_TIMES = ["11:00", "16:00", "17:00", "20:32", "22:00"]
