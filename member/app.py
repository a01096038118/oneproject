from flask import Flask
from member.route import member_bp

app = Flask(__name__)

app.secret_key = "dw-aiot5th-20260622"

app.register_blueprint(member_bp)


if __name__ == '__main__':
    app.run()