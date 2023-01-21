import cv2
import threading
from screen import Screen
from dataclasses import dataclass
import numpy as np
from loguru import logger
import time
import os
from config import Config
from functools import cache
from copy import deepcopy

from utils import list_files_in_folder, cut_roi, roi_center, mask_by_roi

templates_lock = threading.Lock()

TEMPLATE_PATHS = [
    "data\\templates",
    "data\\npc",
    "data\\shop",
    "data\\item_properties",
    "data\\chests",
    "data\\gamble",
]


@dataclass
class Template:
    name: str = None
    img_bgra: np.ndarray = None
    img_bgr: np.ndarray = None
    img_gray: np.ndarray = None
    alpha_mask: np.ndarray = None


@dataclass
class TemplateMatch:
    name: str = None
    score: float = -1.0
    center: tuple[int, int] = None
    center_monitor: tuple[int, int] = None
    region: list[float] = None
    region_monitor: list[float] = None
    valid: bool = False


def load_template(path):
    if os.path.isfile(path):
        try:
            template_img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
            return template_img
        except Exception as e:
            print(e)
            raise ValueError(f"Could not load template: {path}")
    else:
        logger.error(f"Template does not exist: {path}")
    return None


def alpha_to_mask(img: np.ndarray):
    # create a mask from template where alpha == 0
    if img.shape[2] == 4:
        if np.min(img[:, :, 3]) == 0:
            _, mask = cv2.threshold(img[:, :, 3], 1, 255, cv2.THRESH_BINARY)
            return mask
    return None


def color_filter(img, color_range):
    color_ranges = []
    # ex: [array([ -9, 201,  25]), array([ 9, 237,  61])]
    if color_range[0][0] < 0:
        lower_range = deepcopy(color_range)
        lower_range[0][0] = 0
        color_ranges.append(lower_range)
        upper_range = deepcopy(color_range)
        upper_range[0][0] = 180 + color_range[0][0]
        upper_range[1][0] = 180
        color_ranges.append(upper_range)
    # ex: [array([ 170, 201,  25]), array([ 188, 237,  61])]
    elif color_range[1][0] > 180:
        upper_range = deepcopy(color_range)
        upper_range[1][0] = 180
        color_ranges.append(upper_range)
        lower_range = deepcopy(color_range)
        lower_range[0][0] = 0
        lower_range[1][0] = color_range[1][0] - 180
        color_ranges.append(lower_range)
    else:
        color_ranges.append(color_range)
    color_masks = []
    for color_range in color_ranges:
        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_img, color_range[0], color_range[1])
        color_masks.append(mask)
    color_mask = np.bitwise_or.reduce(color_masks) if len(color_masks) > 0 else color_masks[0]
    filtered_img = cv2.bitwise_and(img, img, mask=color_mask)
    return color_mask, filtered_img


@cache
def stored_templates():
    paths = []
    templates = {}
    for path in TEMPLATE_PATHS:
        paths += list_files_in_folder(path)
    for file_path in paths:
        file_name: str = os.path.basename(file_path)
        if file_name.lower().endswith('.png'):
            key = file_name[:-4].upper()
            template_img = load_template(file_path)
            templates[key] = Template(
                name=key,
                img_bgra=template_img,
                img_bgr=cv2.cvtColor(template_img, cv2.COLOR_BGRA2BGR),
                img_gray=cv2.cvtColor(template_img, cv2.COLOR_BGRA2GRAY),
                alpha_mask=alpha_to_mask(template_img)
            )
    return templates


def get_template(key):
    with templates_lock:
        return stored_templates()[key].img_bgr


def _process_template_refs(name: str | np.ndarray | list[str]) -> list[Template]:
    templates = []
    if type(name) != list:
        name = [name]
    for i in name:
        # if the reference is a string, then it's a reference to a named template asset
        if type(i) == str:
            templates.append(stored_templates()[i.upper()])
        # if the reference is an image, append new Template class object
        elif type(i) == np.ndarray:
            templates.append(Template(
                img_bgr=i,
                img_gray=cv2.cvtColor(i, cv2.COLOR_BGR2GRAY),
                alpha_mask=alpha_to_mask(i)
            ))
    return templates


def _single_template_match(template: Template, inp_img: np.ndarray = None, roi: list = None, color_match: list = None, use_grayscale: bool = False) -> TemplateMatch:
    inp_img = inp_img if inp_img is not None else Screen().grab()
    template_match = TemplateMatch()

    # crop image to roi
    if roi is None:
        # if no roi is provided roi = full inp_img
        roi = [0, 0, inp_img.shape[1], inp_img.shape[0]]
    rx, ry, rw, rh = roi
    img = inp_img[ry:ry + rh, rx:rx + rw]

    # filter for desired color or make grayscale
    if color_match:
        template_img,  = color_filter(template.img_bgr, color_match)[1],
        img = color_filter(img, color_match)[1]
    elif use_grayscale:
        template_img = template.img_gray
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        template_img = template.img_bgr

    if not (img.shape[0] > template_img.shape[0] and img.shape[1] > template_img.shape[1]):
        logger.error(f"Image shape and template shape are incompatible: {template.name}. Image: {img.shape}, Template: {template_img.shape}, roi: {roi}")
    else:
        res = cv2.matchTemplate(img, template_img, cv2.TM_CCOEFF_NORMED, mask = template.alpha_mask)
        np.nan_to_num(res, copy=False, nan=0.0, posinf=0.0, neginf=0.0)
        _, max_val, _, max_pos = cv2.minMaxLoc(res)

        # save rectangle corresponding to matched region
        rec_x = int((max_pos[0] + rx))
        rec_y = int((max_pos[1] + ry))
        rec_w = int(template_img.shape[1])
        rec_h = int(template_img.shape[0])
        template_match.region = [rec_x, rec_y, rec_w, rec_h]
        template_match.region_monitor = [*convert_screen_to_monitor((rec_x, rec_y)), rec_w, rec_h]
        template_match.center = roi_center(template_match.region)
        template_match.center_monitor = convert_screen_to_monitor(template_match.center)
        template_match.name = template.name
        template_match.score = max_val
        template_match.valid = True

    return template_match

