from flask import Blueprint, render_template, request, session
from db.utils.json_member_manager import save_members, load_members
import re

member_bp = Blueprint(
    'member',
    __name__,
    url_prefix='/member'
)

# 글자4개 이상
id_pattern = r'^(?=.*[A-Za-z])[A-Za-z0-9]{4,20}$'
# 글자&숫자 포함 8자 이상 20자 이하
pw_pattern = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[\W_])[^\s]{8,20}$'
# '@'과'.' 존재 
mail_pattern = r'^[\w.-]+@[\w.-]+\.[A-Za-z]{2,5}$'
# 숫자 8자
phone_pattern =r'^\d{10,11}$'
# 경력 증명
career_pattern = r'^\d+개월$'

    
# 직원 회원가입 화면 이동
@member_bp.route('/memberSignUp_form', methods = ['GET'])
def memberSignUp_form():
    return render_template('member/memberSignUp_form.html')
    


#  직원 회원가입 양식
@member_bp.route('/memberSignUp_confirm', methods = ['POST'])
def memberSignup_confirm():
    print('memberSignUp_confirm() CALLED!!')

    members = load_members()


    # id_pattern = r'^(?=.*[A-Za-z])[A-Za-z0-9]{4,20}$'
    mId = request.form['mId']
    if not re.match(id_pattern, mId):
        return render_template('member/memberSignUp_form.html',
                               result = '아이디는 4자 이상 20자 이하로 입력해주세요.')

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
        result = 'MEMBER SIGNUP SUCCESS!!')


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
                   
    return render_template('/index.html', result = 'MEMBER SIGNIN SUCCESS!!')



@member_bp.route('/gateway', methods=['GET'])
def member_gateway():
    return render_template('member/member_gateway.html')



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