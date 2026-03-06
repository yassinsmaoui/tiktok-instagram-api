from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from routers import tiktok, instagram, scheduler, videos

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start background scheduler on startup
    from services.scheduler_service import scheduler_service
    scheduler_service.start()
    yield
    scheduler_service.stop()

app = FastAPI(
    title="TikTok → Instagram Automation API",
    description="Download TikTok videos and auto-post them to Instagram",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tiktok.router, prefix="/tiktok", tags=["TikTok"])
app.include_router(instagram.router, prefix="/instagram", tags=["Instagram"])
app.include_router(scheduler.router, prefix="/scheduler", tags=["Scheduler"])
app.include_router(videos.router, prefix="/videos", tags=["Videos"])

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")
