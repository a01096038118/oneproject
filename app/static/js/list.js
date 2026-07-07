window.onload = function () {
    renderLogList();
};

document.addEventListener("DOMContentLoaded", () => {
    // 백엔드 데이터(jsonLogResponse)가 있으면 사용하고, 없으면 샘플 데이터 사용
    if (typeof jsonLogResponse !== 'undefined') {
        renderLogList(jsonLogResponse);
    } else {
        const sampleData = [
            { log_id: 102, danger_zone: "A구역 (제한통제)", person_count: 2, detected_time: "2026-07-07 14:56:22", manager: "관리자A", checked_time: "2026-07-07 15:00:11" },
            { log_id: 101, danger_zone: "B구역 (자재창고)", person_count: 1, detected_time: "2026-07-07 13:22:05", manager: "관리자B", checked_time: "-" }
        ];
        renderLogList(sampleData);
    }
});

function renderLogList(log_list) {
    const container = document.getElementById("log_list_container");
    if (!container) return;

    // container.innerHTML = ""; // 초기화

    log_list.forEach(log => {
        // 기존의 가로 일렬 배치를 위한 행(Row) 생성
        const row = document.createElement("div");
        row.className = "log_data_row"; 

        row.innerHTML = `
            <div class="log_id_block">
                <span>로그 NO.</span>
                <strong>${log.log_id}</strong>
            </div>
            
            <div class="danger_box">
                <h4>위험 구역</h4>
                <p class="highlight_red">${log.danger_zone}</p>
            </div>
            
            <div class="info_item">
                <h4>감지 인원</h4>
                <p class="highlight_red">${log.person_count} 명</p>
            </div>
            
            <div class="info_item">
                <h4>감지된 시간</h4>
                <p>${log.detected_time}</p>
            </div>
            
            <div class="info_item">
                <h4>담당자</h4>
                <p>${log.manager}</p>
            </div>
            
            <div class="info_item">
                <h4>확인 시간</h4>
                <p>${log.checked_time || '-'}</p>
            </div>
        `;

        container.appendChild(row);
    });
}