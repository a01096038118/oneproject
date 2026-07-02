function signupForm() {
    console.log('signupForm() CALLED!!')

    let form = document.signup_form;

    let mId = form.mId.value.trim();
    let mPw = form.mPw.value.trim();
    let mMail = form.mMail.value.trim();
    let mPhone = form.mPhone.value.trim();
    let mCareer = form.mCareer.value.trim();

    let mIdPattern = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z0-9]{4,20}$/;
    let mPwPattern = /^(?=.*[A-Za-z])(?=.*\d)[^\s]{8,20}$/;
    let mMailPattern = /^[\w.-]+@[\w.-]+\.[A-Za-z]{2,5}$/;
    let mPhonePattern = /^\d{10,11}$/;
    let mCareerPattern = /^\d+개월$/;
    
    if (mId === "") {
        alert("PLEASE INPUT MEMBER ID");
        form.mId.focus();
        
        
    } else if (!mIdPattern.test(mId)) {
        alert("아이디: 영문, 숫자 포함 4자 이상 20자 이하로 입력해주세요.")
        form.mId.focus();
        

    } else if (mPw === "") {
        alert("PLEASE INPUT MEMBER PW");
        form.mPw.focus();
        

    } else if (!mPwPattern.test(mPw)) {
        alert("비밀번호: 특수문자, 영문, 숫자 포함하여 8자리 이상 20자리 이하로 입력해주세요.")
        form.mPw.focus();
        

    } else if (mMail === "") {
        alert("PLEASE INPUT MEMBER MAIL");
        form.mMail.focus();
        

    } else if (!mMailPattern.test(mMail)) {
        alert("올바른 이메일 형식이 아닙니다.");
        form.mMail.focus();
        
        
    } else if (mPhone === "") {
        alert("PLEASE INPUT MEMBER PHONE");
        form.mPhone.focus();
        

    } else if (!mPhonePattern.test(mPhone)) {
        alert("숫자만 입력해주세요.");
        form.mPhone.focus();
        

    } else if (mCareer === "") {
        alert("PLEASE INPUT YOUR CAREER MONTH");
        form.mCareer.focus(); 
        
    } else if (!mCareerPattern.test(mCareer)){
        alert("경력사항: 숫자+개월 형식으로 입력해주세요.");
        form.mCareer.focus();
    
        
    } else {
        
        form.submit();
    }

}

function signinForm() {
    console.log('signinForm() CALLED!!')

    let form = document.signin_form;

    let mId = form.mId.value.trim();
    let mPw = form.mPw.value.trim();

    let mIdPattern = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z0-9]{4,20}$/;
    let mPwPattern = /^(?=.*[A-Za-z])(?=.*\d)[^\s]{8,20}$/;
    
    if (mId === "") {
        alert("PLEASE INPUT MEMBER ID");
        form.mId.focus();
    
        
    } else if (!mIdPattern.test(mId)) {
        alert("ID가 존재하지않습니다.")
        form.mId.focus();
        

    } else if (mPw === "") {
        alert("PLEASE INPUT MEMBER PW");
        form.mPw.focus();
        
    
    } else if (!mPwPattern.test(mPw)) {
       alert("틀린 비밀번호입니다.")
       form.mPw.focus();
       

    } else {
        alert("SIGNIN SUCCESS!!")
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
        alert("PLEASE INPUT MEMBER PW");
        form.mPw.focus();

    } else if (mMail === "") {
        alert("PLEASE INPUT MEMBER MAIL");
        form.mMail.focus();

    } else if (mPhone === "") {
        alert("PLEASE INPUT MEMBER PHONE");
        form.mPhone.focus();

    } else {
        alert("MEMBER DATA MODIFY SUCCESS!!")
        form.submit();

    }

}