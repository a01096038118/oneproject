from flask import Flask, render_template, session
from blueprints.troubleshooting.routes import trouble_bp

app = Flask(__name__)
app.secret_key = 'interplanetaryNetworkKey'

app.register_blueprint(trouble_bp)

IS_DEV_MODE = True 

@app.before_request
def devmode_login():

    if IS_DEV_MODE:
        session['signed_member_Id'] = 'devmode'  

@app.route('/')
def home():
    return render_template('trouble_forms/index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

                                                                                                                                                                                                                                                                                                
# app.before_request는 이미 플라스크 제작자들이 app이라는 객체 안에 만들어둔 '기능(메서드)'
# @ 기호는 '이름표(또는 포스트잇)' 같은 역할을 합니다. 전문 용어로는 데코레이터(Decorator)