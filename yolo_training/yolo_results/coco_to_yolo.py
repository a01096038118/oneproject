import json
import os
import sys


BASE = "C:/Alot1team/project/troubleshooting/yolo_trainning/dataset"

SPLITS = {
    "train": {
        "json_path": f"{BASE}/raw/instances_train.json",
        "output_dir": f"{BASE}/labels/train",
    },
    "val": {
        "json_path": f"{BASE}/raw/instances_val.json",
        "output_dir": f"{BASE}/labels/val",
    },
}

# 제외할 카테고리 id (ignored)
IGNORE_CATEGORY_IDS = {0}


def build_id_map(categories):
    """categories 정의 기준으로 YOLO class index 매핑 생성 (ignored 제외)"""
    id_map = {}
    new_idx = 0
    for cat in sorted(categories, key=lambda c: c["id"]):
        if cat["id"] in IGNORE_CATEGORY_IDS:
            continue
        id_map[cat["id"]] = new_idx
        new_idx += 1
    return id_map


def convert(split_name, json_path, output_dir, expected_id_map=None):
    print(f"\n{'=' * 50}")
    print(f"[{split_name}] {json_path}")
    print(f"{'=' * 50}")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1) 클래스 매핑 (categories 정의 기준)
    id_map = build_id_map(data["categories"])
    name_by_id = {c["id"]: c["name"] for c in data["categories"]}

    print("클래스 매핑 (원본 category_id -> YOLO class index):")
    for old_id, new_id in id_map.items():
        print(f"  {old_id} ({name_by_id[old_id]}) -> {new_id}")

    # 스플릿 간 매핑 일치 검증 (all 모드에서 자동 수행)
    if expected_id_map is not None and id_map != expected_id_map:
        raise ValueError(
            f"[{split_name}] 클래스 매핑이 train과 다릅니다! "
            f"json의 categories 정의가 스플릿마다 다른지 확인하세요.\n"
            f"  train: {expected_id_map}\n  {split_name}: {id_map}"
        )

    # 2) image_id -> 이미지 정보 매핑
    images = {img["id"]: img for img in data["images"]}

    # 3) image_id 별로 annotation 모으기 (ignored 제외)
    anns_by_image = {img_id: [] for img_id in images}
    skipped_ignored = 0
    skipped_unknown = 0
    for ann in data["annotations"]:
        cid = ann["category_id"]
        if cid in IGNORE_CATEGORY_IDS:
            skipped_ignored += 1
            continue
        if cid not in id_map:
            # categories에 정의되지 않은 id가 annotation에 등장한 경우 (비정상 데이터)
            skipped_unknown += 1
            continue
        anns_by_image[ann["image_id"]].append(ann)

    print(f"제외된 ignored annotation 수: {skipped_ignored}")
    if skipped_unknown:
        print(f"[경고] categories에 정의되지 않은 category_id를 가진 "
              f"annotation {skipped_unknown}개를 건너뜀 — 데이터 확인 필요!")

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

    print(f"총 {written}개의 txt 라벨 파일 생성 완료 -> {output_dir}")
    return id_map


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("train", "val", "all"):
        print("사용법: python coco_to_yolo.py [train | val | all]")
        sys.exit(1)

    target = sys.argv[1]

    if target == "all":
        # train을 기준 매핑으로 삼고, val이 일치하는지 자동 검증
        train_map = convert("train", **SPLITS["train"])
        convert("val", **SPLITS["val"], expected_id_map=train_map)
        print("\n[OK] train/val 클래스 매핑 일치 확인 완료")
    else:
        convert(target, **SPLITS[target])


if __name__ == "__main__":
    main()
