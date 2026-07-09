import os
import uuid
import cv2
import json
import csv
from datetime import datetime
import config

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

LOG_DIR = os.path.join(PROJECT_ROOT, "json")

os.makedirs(LOG_DIR, exist_ok=True)

LOG_DB_PATH = os.path.join(LOG_DIR, "capture_logs.json")
EXCEL_REPORT_PATH = os.path.join(LOG_DIR, "rescue_report.csv")

os.makedirs(config.OCEAN_RESCUE_DIR, exist_ok=True)

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def create_image_filename():
    formatted_time = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    unique_id = uuid.uuid4().hex[:8]
    rescue_filename = f"{formatted_time}_rescue_{unique_id}.jpg"

    return rescue_filename

# 저장된 로그 전체 조회 
def get_logs():
  
    if not os.path.exists(LOG_DB_PATH):
        return []

    try:
        with open(LOG_DB_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
        
    except (json.JSONDecodeError, IOError):
        return []

def save_logs(logs):
    with open(LOG_DB_PATH, "w", encoding="utf-8") as file:
        json.dump(
            logs,
            file,
            ensure_ascii=False,
            indent=4
        )

def create_log_data(saved_image_url, detected_zone, person_count):
    new_log = {
        "log_id": f'LOG_{uuid.uuid4().hex[:8].upper()}',
        "message": "위험구역 침범 감지",
        "detected_time": get_current_time(),

        "zone_id": detected_zone["zone_id"],
        "danger_zone": detected_zone,
        "person_count": person_count,

        "captured_image_path": saved_image_url,

        "manager": None,
        "checked_time": None
    }

    return new_log

# OpenCV frame 이미지 저장
def save_frame_image(frame):
    
    rescue_filename = create_image_filename()

    # 파일 저장 위치 정하기
    physical_storage_path = os.path.join(
        config.OCEAN_RESCUE_DIR,
        rescue_filename
    )

    success = cv2.imwrite(physical_storage_path, frame)

    if not success:
        return None
    
    db_relative_url = f'external_img/{rescue_filename}'
    return db_relative_url

# 로그 저장용 연결 함수
def save_frame_logs(frame, detected_zone, person_count):
    
    if detected_zone is None:
        return {
            "success": False,
            "message": "감지된 위험구역 정보가 없습니다."
            }
    
    saved_image_url = save_frame_image(frame)

    if not saved_image_url:
        return {
            "success": False,
            "message": "이미지 저장 실패"
            }
    
    # 기존 JSON 로그 읽기
    incident_logs = get_logs()

    # 새 로그 한 건 생성
    new_log = create_log_data(
        saved_image_url,
        detected_zone,
        person_count
    )

    # JSON 리스트에 새 로그 추가
    incident_logs.append(new_log)

    # JSON 파일로 저장
    save_logs(incident_logs)

    return {
        "success": True,
        "log_data": new_log
    }  

# log_id 기준 로그 삭제
def delete_log(log_id):

    logs = get_logs()

    new_logs = []

    for log in logs:
        if log["log_id"] != log_id:
            new_logs.append(log)

    if len(logs) == len(new_logs):
        return {
            "success": False,
            "message": "삭제할 로그를 찾을 수 없습니다."
        }

    save_logs(new_logs)

    return {
        "success": True,
        "message": "로그 삭제 완료",
        "deleted_log_id": log_id
    }

# log_id 기준 로그 확인 처리
def check_log(log_id, manager):

    logs = get_logs()

    for log in logs:
        if log["log_id"] == log_id:
            log["manager"] = manager
            log["checked_time"] = get_current_time()

            save_logs(logs)

            return {
                "success": True,
                "message": "로그 확인 처리 완료",
                "checked_log": log
            }

    return {
        "success": False,
        "message": "확인 처리할 로그를 찾을 수 없습니다."
    }

def create_csv_report():
    logs = get_logs()

    with open(EXCEL_REPORT_PATH, mode="w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)

        writer.writerow([
            "로그 ID",
            "메시지",
            "감지 시각",
            "구역 ID",
            "위험구역",
            "감지 인원",
            "이미지 확인 링크",
            "담당자",
            "확인 시각"
        ])

        for log in logs:
            filename = log["captured_image_path"].split("/")[-1]
            image_path = os.path.join(config.OCEAN_RESCUE_DIR, filename)

            writer.writerow([
                log["log_id"],
                log["message"],
                log["detected_time"],
                log["zone_id"],
                str(log["danger_zone"]),
                log["person_count"],
                image_path,
                log["manager"],
                log["checked_time"]
            ])

    return EXCEL_REPORT_PATH