import cv2
import threading
from ultralytics import YOLO

camera = None
camera_lock = threading.Lock()

model = YOLO("yolov8n.pt")

def reconnect_camera():

    global camera

    print("camera reconnecting...")

    try:
        if camera is not None:
            camera.release()
    except:
        pass
            
    camera = cv2.VideoCapture(EXP_STREAM_URL)

    print("camera reconnected")
        

def get_frame():

    global camera

    if camera is None:
        return None
    
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