# 메인 백엔드 담당
from flask import Flask
from db.blueprint.rescue_router import rescue_bp


app = Flask(__name__)

app.register_blueprint(rescue_bp)
