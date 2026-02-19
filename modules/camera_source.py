import cv2
from config import CAMERA_INDEX, CAMERA_RTSP
from modules.logger import get_logger

log = get_logger("camera_source")

def get_camera(rtsp: bool = False):
    """
    Повертає об'єкт cv2.VideoCapture для локальної або RTSP камери.
    rtsp=True -> використовує RTSP‑потік
    rtsp=False -> локальна вебкамера (CAMERA_INDEX)
    """
    if rtsp:
        log.info("Відкриваю RTSP камеру: %s", CAMERA_RTSP)
        cap = cv2.VideoCapture(CAMERA_RTSP)
    else:
        log.info("Відкриваю локальну камеру: index=%s", CAMERA_INDEX)
        cap = cv2.VideoCapture(CAMERA_INDEX)

    if not cap or not cap.isOpened():
        log.error("Не вдалося відкрити камеру (rtsp=%s)", rtsp)
        return None

    log.info("Камера успішно відкрита (rtsp=%s)", rtsp)
    return cap
