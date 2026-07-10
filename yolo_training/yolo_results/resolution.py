import os

label_dir = r'C:\Alot1team\project\troubleshooting\yolo_trainning\dataset\labels'
img_dir = r'C:\Alot1team\project\troubleshooting\yolo_trainning\dataset\images'

# 확장자 제외한 파일명 세트 생성
label_names = set(f.rsplit('.', 1)[0] for f in os.listdir(label_dir) if f.endswith('.txt'))
image_names = set(f.rsplit('.', 1)[0] for f in os.listdir(img_dir) if f.endswith(('.jpg', '.png', '.jpeg')))

# 1. 이미지는 없는데 라벨만 있는 경우 (짝을 잃은 라벨)
missing_images = label_names - image_names
print(f"짝을 잃은 라벨 파일 개수: {len(missing_images)}")
for name in list(missing_images)[:10]: # 10개까지만 예시 출력
    print(f"이미지 없음: {name}.txt")

# 2. 라벨은 없는데 이미지만 있는 경우
missing_labels = image_names - label_names
print(f"짝을 잃은 이미지 파일 개수: {len(missing_labels)}")
for name in list(missing_labels)[:10]:
    print(f"라벨 없음: {name}.jpg/png")