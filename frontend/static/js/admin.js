
// ADMIN JS
function signupForm() {
    console.log('signupForm() CALLED!!')

    let form = document.signup_form;

    let mId = form.mId.value.trim();
    let mPw = form.mPw.value.trim();
    let mMail = form.mMail.value.trim();
    let mPhone = form.mPhone.value.trim();
    

    let mIdPattern = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z0-9]{4,20}$/;
    let mPwPattern = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[\W_])[^\s]{8,20}$/;
    let mMailPattern = /^[\w.-]+@[\w.-]+\.[A-Za-z]{2,5}$/;
    let mPhonePattern = /^\d{10,11}$/;
    
    
    if (mId === "") {
        alert("PLEASE INPUT ADMIN ID");
        form.mId.focus();
        
        
    } else if (!mIdPattern.test(mId)) {
        alert("아이디: 영문, 숫자 포함 4자 이상 20자 이하로 입력해주세요.")
        form.mId.focus();
        

    } else if (mPw === "") {
        alert("PLEASE INPUT ADMIN PW");
        form.mPw.focus();
        

    } else if (!mPwPattern.test(mPw)) {
        alert("비밀번호: 특수문자, 영문, 숫자 포함하여 8자리 이상 20자리 이하로 입력해주세요.")
        form.mPw.focus();
        

    } else if (mMail === "") {
        alert("PLEASE INPUT ADMIN MAIL");
        form.mMail.focus();
        

    } else if (!mMailPattern.test(mMail)) {
        alert("올바른 이메일 형식이 아닙니다.");
        form.mMail.focus();
        
        
    } else if (mPhone === "") {
        alert("PLEASE INPUT ADMIN PHONE");
        form.mPhone.focus();
        

    } else if (!mPhonePattern.test(mPhone)) {
        alert("숫자만 입력해주세요.");
        form.mPhone.focus();
        
    } 
    else {
        form.submit();
    }
}


function copyToClipboard() {
    const keyText = document.getElementById('adminKey').innerText;

    // 최신 브라우저 Clipboard API 지원 여부 확인 후 복사
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(keyText).then(() => {
            alert('관리자 키가 클립보드에 복사되었습니다!\n안전한 곳에 붙여넣기(Ctrl+V)하여 저장하세요.');
        }).catch(err => {
            fallbackCopy(keyText);
        });
    } else {
        fallbackCopy(keyText);
    }
    }

// 구형 브라우저 환경을 위한 예외 처리용 임시 복사 방식
function fallbackCopy(text) {
    const dummy = document.createElement("textarea");
    document.body.appendChild(dummy);
    dummy.value = text;
    dummy.select();
    document.execCommand("copy");
    document.body.removeChild(dummy);
    alert('관리자 키가 클립보드에 복사되었습니다!');
}


function signinForm() {
    console.log('signinForm() CALLED!!')

    let form = document.signin_form;

    let mId = form.mId.value.trim();
    let mPw = form.mPw.value.trim();
    let admin_key = form.admin_key.value.trim();

    let mIdPattern = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z0-9]{4,20}$/;
    let mPwPattern = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[\W_])[^\s]{8,20}$/;
    let adminKeyPattern =/^[A-Za-z0-9-]+$/;

    
    if (mId === "") {
        alert("PLEASE INPUT ADMIN ID");
        form.mId.focus();
    
        
    } else if (!mIdPattern.test(mId)) {
        alert("ID가 존재하지않습니다.")
        form.mId.focus();
        

    } else if (mPw === "") {
        alert("PLEASE INPUT ADMIN PW");
        form.mPw.focus();
        
    
    } else if (!mPwPattern.test(mPw)) {
       alert("특수문자, 영문, 숫자 포함하여 8자리 이상 20자리 이하로 입력해주세요.")
       form.mPw.focus();
       

    } else if (admin_key === "") {
        alert("PLEASE INPUT ADMIN KEY");
        form.admin_key.focus();

    } else if (!adminKeyPattern.test(admin_key)) {
        alert("KEY NUMBER NO MACTH")
        form.admin_key.focus();
    }
    else {
        form.submit();
    }

}

function modifyForm() {
    console.log('modifyForm() CALLED!!')

    let form = document.modify_form;

    let mPw = form.mPw.value.trim();
    let mMail = form.mMail.value.trim();
    let mPhone = form.mPhone.value.trim();
    
    if (mPw === "") {
        alert("PLEASE INPUT ADMIN PW");
        form.mPw.focus();

    } else if (mMail === "") {
        alert("PLEASE INPUT ADMIN MAIL");
        form.mMail.focus();

    } else if (mPhone === "") {
        alert("PLEASE INPUT ADMIN PHONE");
        form.mPhone.focus();

    } else {
        alert("ADMIN DATA MODIFY SUCCESS!!")
        form.submit();

    }

}

function deleteForm() {
     return confirm("정말 삭제하시겠습니까?");
    }
