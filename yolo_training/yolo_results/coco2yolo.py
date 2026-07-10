import json
import os

# 각 데이터셋에 대한 경로 설정
datasets = [
    {
        "json_path": "C:/Alot1team/project/troubleshooting/yolo_trainning/dataset/raw/instances_train.json",
        "output_dir": "dataset/labels/train"
    },
    {
        "json_path": "C:/Alot1team/project/troubleshooting/yolo_trainning/dataset/raw/instances_val.json",
        "output_dir": "dataset/labels/val"
    }
]

def convert(json_file_path, output_txt_dir):
    os.makedirs(output_txt_dir, exist_ok=True)

    print(f"⏳ '{os.path.basename(json_file_path)}' 파일을 읽는 중입니다...")
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ 에러: '{json_file_path}' 파일을 찾을 수 없습니다.")
        return

    images_info = {img['id']: img for img in data['images']}

    print(f"✅ 총 {len(images_info)}장의 이미지 정보 확인. 변환을 시작합니다!")

    # 딕셔너리를 사용하여 각 이미지별로 라벨 데이터를 관리 (중복 쓰기 방지)
    img_annotations = {}

    for ann in data['annotations']:
        cat_id = ann['category_id']
        
        if cat_id == 0:
            continue
            
      
        real_cat_id = cat_id - 1
        
        img_id = ann['image_id']
        x_min, y_min, w, h = ann['bbox']

        img_info = images_info[img_id]
        img_w, img_h = img_info['width'], img_info['height']

        # YOLO 형식으로 변환
        x_center = (x_min + (w / 2.0)) / img_w
        y_center = (y_min + (h / 2.0)) / img_h
        w /= img_w
        h /= img_h

        base_name = os.path.splitext(img_info['file_name'])[0]
        
        if base_name not in img_annotations:
            img_annotations[base_name] = []
        img_annotations[base_name].append(f"{real_cat_id} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}")

    # 파일에 기록
    count = 0
    for base_name, lines in img_annotations.items():
        txt_filepath = os.path.join(output_txt_dir, f"{base_name}.txt")
        with open(txt_filepath, 'w', encoding='utf-8') as txt_file:
            txt_file.write("\n".join(lines) + "\n")
        count += len(lines)
    
    print(f"🎉 변환 완료! 총 {count}개의 객체가 '{output_txt_dir}'에 저장되었습니다.\n")

if __name__ == "__main__":
    for ds in datasets:
        convert(ds["json_path"], ds["output_dir"])