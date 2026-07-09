import pandas as pd
import io
from flask import Blueprint, render_template, request, session, jsonify, send_file
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

    cId = session.get('signedInMemberId')
    admId = session.get('signedInAdminId')

    mId = cId if cId else admId

    if not mId:
        return jsonify({"status": "fail", "message": "Login required"}), 401 

    eNum = str(uuid.uuid4())    

    return render_template('trouble/new_critical_error_form.html', eNum = eNum)

#new_critical_error_confirm
@trouble_bp.route('/new_critical_error_confirm', methods=['POST'])
def new_critical_error_confirm():

    cId = session.get('signedInMemberId')
    admId = session.get('signedInAdminId')

    mId = cId if cId else admId

    if not mId:
        return jsonify({"status": "fail", "message": "Login required"}), 401 
    
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

    return render_template('trouble/new_critical_error_result.html')

#/error_modify_confirm
@trouble_bp.route('/error_modify_confirm', methods=['POST'])
def error_modify_confirm():
     
    cId = session.get('signedInMemberId')
    admId = session.get('signedInAdminId')

    mId = cId if cId else admId

    if not mId:
        return jsonify({"status": "fail", "message": "Login required"}), 401 
    
    critical_errors = load_errors()

    regdatetime = time.getCurrentDateTime()

    data = request.get_json()
    resolution = data.get('resolution')
    progress = data.get('progress')
    errorid = data.get('errorid')

    eNum = errorid

    target = None
    
    for errors in critical_errors.values():
        if eNum in errors:
            target = errors[eNum]
            target['resolution'] = resolution
            target['date'] = regdatetime
            target['progress'] = progress
            break        

    save_errors(critical_errors)
    
    return jsonify({"status": "success", "message": "Modified Complete!"})

# /trouble/error_list_view
@trouble_bp.route('/error_list', methods=['GET'])
def error_list_view():
    
    cId = session.get('signedInMemberId')
    admId = session.get('signedInAdminId')

    mId = cId if cId else admId

    if not mId:
        return jsonify({"status": "fail", "message": "Login required"}), 401 
    
    critical_errors = load_errors()

    all_error_list = []

    for staff_id, error_info in critical_errors.items():
        for error_num, error_detail in error_info.items():

            errors = error_detail.copy()  

            errors['staff_id'] = staff_id
            errors['error_num'] = error_num
           
            all_error_list.append(errors)

    all_error_list = sorted(all_error_list, key=lambda x: x['date'], reverse=True)     
   
    return render_template('trouble/error_list_result.html', all_error_list = all_error_list)
     
# /trouble/error_info/<eNum>
@trouble_bp.route('/error_info/<eNum>', methods=['GET'])
def error_infos(eNum):

    cId = session.get('signedInMemberId')
    admId = session.get('signedInAdminId')

    mId = cId if cId else admId

    if not mId:
        return jsonify({"status": "fail", "message": "Login required"}), 401 
    
    critical_errors = load_errors()

    target_error = None

    for staff_id, value in critical_errors.items():
        if eNum in value:
            target_error = value[eNum].copy()
            target_error['staff_id'] = staff_id
            target_error['eNum'] = eNum
            break 

    return render_template('trouble/error_lnfo.html', eNum = eNum, target_error = target_error)
   
@trouble_bp.route('/download_excel')
def download_excel():

    cId = session.get('signedInMemberId')
    admId = session.get('signedInAdminId')

    mId = cId if cId else admId

    if not mId:
        return jsonify({"status": "fail", "message": "Login required"}), 401 
  
    data = load_errors()

    all_errors = [] 

    for Id, values in data.items(): 
        for error_num, infos in values.items():

            errors = infos.copy()
            errors['Id'] = Id
            errors['error_num'] = error_num

            all_errors.append(errors)

    df = pd.DataFrame(all_errors)
    
    cols = ['Id', 'error_num', 'category', 'issue', 'error_code', 'progress', 'resolution','date']
    df = df[cols]
    df.columns = ['Staff ID', 'NO.', 'Category', 'Issue', 'Error Code', 'Progress', 'Resolution','Date']

    buffer = io.BytesIO()

    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Error Status')
        
        worksheet = writer.sheets['Error Status']
        
        worksheet.column_dimensions['A'].width = 12 
        worksheet.column_dimensions['B'].width = 40 
        worksheet.column_dimensions['C'].width = 12 
        worksheet.column_dimensions['D'].width = 40 
        worksheet.column_dimensions['E'].width = 60 
        worksheet.column_dimensions['F'].width = 15 
        worksheet.column_dimensions['G'].width = 60 
        worksheet.column_dimensions['H'].width = 25 

        from openpyxl.styles import Alignment
        for row in worksheet.iter_rows(min_row=2, max_col=6, max_row=worksheet.max_row):
            for cell in row:
                cell.alignment = Alignment(wrap_text=True, vertical='center')

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name='Team_Error_Report.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )