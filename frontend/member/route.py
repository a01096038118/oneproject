from flask import Blueprint, render_template, request, redirect, session, flash
import uuid
from db.utils.json_admin_manager import load_admins, save_admins
from db.utils.json_key_manager import load_admin_keys, save_admin_keys
from db.utils.json_member_manager import save_members, load_members
import re



admin_bp = Blueprint(
    'admin',
    __name__,
    url_prefix='/admin'
)

member_bp = Blueprint(
    'member',
    __name__,
    url_prefix='/member'
)

# 글자4개 이상
id_pattern = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z0-9]{4,20}$'
# 글자&숫자 포함 8자 이상 20자 이하
pw_pattern = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[\W_])[^\s]{8,20}$'
# '@'과'.' 존재 
mail_pattern = r'^[\w.-]+@[\w.-]+\.[A-Za-z]{2,5}$'
# 숫자 8자
phone_pattern =r'^\d{10,11}$'
# 경력 증명
career_pattern = r'^\d+개월$'



# 관리자 회원가입 화면 이동
@admin_bp.route('/adminSignUp_form', methods = ['GET'])
def adminSignUp_form():
    print('adminSignUp_confirm() CALLED')

    return render_template('member/adminSignUp_form.html')


# 관리자 회원가입 양식
@admin_bp.route('/adminSignUp_confirm', methods = ['POST'])
def adminSignUp_confirm():
    print('adminSignUp_confirm() CALLED')

    admins = load_admins()
     
    # id_pattern = r'^(?=.*[A-Za-z])[A-Za-z0-9]{4,20}$'
    mId = request.form['mId']
    if not re.match(id_pattern, mId):
        return render_template('member/adminSignUp_result.html',
                               result = '아이디는 영문, 숫자 포함 4자 이상 20자 이하로 입력해주세요.')
   
    # pw_pattern = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[\W_])[^\s]{8,20}$'
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
    
     # id 중복
    if mId in admins:
        return render_template('member/adminSignUp_form.html',
                               result = '중복된 ID 입니다. 다시 입력해주세요.')
    # email 중복
    for admin in admins.values():
        if admin ['mMail'] == mMail:
            return render_template('member/adminSignUp_form.html',
                                    result = '중복된 EMAIL입니다.')
        
    admin_keys = load_admin_keys()
    new_uuid = str(uuid.uuid4())

    admin_keys[new_uuid] = {
        'used': False
    }

    save_admin_keys(admin_keys)

    admins [mId] = {
        'mId': mId,
        'mPw': mPw,
        'mMail': mMail,
        'mPhone': mPhone,
        'role': 'ADMIN',
        'admin_key': new_uuid
    }

    save_admins(admins)
    save_admin_keys(admin_keys)


    return render_template(
        'member/adminSignUp_result.html',
        result = 'OK',
        admin_key = new_uuid)

    
# 직원 회원가입 화면 이동
@member_bp.route('/memberSignUp_form', methods = ['GET'])
def memberSignUp_form():
    return render_template('member/memberSignUp_form.html')
    
#  직원 회원가입 양식
@member_bp.route('/memberSignUp_confirm', methods = ['POST'])
def memberSingup_comfirm():
    print('memberSignUp_confirm() CALLED!!')

    admins = load_admins()
    members = load_members()


    # id_pattern = r'^(?=.*[A-Za-z])[A-Za-z0-9]{4,20}$'
    mId = request.form['mId']
    if not re.match(id_pattern, mId):
        return render_template('member/memberSignUp_form.html',
                               result = '아이디는 영문, 숫자 포함 4자 이상 20자 이하로 입력해주세요.')

    if mId in members:
        return render_template('member/memberSignUp_form.html',
                               result = '중복된 ID입니다. 다시입력해주세요.')

    # pw_pattern = r'^(?=.*[A-Za-z])(?=.*\d)[^\s]{8,20}$'
    mPw = request.form['mPw']
    if not re.match(pw_pattern, mPw):
        return render_template('member/memberSignUp_form.html',
                               result = '비밀번호 특수문자, 영문, 숫자 포함하여 8자리 이상 20자리 이하로 입력해주세요.')
    
    # mail_pattern = r'^[\w.-]+@[\w.-]+\.[A-Za-z]{2,5}$'
    mMail = request.form['mMail']
    if not re.match(mail_pattern, mMail):
        return render_template('member/memberSignUp_form.html',
                               result = '올바른 이메일 형식이 아닙니다.')
    
    for member in members.values():
        if member['mMail'] == mMail:
            return render_template('member/memberSignUp_form.html',
                                   result = '중복된 EMAIL입니다.')

    # phone_pattern =r'^\d{10,11}$'
    mPhone = request.form['mPhone']
    if not re.match(phone_pattern, mPhone):
        return render_template('member/memberSignUp_form.html',
                               result = '숫자만 입력해주세요.')
    
    mCareer = request.form['mCareer']
    if not re.match(career_pattern, mCareer):
        return render_template('member/memberSignUp_form.html',
                               result = '형식에 맞게 작성해주세요.')

    members = load_members()

    members [mId] = {
        'mId': mId,
        'mPw': mPw,
        'mMail': mMail,
        'mPhone': mPhone,
        'mCareer': mCareer,
        'role': 'MEMBER'
    }

    save_members(members)

    return render_template(
        'member/memberSignIn_form.html', 
        result = 'OK')

# 관리자 로그인 화면 
@admin_bp.route('/adminSignIn_form', methods = ['GET'])
def adminSignIn_form():
    return render_template('member/adminSignIn_form.html')

# 관리자 로그인 양식
@admin_bp.route('/adminSignIn_confirm', methods = ['POST'])
def adminSignIn_confirm():

    admins = load_admins()

    mId = request.form['mId']
    mPw = request.form['mPw']
    admin_key = request.form['admin_key']

    admin_keys = load_admin_keys()
    

    # #  이미 사용된 키 확인
    # if admin_keys[admin_key].get('used'):
    #     return render_template(
    #         'member/adminSignUp_result.html', 
    #         result='NG')
    
    if mId not in admins:
        return render_template('member/adminSignIn_form.html',
                                   result = 'ID가 존재하지 않습니다.')
    if admins [mId]['mPw'] != mPw:
        return render_template('member/adminSignIn_form.html',
                               result = '올바른 비밀번호가 아닙니다.') 
    #  키 존재 확인
    if admin_key not in admin_keys:
        return render_template('member/adminSignUp_result.html',
                               result = '올바른 키번호가 아닙니다.')  
    
    save_admin_keys(admin_keys)

    session['signedInAdminId'] = mId
    session['role'] = admins[mId]['role']
        
    return render_template('/index.html', result = 'SIGNIN SUCCESS!!')

    
# member 로그인 화면
@member_bp.route('/memberSignIn_form', methods = ['GET'])
def memberSignIn_form():
    return render_template('member/memberSignIn_form.html')

# member 로그인 양식
@member_bp.route('/memberSignIn_confirm', methods = ['POST'])
def memberSignIn_confirm():

    members = load_members()

    mId = request.form['mId']
    mPw = request.form['mPw']
    

    # 회원이 여러명이 경우 [mId] = X
    if mId not in members:
        return render_template('member/memberSignIn_form.html', 
                               result = 'ID가 존재하지않습니다.')
    if members [mId]['mPw'] !=mPw:
        return render_template('member/memberSignIn_form.html', 
                                result = '올바른 비밀번호가 아닙니다.')
    
    session['signedInMemberId'] = mId
    session['role'] = members[mId]['role']
                   
    return render_template('/index.html', result = 'SIGNIN SUCCESS!!')



# 1. MEMBERS 클릭 시 로그인/회원가입 선택 페이지 리턴
@member_bp.route('/gateway', methods=['GET'])
def member_gateway():
    return render_template('member/member_gateway.html')


# 2. ADMIN 클릭 시 관리자 로그인/회원가입 선택 페이지 리턴
@admin_bp.route('/gateway', methods=['GET'])
def admin_gateway():
    # 파일이 templates/member 안에 들어있으므로 경로를 member/ 로 지정해야 오류가 나지 않습니다!
    return render_template('member/admin_gateway.html')


# 로그아웃
@member_bp.route('/signOut_form', methods = ['GET'])
def signOut_form():
    
    session.pop('signedInMemberId', None)
    session.pop('signedInAdminId', None)

    session.pop('role', None)
    
    flash('로그아웃되었습니다.')

    return redirect('/')


# 회원정보 리스트
@member_bp.route('/member_list', methods=['GET'])
def member_list():

    members = load_members()

    return render_template(
        'member/member_list.html',
        members=members
    )

# 회원정보 수정 화면 
@member_bp.route('/modify_form/<mId>', methods = ['GET'])
def modify_form(mId):

    members = load_members()

    if mId not in members:
        return('존재하지 않은 회원입니다.')
    
    member = members[mId]
    
    return render_template('member/modify_form.html',
                           member = member)

#  회원정보 수정 양식
@member_bp.route('/modify_confirm', methods = ['POST'])
def modify_confirm():

    admin_key = request.form['admin_key']
    admin_keys = load_admin_keys()
    
    if admin_key not in admin_keys:
        return render_template('member/adminSignUp_result.html',
                               result = '올바른 키번호가 아닙니다.') 
    
    members = load_members()

    mId = request.form['mId']
    mPw = request.form['mPw']
    mMail = request.form['mMail']
    mPhone = request.form['mPhone']
        
    if mId in members:

        # [mId]가 없으면 덮어쓰기가 아니라 mPw, mMail, mPhone이 새로 추가됨
        members[mId]['mPw'] = mPw
        members[mId]['mMail'] = mMail
        members[mId]['mPhone'] = mPhone

        save_members(members)

        return render_template('member/modify_result.html',
                                result = 'MODIFY SUCCESS!!')


# member 삭제
@member_bp.route('/delete_form/<mId>')
def delete_form(mId):
    return render_template('member/delete_form.html', mId = mId)
    
@member_bp.route('/delete_confirm', methods = ['POST'])
def delete_confirm():

    mId = request.form['mId']
    admin_key = request.form['admin_key']

    admin_keys = load_admin_keys()

    #  키 존재 확인
    if admin_key not in admin_keys:
        return render_template('member/delete_form.html',
                               mId = mId,
                               result = '올바른 키번호가 아닙니다.') 
    
    members = load_members()
    
    if mId in members:
        del members[mId]

        save_members(members)
        
    return redirect('/member/member_list')

    
