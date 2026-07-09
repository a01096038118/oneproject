def is_object_in_zone(center_x, center_y, zone):
    return (
        zone["x1"] <= center_x <= zone["x2"]
        and
        zone["y1"] <= center_y <= zone["y2"]
    )