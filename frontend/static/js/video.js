// Flask static 폴더 구조에 맞게 경로를 지정합니다.
const playlist = [
    "/static/img/drone1.mp4",
    "/static/img/drone2.mp4",
    "/static/img/drone3.mp4",
    "/static/img/drone4.mp4"
];

let currentVideoIndex = 0;

// HTML의 id인 'bg-video'와 일치시킵니다.
const videoElement = document.getElementById("bg-video");

function loadVideo(index) {
    if (index < playlist.length) {
        videoElement.src = playlist[index];
        videoElement.play().catch(error => {
            console.log("자동 재생이 차단되었습니다:", error);
        });
    }
}

// 영상이 끝났을 때(ended) 다음 영상으로 넘어가는 이벤트 리스너
videoElement.addEventListener("ended", () => {
    currentVideoIndex++;
    
    // 마지막 영상이 끝나면 다시 처음(0)으로 돌아가기
    if (currentVideoIndex >= playlist.length) {
        currentVideoIndex = 0;
    }
    
    loadVideo(currentVideoIndex);
});

// 페이지가 로드되었을 때 첫 번째 비디오 실행
window.addEventListener("DOMContentLoaded", () => {
    loadVideo(currentVideoIndex);
});