import os
import shutil
import json



source_image_folder = "./all_images" 

target_image_folder = "./data/images/train"

json_file_path = "data/raw/instances_train.json"


def organize():
    # 폴더 생성
    os.makedirs(target_image_folder, exist_ok=True)
    
    print("⏳ 데이터셋에서 이미지 목록을 읽는 중...")
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    # 필요한 파일명 목록 추출
    required_files = {img['file_name'] for img in data['images']}
    
    print(f"총 {len(required_files)}장의 이미지를 찾습니다.")
    
    count = 0
    for file_name in required_files:
        src_path = os.path.join(source_image_folder, file_name)
        dst_path = os.path.join(target_image_folder, file_name)
        
        if os.path.exists(src_path):
            shutil.copy2(src_path, dst_path) # 파일 복사
            count += 1
            if count % 100 == 0:
                print(f"📦 {count}장 이동 중...")
        else:
            print(f"경고: '{file_name}' 파일을 찾을 수 없습니다.")

    print(f"완료! 총 {count}장의 이미지를 {target_image_folder}로 복사했습니다.")

if __name__ == "__main__":
    organize()