window.onload = function () {
    loadLogs();
};

async function loadLogs() {

    try {

        const response = await fetch("/dashboard/logs");

        const log_list = await response.json();
        console.log(log_list);

        renderLogList(log_list);

    } catch(error) {
        console.error("로그 조회 실패:", error);
    }
}

function renderLogList(log_list) {
    const container = document.getElementById("log_list_container");

    if(!container) return;

    container.innerHTML = "";

    log_list.forEach(log => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${log.log_id}</td>
            <td>${log.danger_zone.zone_id}</td>
            <td>${log.person_count} 명</td>
            <td>${log.detected_time}</td>
            <td>${log.manager || "-"}</td>
            <td>${log.checked_time || "-"}</td>
            `;

        container.appendChild(row);
    });
}


function downloadLogs() {
    window.location.href = "/dashboard/download_report";
}