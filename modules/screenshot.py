import cv2
import os
import time
from modules.camera_source import get_camera
from config import FRAME_WIDTH, FRAME_HEIGHT
from modules.logger import get_logger

log = get_logger("screenshot")

SCREENSHOT_DIR = os.path.join("static", "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def take_screenshot(rtsp: bool = False):
    """
    Робить скріншот з камери (локальної або RTSP) і зберігає у static/screenshots.
    Повертає шлях до файлу.
    """
    cap = get_camera(rtsp)
    if not cap or not cap.isOpened():
        log.error("Не вдалося відкрити камеру для скріншоту")
        return None

    success, frame = cap.read()
    cap.release()

    if not success or frame is None:
        log.error("Не вдалося зчитати кадр для скріншоту")
        return None

    resized = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
    filename = f"screenshot_{int(time.time())}.jpg"
    filepath = os.path.join(SCREENSHOT_DIR, filename)

    cv2.imwrite(filepath, resized)
    log.info("Скріншот збережено: %s", filepath)

    # Оновлюємо "last.jpg" для маршруту /last_screenshot
    last_path = os.path.join(SCREENSHOT_DIR, "last.jpg")
    cv2.imwrite(last_path, resized)

    return filepath
