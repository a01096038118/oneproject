import os

# 경로를 절대 경로로 정확히 다시 지정하세요
images_dir = r'C:\Alot1team\project\troubleshooting\yolo_trainning\dataset\images\val'
labels_dir = r'C:\Alot1team\project\troubleshooting\yolo_trainning\dataset\labels\val'

def remove_unlabeled_images(img_path, lbl_path):
    count = 0
    # 이미지 폴더를 순회합니다
    for filename in os.listdir(img_path):
        # 1. 파일 이름에서 확장자(.jpg)를 제거 -> 예: '2'
        base_name = os.path.splitext(filename)[0]
        # 2. 라벨 파일 이름 생성 -> 예: '2.txt'
        label_file = base_name + '.txt'
        
        # 3. 라벨 경로 완성
        full_label_path = os.path.join(lbl_path, label_file)
        
        # 4. 정말로 파일이 없는 경우에만 삭제!
        if not os.path.exists(full_label_path):
            print(f"라벨이 없어서 삭제합니다: {filename}")
            os.remove(os.path.join(img_path, filename)) # 테스트 완료 전까지 주석 유지!
            count += 1
        else:
            # 매칭이 잘 되는지 확인용 출력
            # print(f"매칭 성공: {filename} <-> {label_file}")
            pass
            
    print(f"총 {count}개의 라벨링되지 않은 이미지가 확인되었습니다.")

remove_unlabeled_images(images_dir, labels_dir)