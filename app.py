from flask import Flask, render_template
from blueprints.users.member import member_bp
from blueprints.users.admin import admin_bp
from blueprints.users.common import common_bp
from blueprints.dashboard.routes import dashboard_bp
from blueprints.trouble.trouble_routes import trouble_bp



app = Flask(__name__)
app.secret_key = "dw-aiot5th-20260622"

app.register_blueprint(member_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(common_bp)
app.register_blueprint(trouble_bp)

@app.route("/")
def home():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(
        host='0.0.0.0', 
        port=5000, 
        debug=False,
        threaded=True
    )