// 1. 재생할 영상 파일 경로들을 순서대로 배열에 넣습니다.
const playlist = [
    "../img/drone1.mp4",
];

let currentVideoIndex = 0;
const videoElement = document.getElementById("myVideo");

// 2. 첫 번째 영상 설정 및 재생
function loadVideo(index) {
    if (index < playlist.length) {
        videoElement.src = playlist[index];
        videoElement.play().catch(error => {
            console.log("자동 재생이 차단되었습니다. 사용자의 클릭이 필요할 수 있습니다:", error);
        });
    } else {
        console.log("모든 영상 재생이 완료되었습니다.");
        // 처음부터 다시 무한 반복하고 싶다면 아래 주석을 해제하세요.
        // currentVideoIndex = 0;
        // loadVideo(currentVideoIndex);
    }
}

// 3. 영상이 끝났을 때(ended) 다음 영상으로 넘어가는 이벤트 리스너
videoElement.addEventListener("ended", function() {
    currentVideoIndex++; // 다음 인덱스로
    loadVideo(currentVideoIndex);
});

// 페이지 로드 시 첫 영상 시작
loadVideo(currentVideoIndex);