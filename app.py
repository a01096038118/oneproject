from flask import Flask, render_template
from users.route import member_bp, admin_bp, common_bp
from dashboard.blueprints.dashboard.routes import dashboard_bp



app = Flask(__name__)
app.secret_key = "dw-aiot5th-20260622"

app.register_blueprint(member_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(common_bp)

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