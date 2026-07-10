import os

def update_labels():
    target_dirs = [
        r'C:\Alot1team\project\troubleshooting\yolo_trainning\dataset\labels\train',
        r'C:\Alot1team\project\troubleshooting\yolo_trainning\dataset\labels\val'
    ]

    # 현재 data.yaml 기준 클래스 번호
    # 0: swimmer                 -> 0
    # 1: boat                    -> 1
    # 2: jetski                  -> 2
    # 3: life_saving_appliances  -> 제외 (None)
    # 4: buoy                    -> 3
    mapping = {0: 0, 1: 1, 2: 2, 3: None, 4: 3}

    for label_dir in target_dirs:
        if not os.path.exists(label_dir):
            print(f"⚠️ 폴더를 찾을 수 없습니다: {label_dir}")
            continue

        files = [f for f in os.listdir(label_dir) if f.endswith('.txt')]
        print(f"⏳ '{label_dir}' 폴더 내 {len(files)}개의 라벨 파일을 수정합니다...")

        for filename in files:
            file_path = os.path.join(label_dir, filename)
            new_lines = []

            with open(file_path, 'r') as f:
                lines = f.readlines()

            for line in lines:
                parts = line.split()
                if not parts: continue
                old_class_id = int(parts[0])

                # 구명장비(3)는 제외하고, 나머지는 매핑된 번호로 저장
                if old_class_id in mapping and mapping[old_class_id] is not None:
                    new_class_id = mapping[old_class_id]
                    new_line = f"{new_class_id} " + " ".join(parts[1:])
                    new_lines.append(new_line)

            with open(file_path, 'w') as f:
                f.write("\n".join(new_lines) + "\n")

    print("🎉 모든 학습(train) 및 검증(val) 라벨에서 life_saving_appliances 제외 및 번호 수정이 완료되었습니다!")

if __name__ == "__main__":
    update_labels()
