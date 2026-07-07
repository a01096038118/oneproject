window.onload = function () {
    loadLogs();
};

// =========================
// 로그 목록 불러오기
// =========================
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
                    🗑️
                </button>

            </div>
        `;
    });

}

// =========================
// 로그 클릭
// =========================
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

const alertLayer = document.getElementById('intrusionAlert');
// 침입 감지 시 (즉시 켜짐)
function triggerAlert() {
    alertLayer.classList.add('active');
}

// 침입 해제 시 (CSS transition에 의해 스르륵 꺼짐)
function clearAlert() {
    alertLayer.classList.remove('active');
}

const audio = document.getElementById('sirenAudio');
        let fadeInterval = null; // Fade-out 타이머 저장용 변수

// [침입 발생] 소리 즉시 재생
function triggerAlert() {
    // 혹시 작동 중이던 Fade-out 타이머가 있다면 초기화
    clearInterval(fadeInterval); 
    
    audio.volume = 1.0; // 음량을 최대(100%)로 설정
    audio.play().catch(error => {
        alert("브라우저 보안 정책상, 화면을 한 번 클릭한 뒤 버튼을 눌러주세요!");
    });
}

// [상황 해제] 소리가 자연스럽게 스르륵 꺼짐 (Fade-out)
function clearAlert() {
    // 이미 음량이 0이거나 일시정지 상태면 무시
    if (audio.paused || audio.volume === 0) return;

    // 0.05초(50ms)마다 음량을 조금씩 줄이는 타이머 가동
    fadeInterval = setInterval(() => {
        if (audio.volume > 0.05) {
            audio.volume -= 0.05; // 음량을 5%씩 감소
        } else {
            // 음량이 거의 0에 도달하면 완전히 끄고 타이머 종료
            audio.volume = 0;
            audio.pause();
            clearInterval(fadeInterval);
        }
    }, 50); // 50밀리초 주기 (약 1초 동안 부드럽게 사라짐)
}