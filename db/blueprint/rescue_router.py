import os
from flask import Blueprint, request, jsonify, send_from_directory

# 같은 db 폴더 내부의 utils에서  만능 함수들 가져오기 (save_logs, get_logs)
from db.utils.json_capture_manager import save_logs, get_logs

# 'rescue'라는 이름의 블루프린트 생성
rescue_bp = Blueprint('rescue', __name__)

# C 드라이브 이미지 폴더 절대 경로 고정
OCEAN_RESCUE_DIR = r"C:\ocean_rescue_images"


# 1. 드론 카메라가 조난자 포착 후 사진을 보낼 때 (POST /api/drone/capture)
@rescue_bp.route('/api/drone/capture', methods=['POST'])
def drone_capture():
    image_file = request.files.get('image')
    
    # 조장님의 만능 함수 호출
    result = save_logs(image_file)
    
    if not result["success"]:
        return jsonify(result), 500
    return jsonify(result), 200


# 2. 웹 대시보드가 표에 뿌릴 전체 데이터를 요청할 때 (GET /api/dashboard/logs)
@rescue_bp.route('/api/dashboard/logs', methods=['GET'])
def get_dashboard_logs():
    logs_data = get_logs()
    
    # 최신 사건이 위로 오도록 역순 뒤집어서 반환
    return jsonify(logs_data[::-1]), 200


# 3. 대시보드 화면에 실제 사진을 띄워줘야 할 때 (GET /external_img/사진명)
@rescue_bp.route('/external_img/<filename>', methods=['GET'])
def serve_rescue_image(filename):
    return send_from_directory(OCEAN_RESCUE_DIR, filename)
