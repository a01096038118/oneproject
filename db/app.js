// 대시보드 화면이 로드될 때 실행할 자바스크립트 예시
async function loadRescueLogs() {
   
    const response = await fetch('/api/dashboard/logs');
    const logs = await response.json(); 
    
    const tableBody = document.getElementById('log-table-body');
    tableBody.innerHTML = ''; 
    
    
    logs.forEach(item => {
        const row = `
            <tr>
                <td>${item.incident_id}</td>          <!-- 사건 번호 (중복X) -->
                <td>${item.detected_status}</td>      <!-- 탐지 상태 (Person_Detected) -->
                <td>${item.detected_time}</td>        <!-- 발생 시각 (년-월-일 시:분:초) -->
                <td>
                    <!-- 이미지 주소 그대로 img 태그에 넣으면 C드라이브에서 사진 꺼내와서 보여줌 -->
                    <img src="/${item.captured_image_path}" width="150" alt="조난자 사진">
                </td>
            </tr>
        `;
        tableBody.insertAdjacentHTML('beforeend', row);
    });
}
