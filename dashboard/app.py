from flask import (Flask, 
                   render_template,
)
from blueprints.dashboard.routes import dashboard_bp


app = Flask(__name__)

app.register_blueprint(dashboard_bp)

@app.route('/')
def home():
    return "Dashboard"

if __name__ == "__main__":
    app.run(
        debug=True
    )