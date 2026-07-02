from flask import (Blueprint,
                   Response)
from ai.camera_manager import generate_frame

dashboard_bp = Blueprint(
    'dashboard',
    __name__,
    url_prefix="/dashboard"
)

@dashboard_bp.route('/video_feed')
def video_feed():
    return Response(
        generate_frame(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )