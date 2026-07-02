import os
import uuid
import cv2
from datetime import datetime

OCEAN_RESCUE_DIR = r"C:\ocean_rescue_images"

if not os.path.exists(OCEAN_RESCUE_DIR):
    os.makedirs(OCEAN_RESCUE_DIR)

# OpenCV frame 저장, 로그 저장용 연결 함수

def save_frame_image(frame):
    
    # file 이름 만들기
    formatted_time = datetime.now().strftime("%Y-%m-%d_%H%M%S")

    unique_id = uuid.uuid4().hex[:8]

    rescue_filename = f"{formatted_time}_rescue_{unique_id}.jpg"

    physical_storage_path = os.path.join(
        OCEAN_RESCUE_DIR,
        rescue_filename
    )

def save_frame_logs(frame):
    pass
