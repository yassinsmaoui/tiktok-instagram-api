from fastapi import APIRouter, BackgroundTasks, HTTPException
from models.schemas import DownloadRequest, StatusResponse
from services.tiktok_service import download_videos, get_downloaded_ids

router = APIRouter()

_download_status = {"running": False, "last_result": None}


def _run_download(username: str):
    _download_status["running"] = True
    try:
        result = download_videos(username)
        _download_status["last_result"] = result
    except Exception as e:
        _download_status["last_result"] = {"error": str(e)}
    finally:
        _download_status["running"] = False


@router.post("/download", summary="Download videos from a TikTok account")
def download(body: DownloadRequest, background_tasks: BackgroundTasks):
    if _download_status["running"]:
        raise HTTPException(status_code=409, detail="A download is already in progress.")
    background_tasks.add_task(_run_download, body.username)
    return StatusResponse(success=True, message="Download started in background.")


@router.get("/download/status", summary="Check download status")
def download_status():
    return {
        "running": _download_status["running"],
        "last_result": _download_status["last_result"],
    }


@router.get("/downloaded", summary="List all downloaded video IDs")
def downloaded():
    ids = get_downloaded_ids()
    return {"count": len(ids), "ids": ids}
