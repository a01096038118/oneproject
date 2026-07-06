from flask import (Blueprint,
                   Response,
                   jsonify,
                   send_from_directory,
                   request,
                   render_template,
                   session)
from dashboard.ai.camera_manager import generate_frame
from dashboard.utils.log_manager import (
    get_logs,
    delete_log,
    check_log
)

from dashboard import config

dashboard_bp = Blueprint(
    'dashboard',
    __name__,
    url_prefix="/dashboard"
)

@dashboard_bp.route('/main')
def main():
    return render_template('dashboard/dashboard.html')

# OpenCV 실시간 영상을 웹으로 스트리밍
@dashboard_bp.route('/video_feed')
def video_feed():
    return Response(
        generate_frame(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

# 로그 조회
@dashboard_bp.route('/logs', methods=['GET'])
def get_dashboard_logs():

    logs = get_logs()

    return jsonify(logs[::-1]), 200

# 로그 삭제
@dashboard_bp.route('/delete_log/<log_id>', methods=['DELETE'])
def delete_dashboard_log(log_id):

    result = delete_log(log_id)

    if not result["success"]:
        return jsonify(result), 404

    return jsonify(result), 200

# 캡처 이미지 제공
@dashboard_bp.route('/external_img/<filename>', methods=['GET'])
def serve_rescue_image(filename):

    return send_from_directory(
        config.OCEAN_RESCUE_DIR,
        filename
    )

# 로그 확인 처리
@dashboard_bp.route('/check_log/<log_id>', methods=['POST'])
def check_dashboard_log(log_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "요청 데이터가 없습니다."
        }), 400

    manager = session.get("signedInMemberId") or session.get("signedInAdminId") or "임시_관리자"

    if not manager:
        return jsonify({
            "success": False,
            "message": "담당자 정보가 없습니다."
        }), 400

    data = request.get_json(silent=True) or {}
    
    result = check_log(log_id, manager)

    if not result["success"]:
        return jsonify(result), 404

    # return jsonify(result), 200
    actual_log_data = result.get("checked_log", {})

   
    return jsonify({
        "success": True,
        "log_id": actual_log_data.get("log_id"),
        "manager": actual_log_data.get("manager"),
        "checked_time": actual_log_data.get("checked_time"),
        "detected_time": actual_log_data.get("detected_time"),
        "person_count": actual_log_data.get("person_count"),
        "captured_image_path": actual_log_data.get("captured_image_path"),
        "status": actual_log_data.get("message")  # "위험구역 침범 감지" 문자열
    }), 200