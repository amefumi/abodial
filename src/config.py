import configparser
import string
import threading
import numpy as np
import os
from dataclasses import dataclass
from loguru import logger


class Config:
    game = {
        'path': r'C:\Program Files (x86)\Diablo II Resurrected',
        'window_process': r'D2R.exe',
    }

    bot = {
        'difficulty': 'hell',
    }

    colors = {
        'black': (0, 0, 0, 180, 255, 15),
        'gold_numbers': (0, 0, 65, 180, 255, 255),
        'item_highlight': (90, 235, 130, 115, 255, 160),
        'white': (0, 0, 230, 180, 20, 255),
        'gray': (0, 0, 90, 180, 20, 130),
        'blue': (114, 100, 165, 125, 132, 255),
        'green': (56, 190, 190, 63, 255, 255),
        'yellow': (27, 110, 190, 33, 145, 255),
        'gold': (20, 75, 140, 26, 95, 230),
        'orange': (20, 190, 190, 23, 255, 255),
        'red': (-9, 110, 100, 12, 255, 255),
        'health_potion': (170, 100, 76, 190, 255, 255),
        'mana_potion': (105, 20, 76, 135, 255, 255),
        'rejuv_potion': (140, 50, 40, 160, 255, 255),
        'skill_charges': (70, 30, 25, 150, 163, 255),
        'health_globe_red': (178, 110, 20, 183, 255, 255),
        'health_globe_green': (47, 90, 20, 54, 255, 255),
        'mana_globe': (117, 120, 20, 121, 255, 255),
        'blue_slot': (102, 194, 18, 138, 230, 54),
        'green_slot': (33, 181, 18, 87, 258, 69),
        'red_slot': (161, 204, 28, 197, 240, 64),
        'tab_text': (0, 0, 125, 180, 255, 255),
    }

    ui = {
        'window_height': 720,
        'window_width': 1280,
    }

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Config, cls).__new__(cls, *args, **kwargs)
        return cls._instance


if __name__ == '__main__':
    config = Config()
