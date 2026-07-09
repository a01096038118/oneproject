//  로그 기록
window.onload = function() {
    loadLogs();
};

function loadLogs(){

    fetch("/dashboard/logs")
    .then(response => response.json())
    .then(data => {
        
            let html = "";
            
            data.forEach(log => {
                html += `
                    <p onclick="check_log('${log.log_id}')">
                    ${log.log_id}</p>
                    
                    <small>${log.zone_id}</small>
                    <hr>
                `;
            });
            document.getElementById("log_box").innerHTML = html;
        });
    }
        
// check
function check_log(logId){
    
    fetch(`/dashboard/check_log/${logId}`, 
        { method: "POST", 
        headers: {
            "Content-Type":"application/json"
        }, 
        body: JSON.stringify({}) 
        })
        .then(res => res.json())
        .then(data => {
            console.log("backend data:", data);
 

        document.getElementById("manager").innerText = data.manager || "-";
        
        document.getElementById("detected_time").innerText = data.detected_time || "-";

        document.getElementById("person_count").innerText = data.person_count !== undefined ? data.person_count + "명" : "-";
        const checkedTimeTarget = document.getElementById("checked_time")|| document.getElementById("cehcked_time");
        if (checkedTimeTarget) {
            checkedTimeTarget.innerText = data.checked_time || "-";
        }
        
        const dangerStatusTarget = document.getElementById("danger_status");
        if(dangerStatusTarget) {
            dangerStatusTarget.innerText = data.status || "위험구역 감지";
        }

        let imgHtml = "";
        if (data.captured_image_path){
            const filename = data.captured_image_path.split("/").pop();
            imgHtml = `<img src="/dashboard/external_img/${filename}" style="width:100%; max-width:400px; border-radius:10px; margin-top:10px;">`;
        } else {
            imgHtml = '<p style="color:#9ca3af; margin-top:10px;">[저장된 캡처 이미지가 없습니다]</p>';
        }

        document.getElementById("log_detail").innerHTML = `
            <h4> 로그 상세 내용</h4>
            <p>상태: <span style="font-weight:bold; color:#ef4444;">${data.status}</span></p>
            ${imgHtml}
        `;
    })
        // // 5. 확인 시간 매핑
        // const checkedTimeTarget = document.getElementById("checked_time");
        // if (checkedTimeTarget) {
        //     checkedTimeTarget.innerText = logData.checked_time || "-";
        // }

        // // 6. 이미지 및 상세 영역 처리
        // const logDetailTarget = document.getElementById("log_detail");
        // if (logDetailTarget) {
        //     let imgHtml = "";
            
        //     if (logData.captured_image_path && typeof logData.captured_image_path === 'string') {
        //         // "external_img/파일명.jpg" 구조에서 파일명만 추출
        //         const filename = logData.captured_image_path.split("/").pop();
                
        //         if (filename) {
        //             imgHtml = `<img src="/dashboard/external_img/${filename}" style="width:100%; max-width:400px; border-radius:10px; margin-top:10px;">`;
        //         }
        //     } else {
        //         imgHtml = `<p style="color:#9ca3af; margin-top:10px;">[저장된 캡처 이미지가 없습니다]</p>`;
        //     }

        //     // JSON의 'message' 필드를 상태 텍스트로 활용 (예: 위험구역 침범 감지)
        //     const statusText = logData.message || logData.status || "기록없음";

        //     logDetailTarget.innerHTML = `
        //         <h4>로그 상세 내용</h4>
        //         <p>상태: <span style="font-weight:bold; color:#38bdf8;">${statusText}</span></p>
        //         ${imgHtml}
        //     `;
        // }
    
}