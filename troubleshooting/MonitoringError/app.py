from flask import Flask, render_template, session
from blueprints.troubleshooting.routes import trouble_bp

app = Flask(__name__)
app.secret_key = 'interplanetaryNetworkKey'

app.register_blueprint(trouble_bp)

IS_DEV_MODE = True 

@app.before_request
def devmode_login():

    if IS_DEV_MODE:
        session['signed_member_Id'] = 'LeeYoon'  

@app.route('/')
def home():
    return render_template('trouble_forms/index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

