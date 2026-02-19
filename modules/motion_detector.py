import cv2
import time
from modules.camera_source import get_camera
from modules.recorder import start_motion_recording, stop_motion_recording
from modules.logger import get_logger

log = get_logger("motion")

# Фіксовані параметри
MIN_RECORD_TIME = 5      # мінімальний час запису після руху (секунди)
MAX_RECORD_TIME = 60     # максимальний час безперервного запису (секунди)
THRESHOLD = 5000         # чутливість детектора

def detect_motion(rtsp: bool = False):
    """
    Детекція руху: запускає/зупиняє запис залежно від руху.
    Використовує фіксовані параметри MIN_RECORD_TIME, MAX_RECORD_TIME та THRESHOLD.
    """
    cap = get_camera(rtsp)
    if not cap or not cap.isOpened():
        log.error("Не вдалося відкрити камеру для детекції руху")
        return

    recording = False
    prev_frame = None
    last_motion_time = 0
    record_start_time = 0

    while True:
        success, frame = cap.read()
        if not success:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if prev_frame is None:
            prev_frame = gray
            continue

        diff = cv2.absdiff(prev_frame, gray)
        thresh_img = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
        motion_level = cv2.countNonZero(thresh_img)

        if motion_level > THRESHOLD:
            last_motion_time = time.time()
            if not recording:
                log.info("Рух виявлено — старт запису")
                start_motion_recording(rtsp)
                recording = True
                record_start_time = time.time()

        elif recording:
            # якщо рух зник і минув мінімальний час
            if (time.time() - last_motion_time > MIN_RECORD_TIME) or \
               (time.time() - record_start_time > MAX_RECORD_TIME):
                log.info("Зупинка запису (рух зник або досягнуто максимум)")
                stop_motion_recording()
                recording = False

        prev_frame = gray
        time.sleep(0.1)

    cap.release()
