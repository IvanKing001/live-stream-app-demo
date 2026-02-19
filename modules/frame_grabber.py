import cv2

class FrameGrabber:
    def __init__(self):
        self.cap = None

    def start(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)

    def get_frame(self):
        if self.cap is None or not self.cap.isOpened():
            raise Exception("Камера не підключена")

        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame

    def stop(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def is_running(self):
        return self.cap is not None and self.cap.isOpened()
