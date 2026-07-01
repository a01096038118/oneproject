// 대시보드 화면이 로드될 때 실행할 자바스크립트 예시
async function loadRescueLogs() {
   
    const response = await fetch('/api/dashboard/logs');
    const logs = await response.json(); 
    
    const tableBody = document.getElementById('log-table-body');
    tableBody.innerHTML = ''; 
    
    
    logs.forEach(item => {
        const row = `
            <tr>
                <td>${item.incident_id}</td>          <td>${item.detected_status}</td>      <td>${item.detected_time}</td>        <td>
                    <img src="/${item.captured_image_path}" width="150" alt="조난자 사진">
                </td>
            </tr>
        `;
        tableBody.insertAdjacentHTML('beforeend', row);
    });
}