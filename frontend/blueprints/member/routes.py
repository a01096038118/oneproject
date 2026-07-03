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

    # 1. ID 중복 체크 (기존 리스트 구조일 때의 안전한 체크)
    if isinstance(admins, list):
        for admin_item in admins:
            if admin_item.get('mId') == mId:
                return render_template('member/adminSignUp_result.html',
                                       result = '중복된 ID 입니다. 다시 입력해주세요.')
    elif isinstance(admins, dict):
        if mId in admins:
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

    # phone_pattern =r'^\d{10,11}$'
    mPhone = request.form['mPhone']
    if not re.match(phone_pattern, mPhone):
        return render_template('member/adminSignUp_result.html',
                               result = '숫자만 입력해주세요.')
    
    # 🌟 [자동 생성] 고유한 UUID 관리자 키 생성
    generated_admin_key = str(uuid.uuid4())

    # 변수 이름이 겹치지 않게 새로 불러와 할당
    current_admins = load_admins()

    # 데이터 저장 (기존 데이터가 딕셔너리 구조 {mId: {}} 인 경우)
    if isinstance(current_admins, dict):
        current_admins[mId] = {
            'mId': mId,
            'mPw': mPw,
            'mMail': mMail,
            'mPhone': mPhone,
            'role': 'ADMIN',
            'admin_key': generated_admin_key
        }
        save_admins(current_admins)

    # 🌟 회원가입 성공 시 생성된 UUID 키(generated_key)를 결과 페이지로 확실히 전달
    return render_template(
        'member/adminSignUp_result.html',
        result = 'OK',
        generated_key = generated_admin_key)

    
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
        member = members[member]
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
        member = members[member]
        if member ['mMail'] == mMail:
            return render_template('member/adminSignUp_result.html',
                                   result = '중복된 EMAIL입니다.')

    # phone_pattern =r'^\d{10,11}$'
    mPhone = request.form['mPhone']
    if not re.match(phone_pattern, mPhone):
        return render_template('member/adminSignUp_result.html',
                               result = '숫자만 입력해주세요.')

    members = load_members()

    members [mId] = {
        'mId': mId,
        'mPw': mPw,
        'mMail': mMail,
        'mPhone': mPhone,
        'role': 'MEMBER'
    }

    save_members(members)

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

    return render_template('member/memberModify_form.html', members = members)

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
    
@member_bp.route('/gateway', methods=['GET'])
def member_gateway():
    return render_template('member/member_gateway.html')

@admin_bp.route('/gateway', methods=['GET'])
def admin_gateway():
    return render_template('member/admin_gateway.html')