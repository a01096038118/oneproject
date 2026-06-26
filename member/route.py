from flask import Blueprint, render_template, request, redirect, session
import uuid
import load_admins, save_admins, load_admins_key, save_admins_key, save_members, load_members


member_bp = Blueprint(
    'member',
    __name__,
    url_prefix='/member'
)

#  관리자 키 생성 페이지
@member_bp.route('/admin_key_page', methods = ['GET'])
def admin_key_page():
    if session.get('role') != 'ADMIN':
        return '접근 불가! 관리자 전용입니다.'
    
    return render_template('frontend/admin_key_page.html')

# 키 생성
@member_bp.route('/generate_key', methods = ['POST'])
def generate_key():
    if session.get('role') != 'ADMIN':
        return '접근 불가! 관리자 전용입니다.'
    
    admin_key = load_admins_key()
    new_uuid = str(uuid.uuid4())

    admin_key[new_uuid] = {
        'used': False
    }

    save_admins_key(admin_key)
    return render_template(
        'frontend/admin_key_result.html',
        new_key=new_uuid
    )

# 관리자 회원가입 화면 이동
@member_bp.route('/adminSignUp_form', methods = ['GET'])
def adminSignUp_form():
    print('adminSignUp_confirm() CALLED')

    return render_template('frontend/adminSignUp_form.html')


# 관리자 회원가입 양식
@member_bp.route('/adminSignUp_confirm', methods = ['POST'])
def adminSignUp_confirm():
    print('adminSignUp_confirm() CALLED')

    mId = request.form['mId']
    mPw = request.form['mPw']
    mMail = request.form['mMail']
    mPhone = request.form['mPhone']
    inputUuid = request.form['admin_uuid']

    admin_key = load_admins_key()
    admin = load_admins()

    #  키 존재 확인
    if inputUuid not in admin_key:
        return render_template(
            'frontend/adminSignUp_result.html',
            result = 'NG')

    #  이미 사용된 키 확인
    if admin_key[inputUuid].get('used'):
        return render_template(
            'frontend/adminSignUp_result.html', 
            result='NG')

    if mId in admin:
        return render_template(
            'frontend/adminSignUp_result.html',
            result = 'NG')
    
    admin [mId] = {
        'mId': mId,
        'mPw': mPw,
        'mMail': mMail,
        'mPhone': mPhone,
        'role': 'ADMIN'
    }

    admin_key[inputUuid]['used'] = True

    save_admins(admin)
    save_admins_key(admin_key)


    return render_template(
        'frontend/adminSignUp_result.html',
        result = 'OK')

    
# 직원 회원가입 화면 이동
@member_bp.route('/memberSignUp_form', methods = ['GET'])
def memberSignUp_form():
    return render_template('frontend/memberSignUp_form.html')
    
#  직원 회원가입 양식
@member_bp.route('/memberSignUp_confirm', methods = ['POST'])
def memberSingup_comfirm():
    print('memberSignUp_confirm() CALLED!!')

    mId = request.form['mId']
    mPw = request.form['mPw']
    mMail = request.form['mMail']
    mPhone = request.form['mPhone']

    member = load_members()

    member [mId] = {
        'mId': mId,
        'mPw': mPw,
        'mMail': mMail,
        'mPhone': mPhone
    }

    save_members(member)

    return render_template(
        'frontend/memberSignUp_result.html', 
        result = 'OK')

# 로그인 화면 
@member_bp.route('/memberSignIn_form', methods = ['GET'])
def memberSignIn_form():
    return render_template('memberSignIn_form/html')

# 로그인 양식
@member_bp.route('/memberSignIn_confirm', methods = ['POST'])
def memberSignIn_confirm():
    
    

    

@member_bp.route('/memberModify_form', methods = ['GET'])
def memberModify_form():
    pass

@member_bp.route('/memberModify_confirm', methods = ['POST'])
def memberModify_confirm():
    pass

@member_bp.route('/memberDelete_confirm', methods = ['GET'])
def memberDelete_confirm():
    pass
# @member_bp.route('/adminDelete_confirm', methods = ['GET'])
# def adminDelete_confirm():
#     pass
