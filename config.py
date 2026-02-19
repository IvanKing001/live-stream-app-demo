from pathlib import Path
import os

# Базові директорії
BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"
SCREENSHOT_FOLDER = STATIC_DIR / "screenshots"
RECORDING_FOLDER = STATIC_DIR / "recordings"
LOGS_DIR = BASE_DIR / "logs"
LOG_FILE = LOGS_DIR / "events.log"

# Переконайся, що папки існують
os.makedirs(SCREENSHOT_FOLDER, exist_ok=True)
os.makedirs(RECORDING_FOLDER, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# Камери
CAMERA_INDEX = 0  # локальна вебкамера
CAMERA_RTSP = "rtsp://user:password@IP:554/stream"  # замінити на реальні дані

# Налаштування запису
FRAME_WIDTH = 640          # ширина кадру
FRAME_HEIGHT = 480         # висота кадру
FPS = 20                   # кадрів на секунду
DEFAULT_RECORD_DURATION = 10  # секунд
VIDEO_CODEC = "XVID"       # варіанти: "XVID", "MJPG"

# Планувальник
SCHEDULE_HOUR = 9
SCHEDULE_MINUTE = 0
SCHEDULE_RTSP = False  # True = RTSP, False = локальна

# Сервер
HOST = "0.0.0.0"
PORT = 5000
