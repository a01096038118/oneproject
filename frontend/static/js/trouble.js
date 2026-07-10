function submitCriticalErrorForm() {
    console.log('submitCriticalErrorForm')

    alert("REGIST COMPLETE!");

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

function openModal(eNum) {
    console.log('errorModifyForm')

    currentEnum = eNum

    document.getElementById('modal_test').style.display = 'flex'; 
}

function closeModal() { 
    document.getElementById('modal_test').style.display = 'none'; 
}


function saveModalform() {
    console.log('saveModalform')

    let form = document.saveModalform;

    const newResolution = document.getElementById('resolutionInput').value
    const newProgress = document.getElementById('progressInput').value

    const dataToSend = {
        resolution : newResolution,
        progress : newProgress,
        errorid : currentEnum
    }

    fetch('/trouble/error_modify_confirm', {
        method: 'POST', 
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataToSend)   // 자바스크립트 객체를 "문자열(String) 형태의 JSON"으로 변환
    })
    .then(response => response.json())
    .then(data => {
        console.log("SERVER:", data);
        alert("SAVE COMPLETE!");
        document.getElementById('resolutionInput').value = '';
        closeModal();
    })
    .catch(error => console.error("ERROR:", error));
}

try {
    const res = await fetch('/api/data');
    
    if (!res.ok) {
        throw new Error(`Server Error (Status Code: ${res.status})`);
    }

    const data = await res.json(); 
    alert(data.message);

} catch (error) {
    console.error("TroubleShooting Error:", error);
    alert("Server Connection Error");
}
