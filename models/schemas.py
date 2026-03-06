from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

class SchedulerStatus(str, Enum):
    running = "running"
    stopped = "stopped"

class DownloadRequest(BaseModel):
    username: Optional[str] = None  # overrides config if provided

class InstagramCredentials(BaseModel):
    username: str
    password: str

class PostRequest(BaseModel):
    video_filename: Optional[str] = None  # if None, picks random

class ScheduleConfig(BaseModel):
    times: List[str]  # list of "HH:MM" strings

class VideoInfo(BaseModel):
    filename: str
    size_mb: float
    path: str

class StatusResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None
