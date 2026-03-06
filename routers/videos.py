from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os
from config import VIDEO_FOLDER
from services.instagram_service import list_videos

router = APIRouter()


@router.get("/", summary="List all downloaded videos")
def get_videos():
    videos = list_videos()
    result = []
    for v in videos:
        path = os.path.join(VIDEO_FOLDER, v)
        size_mb = round(os.path.getsize(path) / (1024 * 1024), 2)
        result.append({"filename": v, "size_mb": size_mb})
    return {"count": len(result), "videos": result}


@router.get("/{filename}", summary="Download a specific video file")
def get_video(filename: str):
    path = os.path.join(VIDEO_FOLDER, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Video not found.")
    return FileResponse(path, media_type="video/mp4", filename=filename)


@router.delete("/{filename}", summary="Delete a video file")
def delete_video(filename: str):
    path = os.path.join(VIDEO_FOLDER, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Video not found.")
    os.remove(path)
    return {"success": True, "message": f"'{filename}' deleted."}
