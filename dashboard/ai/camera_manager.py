import cv2
import threading
from ultralytics import YOLO
from datetime import datetime, timedelta
import time
from dashboard.utils.log_manager import save_frame_logs
from dashboard import config
from dashboard.ai.zone_manager import is_object_in_zone
from dashboard.ai.drawing_manager import (
    draw_danger_zones,
    draw_detected_objects,
    draw_intrusion_alert
)

class CameraManager:

    def __init__(self):
        self.camera = None
        self.camera_lock = threading.Lock()
        self.model = YOLO(config.YOLO_MODEL_PATH)
        self.last_intrusion_time_by_zone = {}

    def init_camera(self):

        if self.camera is None:
            print("camera connecting...")

            self.camera = cv2.VideoCapture(config.ESP32_STREAM_URL)
            print("camera connected")
    
    def reconnect_camera(self):

        print("camera reconnecting...")

        try:
            if self.camera is not None:
                self.camera.release()

        except Exception as e:
            print("camera release exception:", e)
                
        self.camera = cv2.VideoCapture(config.ESP32_STREAM_URL)

        print("camera reconnected")

    def is_camera_available(self):

        if self.camera is None:
            self.init_camera()

        if not self.camera.isOpened():
            self.reconnect_camera()
            return False

        return True
    
    def read_camera_frame(self):

        with self.camera_lock:
            success, frame = self.camera.read()

        if not success:
            print("camera frame read failed")
            self.reconnect_camera()
            return None

        return frame
        
    def detect_objects(self, frame):

        detected_zones = {}
        detected_people = []

        results = self.model(
            frame,
            verbose=False
        )

        detection_result = results[0]

        for box in detection_result.boxes:

            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            if confidence < config.YOLO_CONFIDENCE_THRESHOLD:
                continue

            class_name = self.model.names[class_id]

            x1, y1, x2, y2 = box.xyxy[0]

            x1 = int(x1)
            y1 = int(y1)
            x2 = int(x2)
            y2 = int(y2)

            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2

            detected_people.append({
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2,
                "center_x": center_x,
                "center_y": center_y,
                "confidence": confidence,
                "class_name": class_name
            })

            if class_name != config.DANGER_TARGET_CLASS:
                continue

            for zone in config.DANGER_ZONES:
                if is_object_in_zone(center_x, center_y, zone):
                    zone_id = zone["zone_id"]

                    if zone_id not in detected_zones:
                        detected_zones[zone_id] = {
                            "zone": zone,
                            "person_count": 0
                        }

                    detected_zones[zone_id]["person_count"] += 1
                    break

        return detected_people, detected_zones
    
    def save_intrusion_log(self, frame, detected_zone, person_count):

        result = save_frame_logs(frame, detected_zone, person_count)

        return result
    
    def save_detected_zone_logs(self, frame, detected_zones):

        now = datetime.now()

        for zone_data in detected_zones.values():
            zone_id = zone_data["zone"]["zone_id"]

            last_time = self.last_intrusion_time_by_zone.get(zone_id)

            if (
                last_time is None
                or now - last_time > timedelta(
                    seconds=config.INTRUSION_LOG_INTERVAL_SECONDS
                )
            ):
                self.save_intrusion_log(
                    frame,
                    zone_data["zone"],
                    zone_data["person_count"]
                )

                self.last_intrusion_time_by_zone[zone_id] = now

    def get_frame(self):

        try:

            if not self.is_camera_available():
                return None
            
            frame = self.read_camera_frame()

            if frame is None:
                return None

            # YOLO 객체 탐지 수행
            detected_people, detected_zones = self.detect_objects(frame)

            # 모든 위험구역 표시
            draw_danger_zones(frame, detected_zones)

            # 탐지된 모든 객체 표시
            draw_detected_objects(frame, detected_people)

            if detected_zones:
                # 침입 알림 표시 및 로그 저장
                draw_intrusion_alert(frame)

                # 마지막 저장 이후 5초 경과 여부 확인
                self.save_detected_zone_logs(frame, detected_zones)    

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
