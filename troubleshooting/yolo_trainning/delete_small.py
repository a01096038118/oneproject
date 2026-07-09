import os
import shutil
from collections import defaultdict

label_root = r'C:\Alot1team\project\troubleshooting\yolo_trainning\dataset\labels'
img_root = r'C:\Alot1team\project\troubleshooting\yolo_trainning\dataset\images'
min_size = 0.007

dry_run = False

# 원본 라벨 폴더를 통째로 백업해두고 싶으면 True (라벨 파일은 용량이 작아서 권장)
make_backup = True
backup_root = label_root + '_backup'

img_exts = ['.jpg', '.png', '.jpeg']

stats_before = defaultdict(int)
stats_after = defaultdict(int)
removed_lines = 0
removed_images = 0

if make_backup and not dry_run and not os.path.exists(backup_root):
    shutil.copytree(label_root, backup_root)
    print(f"[백업 완료] {backup_root}")

for root, dirs, files in os.walk(label_root):
    for label_file in files:
        if not label_file.endswith('.txt'):
            continue

        label_path = os.path.join(root, label_file)

        with open(label_path, 'r') as f:
            lines = f.readlines()

        kept_lines = []
        for line in lines:
            parts = line.split()
            if len(parts) < 5:
                continue

            cls_id = parts[0]
            w, h = float(parts[3]), float(parts[4])
            stats_before[cls_id] += 1

            if w < min_size or h < min_size:
                removed_lines += 1
                continue  # 이 박스(줄)만 버림

            kept_lines.append(line)
            stats_after[cls_id] += 1

        relative_path = os.path.relpath(root, label_root)
        current_img_dir = os.path.join(img_root, relative_path)

        if len(kept_lines) == 0:
            # 남은 박스가 하나도 없을 때만 이미지+라벨 삭제
            removed_images += 1
            print(f"[이미지 전체 삭제 대상] {label_file} (남은 박스 0개)")
            if not dry_run:
                os.remove(label_path)
                for ext in img_exts:
                    img_path = os.path.join(current_img_dir, label_file.replace('.txt', ext))
                    if os.path.exists(img_path):
                        os.remove(img_path)
                        break
        else:
            # 일부 박스만 걸러낸 경우: 라벨 파일만 다시 쓰기 (이미지는 유지)
            if len(kept_lines) != len(lines):
                print(f"[라인 일부 제거] {label_file}: {len(lines)} -> {len(kept_lines)}")
                if not dry_run:
                    with open(label_path, 'w') as f:
                        f.writelines(kept_lines)

print("\n===== 요약 =====")
print(f"모드: {'DRY RUN (실제 변경 없음)' if dry_run else '실제 적용됨'}")
print(f"제거된 박스(라인) 수: {removed_lines}")
print(f"완전히 삭제된 이미지 수: {removed_images}")
print("\n클래스별 박스 개수 (필터링 전 -> 후):")
for cls_id in sorted(set(list(stats_before.keys()) + list(stats_after.keys())), key=lambda x: int(x)):
    print(f"  class {cls_id}: {stats_before[cls_id]} -> {stats_after[cls_id]}")