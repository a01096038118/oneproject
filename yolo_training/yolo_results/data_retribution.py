import os
import shutil
import random

# 1. 경로 설정
base_dir = r'C:\Alot1team\project\troubleshooting\yolo_trainning\dataset'
images_dir = os.path.join(base_dir, 'images')
labels_dir = os.path.join(base_dir, 'labels')
train_dir = os.path.join(base_dir, 'train')
val_dir = os.path.join(base_dir, 'val')

# 2. train/val 폴더 초기화 
for folder in [train_dir, val_dir]:
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(os.path.join(folder, 'images'))
    os.makedirs(os.path.join(folder, 'labels'))

# 3. 파일 리스트 가져오기
image_files = [f for f in os.listdir(images_dir) if f.endswith(('.jpg', '.png', '.jpeg'))]
random.shuffle(image_files)

# 4. 8:2 비율로 분할
split_idx = int(len(image_files) * 0.8)
train_files = image_files[:split_idx]
val_files = image_files[split_idx:]

def move_files(files, target_folder):
    for f in files:
        # 이미지 이동
        shutil.copy(os.path.join(images_dir, f), os.path.join(target_folder, 'images', f))
        # 라벨 이동 (txt 파일)
        label_file = f.rsplit('.', 1)[0] + '.txt'
        if os.path.exists(os.path.join(labels_dir, label_file)):
            shutil.copy(os.path.join(labels_dir, label_file), os.path.join(target_folder, 'labels', label_file))

# 5. 실행
print("학습 데이터 재분할 시작...")
move_files(train_files, train_dir)
move_files(val_files, val_dir)
print(f"완료! 학습 데이터: {len(train_files)}장, 검증 데이터: {len(val_files)}장")