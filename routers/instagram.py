from fastapi import APIRouter, HTTPException
from models.schemas import PostRequest, InstagramCredentials, StatusResponse
from services import instagram_service

router = APIRouter()


@router.post("/login", summary="Login to Instagram (updates session)")
def login(creds: InstagramCredentials):
    try:
        instagram_service.reset_client()
        instagram_service.get_client(creds.username, creds.password)
        return StatusResponse(success=True, message="Logged in successfully.")
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/post", summary="Post a video to Instagram Reels")
def post(body: PostRequest):
    try:
        result = instagram_service.post_video(body.video_filename)
        return StatusResponse(success=True, message="Video posted.", data=result)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/logout", summary="Reset Instagram session")
def logout():
    instagram_service.reset_client()
    return StatusResponse(success=True, message="Session cleared.")
