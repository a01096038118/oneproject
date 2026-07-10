"""
COCO(json) -> YOLO(txt) 변환 스크립트
- category_id == 0 (ignored) 는 제외
- 나머지 클래스는 0부터 연속된 인덱스로 재매핑
- train, val 각각 json/output_dir만 바꿔서 두 번 실행
"""

import json
import os

# ==================== 여기만 수정하세요 ====================
CONFIG = {
    "json_path": "C:/Alot1team/project/troubleshooting/yolo_trainning/dataset/raw/instances_val.json",
    "output_dir": "C:/Alot1team/project/troubleshooting/yolo_trainning/dataset/labels/val",
}
# ==========================================================

# 제외할 카테고리 id (ignored)
# 실제 annotation 데이터와 대조 검증한 결과, categories 필드에 적힌 그대로가 맞음:
# category_id 0 = ignored (이 데이터셋 파일에는 실제로 0건 존재)
# category_id 1 = swimmer (사람 크기 박스로 직접 확인됨 - 절대 제외하면 안 됨)
IGNORE_CATEGORY_ID = 0


def convert(json_path: str, output_dir: str):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1) categories 필드는 실제 데이터와 어긋나 있을 수 있으므로,
    #    annotations에 "실제로 등장하는" category_id만 기준으로 재매핑한다.
    actual_ids = sorted({ann["category_id"] for ann in data["annotations"]})
    print(f"annotations에 실제로 존재하는 category_id 목록: {actual_ids}")

    id_map = {}
    new_idx = 0
    for cid in actual_ids:
        if cid == IGNORE_CATEGORY_ID:
            continue
        id_map[cid] = new_idx
        new_idx += 1

    print(f"제외 처리된 category_id: {IGNORE_CATEGORY_ID} (categories 필드 이름표가 아닌, "
          f"실제 annotation 개수 확인 결과를 기준으로 지정된 값입니다)")
    print("클래스 매핑 (원본 category_id -> YOLO class index):")
    name_by_id = {c["id"]: c["name"] for c in data["categories"]}
    for old_id, new_id in id_map.items():
        # 실제 데이터 기준으로는 categories 필드 이름과 1칸씩 밀려있을 수 있으니 참고용으로만 출력
        print(f"  {old_id} (categories 필드상 이름: {name_by_id.get(old_id, '?')}) -> {new_id}")

    # 2) image_id -> 이미지 정보 매핑
    images = {img["id"]: img for img in data["images"]}

    # 3) image_id 별로 annotation 모으기 (ignored 제외)
    anns_by_image = {img_id: [] for img_id in images}
    skipped_ignored = 0
    for ann in data["annotations"]:
        if ann["category_id"] == IGNORE_CATEGORY_ID:
            skipped_ignored += 1
            continue
        anns_by_image[ann["image_id"]].append(ann)

    print(f"\n제외된 ignored annotation 수: {skipped_ignored}")

    # 4) 출력 폴더 생성
    os.makedirs(output_dir, exist_ok=True)

    # 5) 이미지 전체에 대해 txt 생성 (객체 없는 이미지는 빈 txt = 배경 이미지)
    written = 0
    for img_id, img in images.items():
        w, h = img["width"], img["height"]
        lines = []
        for ann in anns_by_image[img_id]:
            x, y, bw, bh = ann["bbox"]  # COCO: top-left x, y, width, height
            cx = (x + bw / 2) / w
            cy = (y + bh / 2) / h
            nw = bw / w
            nh = bh / h
            cls = id_map[ann["category_id"]]
            lines.append(f"{cls} {cx:.6f} {cy:.6f} {nw:.6f} {nh:.6f}")

        base_name = os.path.splitext(img["file_name"])[0]
        out_path = os.path.join(output_dir, base_name + ".txt")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        written += 1

    print(f"\n총 {written}개의 txt 라벨 파일 생성 완료 -> {output_dir}")


if __name__ == "__main__":
    convert(CONFIG["json_path"], CONFIG["output_dir"])
