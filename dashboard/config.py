# ESP32 카메라 설정
# TODO: 실제 ESP32 스트림 주소 입력
ESP32_STREAM_URL = None

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

# 이미지 저장 경로
OCEAN_RESCUE_DIR = r"C:\ocean_rescue_images"