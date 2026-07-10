import cv2
from dashboard import config

def draw_danger_zones(frame, detected_zones):
    for zone in config.DANGER_ZONES:

        zone_color = config.DANGER_ZONE_NORMAL_COLOR

        if zone["zone_id"] in detected_zones:
            zone_color = config.DANGER_ZONE_DETECTED_COLOR

        cv2.rectangle(
            frame,
            (zone["x1"], zone["y1"]),
            (zone["x2"], zone["y2"]),
            zone_color,
            config.DANGER_ZONE_BOX_THICKNESS
        )

        cv2.putText(
            frame,
            zone["zone_id"],
            (zone["x1"], zone["y1"] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            zone_color,
            config.TEXT_THICKNESS
        )

def draw_detected_objects(frame, detected_people):

    for detected_object in detected_people:

        cv2.rectangle(
            frame,
            (detected_object["x1"], detected_object["y1"]),
            (detected_object["x2"], detected_object["y2"]),
            config.OBJECT_BOX_COLOR,
            config.OBJECT_BOX_THICKNESS
        )

        cv2.putText(
            frame,
            f'{detected_object["class_name"]} {detected_object["confidence"]:.2f}',
            (detected_object["x1"], detected_object["y1"] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            config.OBJECT_BOX_COLOR,
            config.TEXT_THICKNESS
        )

        cv2.circle(
            frame,
            (detected_object["center_x"], detected_object["center_y"]),
            config.CENTER_POINT_RADIUS,
            config.CENTER_POINT_COLOR,
            -1
        )

def draw_intrusion_alert(frame):
    cv2.putText(
        frame,
        config.INTRUSION_ALERT_TEXT,
        config.INTRUSION_TEXT_POSITION,
        cv2.FONT_HERSHEY_SIMPLEX,
        config.INTRUSION_TEXT_SCALE,
        config.INTRUSION_TEXT_COLOR,
        config.INTRUSION_TEXT_THICKNESS
    )