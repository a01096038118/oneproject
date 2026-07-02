import cv2
import threading
from ultralytics import YOLO
from datetime import datetime, timedelta, time
import tempfile
import os

camera = None
camera_lock = threading.Lock()

model = YOLO("yolov8n.pt")

last_intrusion_time = None

EXP32_STREAM_URL = None

DANGER_X1 = 250
DANGER_Y1 = 100
DANGER_X2 = 550
DANGER_Y2 = 350

def save_intrusion_log():
    pass

def init_camera():
    
    global camera

    if camera is None:
        print("camera reconnecting...")
        camera = cv2.VideoCapture(EXP32_STREAM_URL)
        print("camera reconnected")


def reconnect_camera():

    global camera

    print("camera reconnecting...")

    try:
        if camera is not None:
            camera.release()
    except:
        pass
            
    camera = cv2.VideoCapture(EXP32_STREAM_URL)

    print("camera reconnected")
        

def get_frame():

    global camera

    if camera is None:
        return None
    
    try:
    
        if not camera.isOpened():
            reconnect_camera()
            return None
        
        with camera_lock:
            success, frame = camera.read()

        if not success:
            return None

        is_intrusion = False

        results = model(
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

            if (
                DANGER_X1 <= center_x <= DANGER_X2
                and
                DANGER_Y1 <= center_y <= DANGER_Y2
            ):
                is_intrusion = True
            
        danger_color = (0, 0, 255)

        if is_intrusion:
            danger_color = (0, 255, 255)

            # 사람 박스 표시
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

            # 중심점 표시
            cv2.circle(
                frame,
                (center_x, center_y),
                5,
                (255, 0, 0),
                -1
            )

            # 위험구역 표시
            cv2.rectangle(
                frame,
                (DANGER_X1, DANGER_Y1),
                (DANGER_X2, DANGER_Y2),
                danger_color,
                3
            )

            cv2.putText(
                frame,
                "DANGER ZONE",
                (DANGER_X1, DANGER_Y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                danger_color,
                2
            )

            # 침입 발생
            if is_intrusion:

                cv2.putText(
                    frame,
                    "PERSON INTRUSION",
                    (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    3
                )

                now = datetime.now()

                if(
                    last_intrusion_time is None
                    or
                    now - last_intrusion_time >
                    timedelta(seconds=5)
                ):
                    save_intrusion_log()

                    last_intrusion_time = now

            return frame    

    except Exception as e:

        print("camera exception:", e)
    
        reconnect_camera()
    
        return None
        
def generate_frame():

    while True:

        frame = get_frame()

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