import cv2
import threading
from ultralytics import YOLO
from datetime import datetime, timedelta
import time
import config
from utils.log_manager import save_frame_logs

class CameraManager:

    def __init__(self):
        self.camera = None
        self.camera_lock = threading.Lock()
        self.model = YOLO("yolov8n.pt")
        self.last_intrusion_time = None

    # 침입 감지 시 frame 로그 저장 연결 함수
    def save_intrusion_log(self, frame, detected_zone):

        result = save_frame_logs(frame, detected_zone)

        return result

    def init_camera(self):

        if self.camera is None:
            print("camera reconnecting...")
            self.camera = cv2.VideoCapture(config.ESP32_STREAM_URL)
            print("camera reconnected")


    def reconnect_camera(self):

        print("camera reconnecting...")

        try:
            if self.camera is not None:
                self.camera.release()
        except:
            pass
                
        self.camera = cv2.VideoCapture(config.ESP32_STREAM_URL)

        print("camera reconnected")
        

    def get_frame(self):

        if self.camera is None:
            self.init_camera()
        
        try:
        
            if not self.camera.isOpened():
                self.reconnect_camera()
                return None
            
            with self.camera_lock:
                success, frame = self.camera.read()

            if not success:
                return None

            is_intrusion = False

            detected_zone = None

            # YOLO 객체 탐지 수행
            results = self.model(
                frame,
                verbose=False
            )

            result = results[0]

            for box in result.boxes:

                class_id = int(box.cls[0])
                confidence = float(box.conf[0])

                if class_id != 0:
                    continue

                if confidence < 0.8:
                    continue

                x1, y1, x2, y2 = box.xyxy[0]

                x1 = int(x1)
                y1 = int(y1)
                x2 = int(x2)
                y2 = int(y2)

                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2

                for zone in config.DANGER_ZONES:
                    if (
                        zone["x1"] <= center_x <= zone["x2"]
                        and
                        zone["y1"] <= center_y <= zone["y2"]
                    ):
                        is_intrusion = True
                        detected_zone = zone
                        break
                
            danger_color = (0, 0, 255)

            if is_intrusion:
                danger_color = (0, 255, 255)

            # 모든 위험구역 표시
            for zone in config.DANGER_ZONES:
                cv2.rectangle(
                    frame,
                    (zone["x1"], zone["y1"]),
                    (zone["x2"], zone["y2"]),
                    danger_color,
                    3
                )

                cv2.putText(
                    frame,
                    zone["zone_id"],
                    (zone["x1"], zone["y1"] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    danger_color,
                    2
                )

            if is_intrusion:

                # 침입 객체 표시
                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    f'person{confidence: .2f}',
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )

                cv2.circle(
                    frame,
                    (center_x, center_y),
                    5,
                    (255, 0, 0),
                    -1
                )
            
                # 침입 알림 표시 및 로그 저장
                cv2.putText(
                    frame,
                    "PERSON INTRUSION",
                    (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    3
                )

                # 마지막 저장 이후 5초 경과 여부 확인
                now = datetime.now()

                if(
                    self.last_intrusion_time is None
                    or
                    now - self.last_intrusion_time >
                    timedelta(seconds=5)
                ):
                    self.save_intrusion_log(frame, detected_zone)

                    self.last_intrusion_time = now

            return frame    

        except Exception as e:

            print("camera exception:", e)
        
            self.reconnect_camera()
        
            return None
            
    def generate_frame(self):

        while True:

            frame = self.get_frame()

            if frame is None:
                time.sleep(0.1)
                continue

            ret, buffer = cv2.imencode(".jpg", frame)

            if not ret:
                time.sleep(0.1)
                continue

            frame_bytes = buffer.tobytes()

            yield(
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n'
                + frame_bytes +
                b'\r\n'
            )

            time.sleep(0.03)

camera_manager = CameraManager()

def generate_frame():
    return camera_manager.generate_frame()
