from flask import Blueprint, render_template, request, redirect, session, url_for
from utils.trouble_json_manager import load_errors, save_errors
from utils import time
import uuid

trouble_bp = Blueprint(
    'trouble',
    __name__,
    url_prefix='/trouble'
)

#new_critical_error_form                     
@trouble_bp.route('/new_critical_error_form', methods=['GET'])
def new_critical_error_form():

    mId = session.get('signed_member_Id')
    if not mId:
        return redirect(url_for('member.signin_form'))

    return render_template('trouble_forms/new_critical_error_form.html')

#new_critical_error_confirm
@trouble_bp.route('/new_critical_error_confirm', methods=['POST'])
def new_critical_error_confirm():

    mId = session.get('signed_member_Id')

    if not mId:
        return redirect(url_for('/member.signin_form'))
    
    eNum = str(uuid.uuid4())
    
    regdatetime = time.getCurrentDateTime()
    
    eNum = request.form['eNum']
    category = request.form['category']
    error_code = request.form['error_code']
    issue = request.form['issue']
    progress = request.form['progress']

    critical_errors = load_errors()

    if mId not in critical_errors:
        critical_errors[mId] = {}

    staff_errors = critical_errors[mId]
     
    staff_errors[eNum] = {
        'category': category,
        'error_code' : error_code,
        'issue' : issue,
        'progress': progress,
        'resolution' :"",
        'date': regdatetime    
    }
    
    save_errors(critical_errors)

    return render_template('trouble_forms/new_critical_error_result.html')

# /error_modify_form
@trouble_bp.route('/error_modify_form', methods=['GET'])
def error_modify_form():
    mId = session.get('signed_member_Id')
    if not mId:
        return redirect(url_for('member.signin_form'))
    
    critical_errors = load_errors()
    
    if mId not in critical_errors or not critical_errors[mId]:
   
        return redirect(url_for('new_critical_error_form'))

    return render_template('trouble_forms/error_modify_form.html')

#/error_modify_confirm
@trouble_bp.route('/error_modify_confirm', methods=['POST'])
def error_modify_confirm():
     
    mId  = session['signed_member_Id']
    
    if not mId:
        return redirect(url_for('member.signin_form'))
    
    critical_errors = load_errors()
    
    if mId not in critical_errors or not critical_errors[mId]:
   
        return redirect(url_for('new_critical_error_form'))

    regdatetime = time.getCurrentDateTime()
    
    resolution = request.form['resolution']
    progress = request.form['progress']
    
    staff_errors = critical_errors.get(mId, {})

    staff_errors[eNum]['resolution'] = resolution
    staff_errors[eNum]['progress'] = progress
    staff_errors[eNum]['regdatetime'] = regdatetime
   

    save_errors(critical_errors)
    
    return render_template('trouble_forms/error_modify_result.html')

@trouble_bp.route('/error_delete_form', methods=['GET'])
def error_delete_form():

    mId = session.get('signed_member_Id')
    if not mId:
        return redirect(url_for('member.signin_form'))
    
    critical_errors = load_errors()
    
    if mId not in critical_errors or not critical_errors[mId]:
   
        return redirect(url_for('new_critical_error_form'))

    return render_template('trouble_forms/error_delete_form.html')

# /error/delete_confirm
@trouble_bp.route('/error_delete_confirm', methods=['POST'])
def error_delete_confirm():

    mId = session.get('signed_member_Id')

    if not mId:
        return redirect(url_for('member.signin_form'))
    
    eNum = request.form['eNum']
    
    critical_errors = load_errors()

    if eNum in critical_errors:
        del critical_errors[eNum]

    save_errors(critical_errors)

    return render_template('trouble_forms/error_delete_result.html', eNum = eNum)

# /trouble/error_list_view
@trouble_bp.route('/error_list', methods=['GET'])
def error_list_view():
    
    mId  = session['signed_member_Id']
   
    if not mId:
        return redirect(url_for('member.signin_form'))
    
    critical_errors = load_errors()
     
    if mId not in critical_errors or not critical_errors[mId]:
        
        return redirect(url_for('new_critical_error_form'))
    
    staff_errors = critical_errors.get(mId, {})
    
    error_lists = list(staff_errors.items())
    error_lists.reverse()
    
    return render_template('trouble_forms/error_list_result.html', mId = mId, critical_errors = error_lists)
     
# /trouble/error_info/<eNum>
@trouble_bp.route('/error_info/<aNum>', methods=['GET'])
def error_infos(eNum):
    mId = session.get('signed_member_Id')
    if not mId:
        return redirect(url_for('member.signin_form'))
    
    critical_errors = load_errors()
  
    staff_errors = critical_errors.get(mId, {})
    
    if eNum not in staff_errors:
        return render_template('trouble_forms/error.html', errorMsg="That Error NOT FOUND!")

    return render_template('trouble_forms/error_lnfo.html', critical_errors=staff_errors[eNum])
   
       
# list view 방식을 쭉 테이블 형식으로 보여줄지 
# 그자리에서 클릭하면 큰 창을 띄워서 그 특정 데이터만 확실하게 정보를 보여줄지 고민 