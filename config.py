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
