# TikTok → Instagram Automation API

A FastAPI server to automate downloading TikTok videos and reposting them to Instagram Reels.

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure credentials
Copy `.env.example` to `.env` and fill in your credentials:
```bash
cp .env.example .env
```

```env
TIKTOK_USERNAME=zasai26
INSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_PASSWORD=your_instagram_password
```

### 3. Run the server
```bash
uvicorn main:app --reload
```

The API will be available at: http://localhost:8000  
Interactive docs: http://localhost:8000/docs

---

## API Endpoints

### TikTok
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/tiktok/download` | Start downloading videos (background task) |
| `GET`  | `/tiktok/download/status` | Check download progress |
| `GET`  | `/tiktok/downloaded` | List all downloaded video IDs |

### Instagram
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/instagram/login` | Login with credentials |
| `POST` | `/instagram/post` | Post a video (random or specified) |
| `POST` | `/instagram/logout` | Clear session |

### Scheduler
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/scheduler/status` | Get status and next run times |
| `POST` | `/scheduler/start` | Start auto-posting scheduler |
| `POST` | `/scheduler/stop` | Stop scheduler |
| `PUT`  | `/scheduler/times` | Update posting times |
| `POST` | `/scheduler/trigger` | Manually trigger a post now |

### Videos
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/videos/` | List all local videos |
| `GET`  | `/videos/{filename}` | Download a specific video |
| `DELETE` | `/videos/{filename}` | Delete a video |

---

## Project Structure

```
tiktok_instagram_api/
├── main.py                     # FastAPI app entry point
├── config.py                   # Settings and env variables
├── requirements.txt
├── .env.example
├── models/
│   └── schemas.py              # Pydantic request/response models
├── routers/
│   ├── tiktok.py               # TikTok download endpoints
│   ├── instagram.py            # Instagram post endpoints
│   ├── scheduler.py            # Scheduler control endpoints
│   └── videos.py               # Video management endpoints
└── services/
    ├── tiktok_service.py       # yt-dlp download logic
    ├── instagram_service.py    # instagrapi post logic
    └── scheduler_service.py    # APScheduler background jobs
```
