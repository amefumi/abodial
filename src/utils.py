import os
import numpy as np
import cv2


def cut_roi(img, roi):
    x, y, w, h = roi
    return img[y:y + h, x:x + w]


def roi_center(roi: list[float] = None):
    x, y, w, h = roi
    return round(x + w / 2), round(y + h / 2)


def mask_by_roi(img, roi, op: str = "regular"):
    x, y, w, h = roi
    if op == "regular":
        masked = np.zeros(img.shape, dtype=np.uint8)
        masked[y:y + h, x:x + w] = img[y:y + h, x:x + w]
    elif op == "inverse":
        masked = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), -1)
    else:
        return None
    return masked


def list_files_in_folder(path: str):
    r = []
    for root, _, files in os.walk(path):
        for name in files:
            r.append(os.path.join(root, name))
    return r
