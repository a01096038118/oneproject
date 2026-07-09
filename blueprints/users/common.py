from flask import Blueprint, redirect, session, flash


common_bp = Blueprint(
    'common',
    __name__,
    url_prefix='/common'
)

# 로그아웃
@common_bp.route('/signOut_form', methods = ['GET'])
def signOut_form():
    
    session.pop('signedInMemberId', None)
    session.pop('signedInAdminId', None)

    session.pop('role', None)
    
    flash('로그아웃되었습니다.')

    return redirect('/')




    
