import cv2
import os
import time
import threading
from modules.frame_grabber import get_frame
from config import FRAME_WIDTH, FRAME_HEIGHT, FPS
from modules.logger import get_logger

log = get_logger("recorder")

RECORDINGS_DIR = os.path.join("static", "recordings")
os.makedirs(RECORDINGS_DIR, exist_ok=True)

motion_writer = None
motion_thread = None
motion_active = False

def start_test_recording(rtsp: bool = False, duration: int = 5):
    """
    Записує відео протягом duration секунд (для планових записів).
    """
    filename = f"recording_{int(time.time())}.avi"
    filepath = os.path.join(RECORDINGS_DIR, filename)

    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    writer = cv2.VideoWriter(filepath, fourcc, FPS, (FRAME_WIDTH, FRAME_HEIGHT))

    start_time = time.time()
    while True:
        frame = get_frame()
        if frame is None:
            continue
        resized = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
        writer.write(resized)

        if duration and (time.time() - start_time) > duration:
            break

    writer.release()

    last_path = os.path.join(RECORDINGS_DIR, "last.avi")
    try:
        os.replace(filepath, last_path)
    except Exception as e:
        log.error("Не вдалося оновити last.avi: %s", e)

    log.info("Тестовий запис збережено: %s", filepath)
    return filepath

def _record_loop(filename: str):
    global motion_writer, motion_active

    filepath = os.path.join(RECORDINGS_DIR, filename)
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    motion_writer = cv2.VideoWriter(filepath, fourcc, FPS, (FRAME_WIDTH, FRAME_HEIGHT))

    log.info("Запис стартував: %s", filepath)
    motion_active = True

    while motion_active:
        frame = get_frame()
        if frame is None:
            continue
        resized = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
        motion_writer.write(resized)

    motion_writer.release()

    last_path = os.path.join(RECORDINGS_DIR, "last.avi")
    try:
        os.replace(filepath, filepath)
    except Exception as e:
        log.error("Не вдалося оновити last.avi: %s", e)

    log.info("Запис завершено: %s", filepath)

def start_motion_recording():
    global motion_thread
    filename = f"motion_{int(time.time())}.avi"
    motion_thread = threading.Thread(target=_record_loop, args=(filename,))
    motion_thread.daemon = True
    motion_thread.start()
    return filename

def stop_motion_recording():
    global motion_active
    motion_active = False
    log.info("Запис при русі зупинено")
