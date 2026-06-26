function submitTroubleForm() {
    console.log('submitTroubleForm')

    // alert("");

    let form = document.submitTroubleForm;

    let issue = form.issue.value.trim();

    console.log('issue:', issue)
    
    if (issue === '') {
        alert('Please input your issue')
        form.issue.focus();
    } else if (issue.length < 50) {
    alert('Account issue at least 50digits!!'); 
    form.issue.focus();
    
    } else {
        form.submit();
    }
}

function copyAccountNum(accountNumber) {
    console.log('copyAccountToClipboard')

        navigator.clipboard.writeText(accountNumber)
            .then(() => {
                alert("COPY COMPLETE!");
            })  
            .catch(err => {
                console.error("fail issue:", err);
                alert("COPY FAILED!");
            });
}

function depositForm() {
    console.log('depositForm')

    let form = document.deposit_form;

    let aPw = form.aPw.value.trim(); 
    let dAmount = form.dAmount.value.trim();

    console.log('dAmount:', dAmount)
    
    if (aPw === '') {
        alert('Please input Account PW!!')
        form.aPw.focus();
    } else if (dAmount === '') {
        alert('Please input DEPOSIT AMOUNT!!')
        form.dAmount.focus();
    }  else {
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