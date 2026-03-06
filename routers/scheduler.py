from fastapi import APIRouter, HTTPException
from models.schemas import ScheduleConfig, StatusResponse
from services.scheduler_service import scheduler_service

router = APIRouter()


@router.get("/status", summary="Get scheduler status and next runs")
def status():
    return scheduler_service.get_status()


@router.post("/start", summary="Start the scheduler")
def start():
    scheduler_service.start()
    return StatusResponse(success=True, message="Scheduler started.")


@router.post("/stop", summary="Stop the scheduler")
def stop():
    scheduler_service.stop()
    return StatusResponse(success=True, message="Scheduler stopped.")


@router.put("/times", summary="Update posting schedule times")
def update_times(body: ScheduleConfig):
    # Validate HH:MM format
    import re
    for t in body.times:
        if not re.match(r"^\d{2}:\d{2}$", t):
            raise HTTPException(status_code=400, detail=f"Invalid time format: '{t}'. Use HH:MM.")
    scheduler_service.update_times(body.times)
    return StatusResponse(success=True, message="Schedule updated.", data={"times": body.times})


@router.post("/trigger", summary="Manually trigger an Instagram post now")
def trigger():
    try:
        scheduler_service.trigger_now()
        return StatusResponse(success=True, message="Post triggered manually.")
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=str(e))
