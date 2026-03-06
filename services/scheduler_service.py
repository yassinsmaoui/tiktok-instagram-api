from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from config import POST_TIMES
import logging

logger = logging.getLogger(__name__)


def _post_job():
    """Job executed by the scheduler."""
    try:
        from services.instagram_service import post_video
        result = post_video()
        logger.info(f"Scheduled post success: {result['uploaded']}")
    except Exception as e:
        logger.error(f"Scheduled post failed: {e}")


class SchedulerService:
    def __init__(self):
        self._scheduler = BackgroundScheduler()
        self._times = list(POST_TIMES)
        self._running = False

    def start(self):
        if not self._running:
            self._load_jobs()
            self._scheduler.start()
            self._running = True
            logger.info("Scheduler started.")

    def stop(self):
        if self._running:
            self._scheduler.shutdown(wait=False)
            self._running = False
            logger.info("Scheduler stopped.")

    def _load_jobs(self):
        self._scheduler.remove_all_jobs()
        for t in self._times:
            hour, minute = t.split(":")
            self._scheduler.add_job(
                _post_job,
                CronTrigger(hour=int(hour), minute=int(minute)),
                id=f"post_{t}",
                replace_existing=True,
            )

    def update_times(self, times: list[str]):
        self._times = times
        if self._running:
            self._load_jobs()

    def get_status(self) -> dict:
        jobs = []
        for job in self._scheduler.get_jobs():
            jobs.append({
                "id": job.id,
                "next_run": str(job.next_run_time) if job.next_run_time else None,
            })
        return {
            "running": self._running,
            "times": self._times,
            "jobs": jobs,
        }

    def trigger_now(self):
        """Manually trigger a post immediately."""
        _post_job()


scheduler_service = SchedulerService()
