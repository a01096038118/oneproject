import os
import uuid
from datetime import datetime

# 고정 절대 경로 폴더 지정
OCEAN_RESCUE_DIR = r"C:\ocean_rescue_images"

if not os.path.exists(OCEAN_RESCUE_DIR):
    os.makedirs(OCEAN_RESCUE_DIR)

def save_images(image_file):
    """
    [이미지 저장 엔진 복수형 s 적용 완료!] 
    드론이 준 이미지를 C:\ocean_rescue_images 폴더에 물리 저장합니다.
    파일명 포맷: 년-월-일_시분초_rescue_고유ID.확장자
    """
    if not image_file or image_file.filename == '':
        return None

    # os.path.splitext는 (파일명, 확장자) 튜플을 반환하므로 [1]을 붙여 확장자 문자열만 추출합니다.
    file_extension = os.path.splitext(image_file.filename)[1]
    
    # 년-월-일_시분초 포맷 생성
    formatted_time = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    
    # 파일명 겹침 방지용 8자리 고유 식별자
    unique_id = uuid.uuid4().hex[:8]
    
    # 요구사항에 맞춘 최종 파일명 조합
    rescue_filename = f"{formatted_time}_rescue_{unique_id}{file_extension}"

    # 최종 물리 저장 절대 경로 결합
    physical_storage_path = os.path.join(OCEAN_RESCUE_DIR, rescue_filename)
    
    # 이미지 파일 저장
    image_file.save(physical_storage_path)

    # DB에 저장할 웹 서버 매핑용 상대 경로 반환
    db_relative_url = f"external_img/{rescue_filename}"
    return db_relative_url