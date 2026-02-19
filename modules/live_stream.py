from flask import Flask, Response, render_template, redirect, url_for
import cv2
import os
import time
from modules.frame_grabber import FrameGrabber

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

app = Flask(__name__, template_folder=TEMPLATES_DIR)

fg = FrameGrabber()
camera_status = "Зупинена"
recording = False
video_writer = None



os.makedirs("captures", exist_ok=True)
os.makedirs("recordings", exist_ok=True)

def generate_frames():
    global video_writer, recording
    while fg.is_running():
        frame = fg.get_frame()
        if frame is None:
            continue
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue

        
        if recording and video_writer is not None:
            video_writer.write(frame)

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/')
def index():
    return render_template("index.html", status=camera_status, recording=recording)

@app.route('/start_camera')
def start_camera():
    global camera_status
    fg.start()
    camera_status = "Запущена"
    return redirect(url_for('index'))

@app.route('/stop_camera')
def stop_camera():
    global camera_status, recording, video_writer
    fg.stop()
    camera_status = "Зупинена"
    if recording:
        recording = False
        if video_writer is not None:
            video_writer.release()
            video_writer = None
    return redirect(url_for('index'))

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture_photo')
def capture_photo():
    frame = fg.get_frame()
    if frame is not None:
        filename = f"captures/photo_{int(time.time())}.jpg"
        cv2.imwrite(filename, frame)
    return redirect(url_for('index'))

@app.route('/start_recording')
def start_recording():
    global recording, video_writer
    if fg.is_running() and not recording:
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        filename = f"recordings/video_{int(time.time())}.avi"
        video_writer = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))
        recording = True
    return redirect(url_for('index'))

@app.route('/stop_recording')
def stop_recording():
    global recording, video_writer
    if recording:
        recording = False
        if video_writer is not None:
            video_writer.release()
            video_writer = None
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
