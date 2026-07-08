# ESP32 카메라 설정
ESP32_STREAM_URL = "http://192.168.137.89:81/stream"

# YOLO 모델 설정
YOLO_MODEL_PATH = "ai/models/best.pt"
YOLO_CONFIDENCE_THRESHOLD = 0.8
DANGER_TARGET_CLASS = "swimmer"

# 위험구역 설정
DANGER_ZONES = [
    {
        "zone_id": "ZONE_001",
        "x1": 250,
        "y1": 100,
        "x2": 550,
        "y2": 350
    },
    {
        "zone_id": "ZONE_002",
        "x1": 100,
        "y1": 400,
        "x2": 300,
        "y2": 550
    }
]

# 침입 알림 표시 설정
INTRUSION_ALERT_TEXT = "SWIMMER INTRUSION"
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