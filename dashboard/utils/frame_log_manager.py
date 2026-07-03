import os
import uuid
import cv2
import json
from datetime import datetime

OCEAN_RESCUE_DIR = r"C:\ocean_rescue_images"

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

LOG_DIR = os.path.join(PROJECT_ROOT, "json")

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_DB_PATH = os.path.join(LOG_DIR, "capture_logs.json")

if not os.path.exists(OCEAN_RESCUE_DIR):
    os.makedirs(OCEAN_RESCUE_DIR)

# OpenCV frame 이미지 저장
def save_frame_image(frame):
    
    # 파일 이름 만들기
    formatted_time = datetime.now().strftime("%Y-%m-%d_%H%M%S")

    unique_id = uuid.uuid4().hex[:8]

    rescue_filename = f"{formatted_time}_rescue_{unique_id}.jpg"

    # 파일 저장 위치 정하기
    physical_storage_path = os.path.join(
        OCEAN_RESCUE_DIR,
        rescue_filename
    )

    success = cv2.imwrite(physical_storage_path, frame)

    if not success:
        return None
    
    db_relative_url = f'external_img/{rescue_filename}'
    return db_relative_url

# 로그 저장용 연결 함수
def save_frame_logs(frame):
    
    saved_image_url = save_frame_image(frame)

    if not saved_image_url:
        return {
            "success": False,
            "message": "이미지 저장 실패"
            }
    
    if os.path.exists(LOG_DB_PATH):
        try:
            with open(LOG_DB_PATH, "r", encoding="utf-8") as file:
                incident_logs = json.load(file)

        except json.JSONDecodeError:
            incident_logs = []
