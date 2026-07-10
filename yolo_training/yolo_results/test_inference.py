from ultralytics import YOLO
import cv2
import os

model = YOLO(r'C:\Alot1team\project\troubleshooting\yolo_trainning\results\my_experiment_v1-13\weights\best.pt')

# 테스트할 파일 경로 (이미지든 영상이든 여기만 바꾸세요)
file_path = r'C:\Alot1team\project\troubleshooting\test\video1.mp4' # 혹은 .mp4

# 파일 확장자로 이미지인지 영상인지 구분
is_image = file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))

if is_image:
    # --- 사진 처리 ---
    results = model(file_path, conf=0.3)
    annotated_frame = results[0].plot()

    cv2.namedWindow("Detection Result", cv2.WINDOW_NORMAL)
    cv2.imshow("Detection Result", annotated_frame)
    cv2.waitKey(0) # 아무 키나 누를 때까지 대기
else:
    # --- 영상 처리 ---
    cap = cv2.VideoCapture(file_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        
        results = model(frame, conf=0.3)
        annotated_frame = results[0].plot()
        
        cv2.imshow("Detection Result", annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break
    cap.release()

cv2.destroyAllWindows()