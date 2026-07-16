// html이 준비되면 실행되는 함수
window.onload = function () {
    loadLogs();
};


// 로그 목록 불러오기

async function loadLogs() {

    const response = await fetch("/dashboard/logs");
    const logs = await response.json();

    const logBox = document.getElementById("log_box");

    logBox.innerHTML = "<h4>로그 목록</h4>";

    logs.forEach(log => {

        logBox.innerHTML += `
            <div class="log_item">

                <div class="log_info"
                     onclick="checkLog('${log.log_id}')">

                    <b>${log.log_id}</b><br>
                    <small>${log.detected_time}</small>

                </div>

                <button class="delete_btn"
                    onclick="event.stopPropagation(); deleteLog('${log.log_id}')">
                    // 부모 클릭이벤트가 실행되지않게함
                    🗑️
                </button>

            </div>
        `;
    });

}


// 로그 클릭

async function checkLog(logId){

    const response = await fetch(
        `/dashboard/check_log/${logId}`,
        {
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({})
        }
    );

    const data = await response.json();

    const log = data.checked_log;

    if(!data.success){
        alert(data.message);
        return;
    }

    // 담당자
    document.getElementById("manager").innerText =
        log.manager ?? "미확인";

    // 감지 인원
    document.getElementById("person_count").innerText =
        log.person_count + "명";

    // 감지 시간
    document.getElementById("detected_time").innerText =
        log.detected_time;

    // 확인 시간
    document.getElementById("checked_time").innerText =
        log.checked_time ?? "-";

    // 위험구역
    document.getElementById("danger_zone").innerText =
        log.zone_id;

    // 이미지
    let imageHtml = "";

    if(log.captured_image_path){

        const filename =
            log.captured_image_path.split("/").pop();

        imageHtml =
        `<img src="/dashboard/external_img/${filename}"
              style="width:100%;
                     max-width:500px;
                     border-radius:10px;">`;

    }

    document.getElementById("log_detail").innerHTML = `
        <h4>로그 상세</h4>

        <p>
            <b>상태 :</b>
            ${log.message}
        </p>

        ${imageHtml}
    `;

}

async function deleteLog(logId){

    if(!confirm("삭제하시겠습니까?")){
        return;
    }

    const response = await fetch(
        `/dashboard/delete_log/${logId}`,
        {
            method:"DELETE"
        }
    );

    const result = await response.json();

    if(result.success){

        alert("삭제되었습니다.");

        // 로그 목록 새로고침
        loadLogs();

        // 상세 정보 초기화
        document.getElementById("person_count").innerText = "-";
        document.getElementById("manager").innerText = "-";
        document.getElementById("detected_time").innerText = "-";
        document.getElementById("checked_time").innerText = "-";
        document.getElementById("danger_zone").innerText = "-";
        document.getElementById("log_detail").innerHTML =
            "<h4>로그 상세</h4>";

    }else{

        alert(result.message);
    }

}

// const alertLayer = document.getElementById('intrusionAlert');
// // 침입 감지 시 (즉시 켜짐)
// function triggerAlert() {
//     alertLayer.classList.add('active');
// }

