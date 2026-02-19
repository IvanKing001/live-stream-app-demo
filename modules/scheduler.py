from apscheduler.schedulers.background import BackgroundScheduler
from config import SCHEDULE_HOUR, SCHEDULE_MINUTE, SCHEDULE_RTSP
from modules.recorder import start_test_recording
from modules.logger import get_logger

log = get_logger("scheduler")

scheduler = BackgroundScheduler()

def schedule_daily_recording():
    """Запускає щоденний запис у заданий час."""
    scheduler.add_job(
        lambda: start_test_recording(rtsp=SCHEDULE_RTSP),
        "cron",
        hour=SCHEDULE_HOUR,
        minute=SCHEDULE_MINUTE,
        id="daily_recording",
        replace_existing=True
    )
    log.info("Заплановано щоденний запис о %02d:%02d", SCHEDULE_HOUR, SCHEDULE_MINUTE)

def start_scheduler():
    """Стартує планувальник у фоні."""
    scheduler.start()
    log.info("Планувальник запущено")
