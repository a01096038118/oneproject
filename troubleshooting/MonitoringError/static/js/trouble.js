function submitCriticalErrorForm() {
    console.log('submitCriticalErrorForm')

    // alert("");

    let form = document.newErrorForm;

    let error_code = form.error_code.value;
    let issue = form.issue.value;
   
    if (error_code === '') {
        alert('Please input your issue')
        form.error_code.focus();
    } else if (issue === '') {
        alert('Please input error code')
        form.issue.focus();
    } else {
        form.submit();
    }
}

function errorModifyForm() {
    console.log('errorModifyForm')

    let form = document.Modify_form;

    let resolution = form.resolution.value; 
    
    if (resolution === '') {
        alert('Please input how to resolve!!')
        form.resolution.focus();
    } else {
        form.submit();
    }
}


function withdrawalForm() {
    console.log('withdrawalForm')

    let form = document.withdrawal_form;

    let aPw = form.aPw.value.trim(); 
    let wAmount = form.wAmount.value.trim();

    console.log('wAmount:', wAmount)
    
    if (aPw === '') {
        alert('Please input Account PW!!')
        form.aPw.focus();
    } else if (wAmount === '') {
        alert('Please input WITHDRAWAL AMOUNT!!')
        form.wAmount.focus();
    }  else {
        form.submit();
    }
}


function accModifyForm() {
    console.log('accModifyForm')

    let form = document.Modify_form;

    let aPw = form.aPw.value.trim();

    console.log('aPw:', aPw)

    if  (aPw === '') {
         alert('Please input New Account PW!!')
         form.aPw.focus();
    } else {
        form.submit();
    }
}

function accDeleteForm() {
    console.log('accDeleteForm')

    let form = document.Delete_form;

    let aNum = form.aNum.value.trim();

    console.log('aNum', aNum)

    if  (aNum === '') {
         alert('Please input Account Num!!')
         form.aNum.focus();
    } else {
        form.submit();
    }

}