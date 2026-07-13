import os

# config.py 파일이 있는 dashboard 폴더의 절대 경로
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ESP32 카메라 설정
ESP32_STREAM_URL = "http://192.168.137.181:81/stream"

# YOLO 모델 설정
YOLO_MODEL_PATH = os.path.join(
    BASE_DIR,
    "ai",
    "models",
    "best.pt"
)
YOLO_CONFIDENCE_THRESHOLD = 0.6
DANGER_TARGET_CLASS = "victim"

# 위험구역 설정
DANGER_ZONES = [
    {
        "zone_id": "ZONE_001",
        "x1": 30,
        "y1": 240,
        "x2": 340,
        "y2": 470
    },
    {
        "zone_id": "ZONE_002",
        "x1": 360,
        "y1": 30,
        "x2": 610,
        "y2": 240
    }
]

# 침입 알림 표시 설정
INTRUSION_ALERT_TEXT = "VICTIM INTRUSION"
INTRUSION_LOG_INTERVAL_SECONDS = 5

INTRUSION_TEXT_POSITION = (30, 50)
INTRUSION_TEXT_SCALE = 1
INTRUSION_TEXT_COLOR = (0, 0, 255)
INTRUSION_TEXT_THICKNESS = 3

# 화면 표시 설정
DANGER_ZONE_NORMAL_COLOR = (0, 0, 255)
DANGER_ZONE_DETECTED_COLOR = (0, 255, 255)
OBJECT_BOX_COLOR = (0, 255, 0)
CENTER_POINT_COLOR = (255, 0, 0)

DANGER_ZONE_BOX_THICKNESS = 3
OBJECT_BOX_THICKNESS = 2
TEXT_THICKNESS = 2
CENTER_POINT_RADIUS = 5

# 이미지 저장 경로
OCEAN_RESCUE_DIR = r"C:\ocean_rescue_images"