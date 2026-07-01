import os
import json
import csv
import uuid
from datetime import datetime

# 같은 폴더(db/utils)에 있는 image_handler에서 이미지 저장 함수 가져오기
from db.utils.image_handler import save_images

# 현재 파일 위치(db/utils) 기준으로 부모 폴더(DB 루트) 경로 계산
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__)) # db/utils
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..")) # DB 폴더

# 새로 만든 db/json/ 폴더 안의 파일 경로로 고정 설정
INCIDENT_LOG_DB_PATH = os.path.join(PROJECT_ROOT, "json", "capture_logs.json")
EXCEL_REPORT_PATH = os.path.join(PROJECT_ROOT, "json", "rescue_report.csv")


def _save_to_excel(new_incident):
    """[내부 함수] 엑셀 파일에 로그와 클릭 링크를 누적 추가"""
    file_exists = os.path.exists(EXCEL_REPORT_PATH)
    
    # 상대 경로에서 파일명만 추출
    filename = new_incident["captured_image_path"].split("/")[-1]
    
    # 엑셀 하이퍼링크 수식 조합 (C:\ocean_rescue_images 폴더 기반)
    excel_hyperlink = f'=HYPERLINK("C:\\ocean_rescue_images\\{filename}", "사진 열기 (클릭)")'
    
    with open(EXCEL_REPORT_PATH, mode="a", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        
        # 파일이 처음 생성될 때만 맨 윗줄에 헤더(컬럼 타이틀) 생성
        if not file_exists:
            writer.writerow(["사건 번호", "탐지 상태", "발생 시각", "이미지 확인 링크"])
            
        # 데이터 행 기록
        writer.writerow([
            new_incident["incident_id"],
            new_incident["detected_status"],
            new_incident["detected_time"],
            excel_hyperlink
        ])


def save_logs(image_file):
    """
    [저장 엔진] 이미지를 C 드라이브에 저장하고, 
    db/json 폴더 안의 JSON 파일과 엑셀 리포트에 로그를 동시에 기록합니다.
    """
    # 1. 이미지 핸들러 함수(save_images) 호출하여 물리 저장 및 상대 경로 획득
    saved_image_url = save_images(image_file)
    if not saved_image_url:
        return {"success": False, "message": "이미지 저장 실패"}

    # 2. 기존 JSON 데이터 읽기
    if os.path.exists(INCIDENT_LOG_DB_PATH):
        try:
            with open(INCIDENT_LOG_DB_PATH, "r", encoding="utf-8") as file:
                incident_logs = json.load(file)
        except json.JSONDecodeError:
            incident_logs = []
    else:
        incident_logs = []

    # 3. 새로운 데이터 객체 생성 (사건번호 및 파일명 중복 방지 완료)
    new_incident = {
        "incident_id": f"INC_{uuid.uuid4().hex[:8].upper()}", # 절대 안 겹치는 8자리 고유 사건 번호
        "detected_status": "Person_Detected",                 
        "detected_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), # 년-월-일 시:분:초
        "captured_image_path": saved_image_url               
    }

    # 4. JSON 파일 업데이트
    incident_logs.append(new_incident)
    with open(INCIDENT_LOG_DB_PATH, "w", encoding="utf-8") as file:
        json.dump(incident_logs, file, ensure_ascii=False, indent=4)

    # 5. 엑셀 파일 기록 실행
    _save_to_excel(new_incident)

    return {"success": True, "incident_data": new_incident}


def get_logs():
    """
    [조회 엔진] 대시보드 화면용으로 
    db/json 폴더 내부의 모든 로그 리스트를 읽어서 반환합니다.
    """
    if not os.path.exists(INCIDENT_LOG_DB_PATH):
        return []

    try:
        with open(INCIDENT_LOG_DB_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        return []
