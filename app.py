from flask import Flask, Response, render_template, redirect, url_for
import cv2
from modules.frame_grabber import FrameGrabber

app = Flask(__name__)
fg = FrameGrabber()
camera_status = "Зупинена"

def generate_frames():
    while fg.is_running():
        frame = fg.get_frame()
        if frame is None:
            continue
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/')
def index():
    return render_template("index.html", status=camera_status)

@app.route('/start_camera')
def start_camera():
    global camera_status
    fg.start()
    camera_status = "Запущена"
    return redirect(url_for('index'))

@app.route('/stop_camera')
def stop_camera():
    global camera_status
    fg.stop()
    camera_status = "Зупинена"
    return redirect(url_for('index'))

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
