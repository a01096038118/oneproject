from flask import Blueprint, render_template, request, redirect, session
import uuid

from db.utils.json_admin_manager import load_admins, save_admins
from db.utils.json_key_manager import load_admins_key, save_admins_key
from db.utils.json_member_manager import save_members, load_members
import re

'''modified'''

member_bp = Blueprint(
    'member',
    __name__,
    url_prefix='/member'
)

admin_bp = Blueprint(
    'admin',
    __name__,
    url_prefix='/admin'
)

# 글자4개 이상
id_pattern = r'^(?=.*[A-Za-z])[A-Za-z0-9]{4,20}$'
# 글자&숫자 포함 8자 이상 20자 이하
pw_pattern = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*^[A-Za-z0-9])[^\s]{8,20}$'
# '@'과'.' 존재 
mail_pattern = r'^[\w.-]+@[\w.-]+\.[A-Za-z]{2,5}$'
# 숫자 8자
phone_pattern =r'^\d{10,11}$'
# 경력 증명
career_pattern = r'^\d+개월$'


#  관리자 키 생성 페이지
@admin_bp.route('/admin_key_page', methods = ['GET'])
def admin_key_page():
    print(session['signIntedMember'])
    if session['signIntedMember']['role'] != 'ADMIN':
        return '접근 불가! 관리자 전용입니다.'
    
    return render_template('member/admin_key_page.html')

# 키 생성
@admin_bp.route('/generate_key', methods = ['POST'])
def generate_key():
    if session['signIntedMember']['role'] != 'ADMIN':
        return '접근 불가! 관리자 전용입니다.'
    
    admin_key = load_admins_key()
    new_uuid = str(uuid.uuid4())

    admin_key[new_uuid] = {
        'used': False
    }

    save_admins_key(admin_key)
    return render_template(
        'member/admin_key_result.html',
        new_key=new_uuid
    )

# 관리자 회원가입 화면 이동
@admin_bp.route('/adminSignUp_form', methods = ['GET'])
def adminSignUp_form():
    print('adminSignUp_confirm() CALLED')

    return render_template('member/adminSignUp_form.html')


# 관리자 회원가입 양식
@admin_bp.route('/adminSignUp_confirm', methods = ['POST'])
def adminSignUp_confirm():
    print('adminSignUp_confirm() CALLED')

    # id_pattern = r'^(?=.*[A-Za-z])[A-Za-z0-9]{4,20}$'
    mId = request.form['mId']
    if not re.match(id_pattern, mId):
        return render_template('member/adminSignUp_result.html',
                               result = '아이디는 영문, 숫자 포함 4자 이상 20자 이하로 입력해주세요.')
    admins = load_admins()

    for admin in admins:
        if admin ['mId'] == mId:
            return render_template('member/adminSignUp_result.html',
                                   result = '중복된 ID 입니다. 다시 입력해주세요.')
    
    # pw_pattern = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*^[A-Za-z0-9])[^\s]{8,20}$'
    mPw = request.form['mPw']
    if not re.match(pw_pattern, mPw):
        return render_template('member/adminSignUp_result.html',
                               result = '비밀번호 특수문자, 영문, 숫자 포함해서 8자리 이상 입력해주세요.')
     
    # mail_pattern = r'^[\w.-]+@[\w.-]+\.[A-Za-z]{2,5}$'
    mMail = request.form['mMail']
    if not re.match(mail_pattern, mMail):
        return render_template('member/adminSignUp_result.html',
                               result = '올바른 이메일 형식이 아닙니다.')
    admin = load_admins()
    for admin in admins:
        if admin ['mId'] == mId:
            return render_template('member/adminSignUp_result.html',
                                   result = '중복된 EMAIL입니다.')

    # phone_pattern =r'^\d{10,11}$'
    mPhone = request.form['mPhone']
    if not re.match(phone_pattern, mPhone):
        return render_template('member/adminSignUp_result.html',
                               result = '숫자만 입력해주세요.')
    
    inputKey = request.form['admin_key']

    admin_key = load_admins_key()
    print('admin_key:', admin_key)
    admins = load_admins()

    #  키 존재 확인
    if inputKey not in admin_key:
        return render_template(
            'member/adminSignUp_result.html',
            result = 'NG. 올바른 키번호가 아닙니다.')

    #  이미 사용된 키 확인
    if admin_key[inputKey].get('used'):
        return render_template(
            'member/adminSignUp_result.html', 
            result='NG . 이미 사용된 키입니다.')

    if mId in admin:
        return render_template(
            'member/adminSignUp_result.html',
            result = 'NG. 이미 존재하는 ID입니다.')
    
    admin [mId] = {
        'mId': mId,
        'mPw': mPw,
        'mMail': mMail,
        'mPhone': mPhone,
        'role': 'ADMIN',
        'admin_key': inputKey
    }

    admin_key[inputKey]['used'] = True

    save_admins(admin)
    save_admins_key(admin_key)


    return render_template(
        'member/adminSignUp_result.html',
        result = 'OK')

    
# 직원 회원가입 화면 이동
@member_bp.route('/memberSignUp_form', methods = ['GET'])
def memberSignUp_form():
    return render_template('member/memberSignUp_form.html')
    
#  직원 회원가입 양식
@member_bp.route('/memberSignUp_confirm', methods = ['POST'])
def memberSingup_comfirm():
    print('memberSignUp_confirm() CALLED!!')

    # id_pattern = r'^(?=.*[A-Za-z])[A-Za-z0-9]{4,20}$'
    mId = request.form['mId']
    if not re.match(id_pattern, mId):
        return render_template('member/adminSignUp_result.html',
                               result = '아이디는 영문, 숫자 포함 4자 이상 20자 이하로 입력해주세요.')
    members = load_members()

    for member in members:
        if member ['mId'] == mId:
            return render_template('member/adminSignUp_result.html',
                                   result = '중복된 ID입니다. 다시입력해주세요.')

    # pw_pattern = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*^[A-Za-z0-9])[^\s]{8,20}$'
    mPw = request.form['mPw']
    if not re.match(pw_pattern, mPw):
        return render_template('member/adminSignUp_result.html',
                               result = '비밀번호 특수문자, 영문, 숫자 포함하여 8자리 이상 입력해주세요.')
    
    # mail_pattern = r'^[\w.-]+@[\w.-]+\.[A-Za-z]{2,5}$'
    mMail = request.form['mMail']
    if not re.match(mail_pattern, mMail):
        return render_template('member/adminSignUp_result.html',
                               result = '올바른 이메일 형식이 아닙니다.')
    
    members = load_members()
    
    for member in members:
        if member ['mMail'] == mMail:
            return render_template('member/adminSignUp_result.html',
                                   result = '중복된 EMAIL입니다.')

    # phone_pattern =r'^\d{10,11}$'
    mPhone = request.form['mPhone']
    if not re.match(phone_pattern, mPhone):
        return render_template('member/adminSignUp_result.html',
                               result = '숫자만 입력해주세요.')
    
    mCareer = request.form['mCareer']
    if re.match(career_pattern, mCareer):
        return render_template('member/adminSignUp_result.html',
                               result = 'OK')

    members = load_members()

    member [mId] = {
        'mId': mId,
        'mPw': mPw,
        'mMail': mMail,
        'mPhone': mPhone,
        'mCareer': mCareer,
        'role': 'MEMBER'
    }

    save_members(member)

    return render_template(
        'member/memberSignUp_result.html', 
        result = '회원가입 성공')

# 관리자 로그인 화면 
@admin_bp.route('/adminSignIn_form', methods = ['GET'])
def adminSignIn_form():
    return render_template('member/adminSignIn_form.html')

# 관리자 로그인 양식
@admin_bp.route('/adminSignIn_confirm', methods = ['POST'])
def adminSignIn_confirm():

    admins = load_admins()
    keys = load_admins_key()
    print(admins)

    mId = request.form['mId']
    mPw = request.form['mPw']
    inputKey = request.form['admin_key']
    for admin in admins:
        admin = admins[admin]
        if admin['mId'] == mId:
            if admin['mPw'] != mPw:
                return render_template('member/adminSignIn_result.html',
                                       result = '올바른 비밀번호가 아닙니다.')   
                 
            if inputKey != admin['admin_key']:
                return render_template('member/adminSignIn_result.html',
                                    result = '올바른 키번호가 아닙니다.')
            
            session['signIntedMember'] = admin
            return render_template('member/adminSignIn_result.html',
                                   result = 'SIGNUP SUCCESS!!')
        
    return render_template('member/adminSignIn_result.html',
                            result = 'ID가 존재하지 않습니다.')

    
# member 로그인 화면
@member_bp.route('/memberSignIn_form', methods = ['GET'])
def memberSignIn_form():
    return render_template('/member/memberSignIn_form.html')

# member 로그인 양식
@member_bp.route('/memberSignIn_confirm', methods = ['POST'])
def memberSignIn_confirm():

    members = load_members()

    mId = request.form['mId']
    mPw = request.form['mPw']

    # 회원이 여러명이 경우 [mId] = X
    for member in members:
        member = members[member]
        
        if member['mId'] == mId:
            if member['mPw'] != mPw:
                return render_template('member/memberSignIn_result.html', 
                                       result = '올바른 비밀번호가 아닙니다.')
            
            session['signIntedMember'] = member['mId']
            return render_template('member/memberSignIn_result.html', 
                                   result = 'OK')
        
    return render_template('member/memberSignIn_result.html',
                           result = 'ID가 존재하지않습니다.')

# 로그아웃
@member_bp.route('/signOut_confirm', methods = ['GET'])
def signOut_confirm():
    
    session.clear()

    return redirect('/')

# 회원정보 수정 화면
@member_bp.route('/memberModify_form', methods = ['GET'])
def memberModify_form():

    members = load_members()
    signedId = session.get('signIntedMember')
    member = members[signedId]

    return render_template('member/memberModify_form.html', member = member)

#  회원정보 수정 양식
@member_bp.route('/memberModify_confirm', methods = ['POST'])
def memberModify_confirm():

    admins = load_admins_key()
    inputKey = request.form['admin_key']
    master_admin = False

    for admin in admins:
        if admin['admin_key'] == inputKey:
                master_admin = True
                break
        
    if not master_admin:
        return render_template('memberModify_result.html',
                                result = '올바른 키번호가 아닙니다.')
    
    members = load_members()

    mId = request.form['mId']
    mPw = request.form['mPw']
    mMail = request.form['mMail']
    mPhone = request.form['mPhone']
        
    for member in members:
        if member['mId'] == mId:

            member['mPw'] = mPw
            member['mMail'] = mMail
            member['mPhone'] = mPhone

            save_members(members)
            return render_template('memberModify_result.html',
                                   result = 'MODIFY SUCCESS!!')


@member_bp.route('/memberDelete_confirm', methods = ['GET'])
def memberDelete_confirm():

    members = load_members()

    signIntedmember = session.get('signIntedmember')
    del members[signIntedmember]

    save_members(members)

    session.clear

    return render_template('memberDelete_result.html',
                           result = 'OK')
    
