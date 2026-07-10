import cv2
import os

# ⚙️ 설정 부분
video_path = r'C:\Alot1team\project\videos\test_video.mp4'  # 원본 동영상 경로
output_folder = r'C:\Alot1team\project\extracted_frames'    # 추출된 이미지가 저장될 경로
frame_interval = 30  # 30프레임마다 1장 추출 (1초에 1장)

def extract_frames():
    # 저장 폴더 생성
    os.makedirs(output_folder, exist_ok=True)
    
    # 동영상 열기
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"❌ 에러: 동영상 파일을 열 수 없습니다: {video_path}")
        return

    frame_count = 0
    saved_count = 0

    print(f"⏳ 프레임 추출을 시작합니다 (주기: {frame_interval}프레임마다)...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # 설정한 간격마다 이미지 저장
        if frame_count % frame_interval == 0:
            filename = os.path.join(output_folder, f"frame_{saved_count:05d}.jpg")
            cv2.imwrite(filename, frame)
            saved_count += 1
            
        frame_count += 1

    cap.release()
    print(f"🎉 완료! 총 {saved_count}장의 이미지가 '{output_folder}'에 저장되었습니다.")

if __name__ == "__main__":
    extract_frames()