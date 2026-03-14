def get_bbox_center(bbox):
    """
    Calculate the center point of a bounding box.
    bbox: [x1, y1, x2, y2]
    """
    x1, y1, x2, y2 = bbox
    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2
    return cx, cy

def get_bbox_area(bbox):
    """
    Calculate area of a bounding box.
    """
    x1, y1, x2, y2 = bbox
    return (x2 - x1) * (y2 - y1)
