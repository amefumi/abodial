import time
import threading
from win32gui import EnumWindows, GetClientRect, ClientToScreen
from win32process import GetWindowThreadProcessId
import os
import psutil
from loguru import logger
from mss import mss
import numpy as np
import cv2
from config import Config


class Screen:
    game_hwnd = None
    left = None
    top = None
    height = Config.ui['window_height']
    width = Config.ui['window_width']

    sct = mss()
    monitor_roi = sct.monitors[0]
    cached_image = None
    cached_image_lock = threading.Lock()
    last_grab = None
    last_grab_time = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Screen, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def find_d2r_window(self):
        window_list = []
        EnumWindows(lambda w, l: l.append(w), window_list)
        for hwnd in window_list:
            _, process_id = GetWindowThreadProcessId(hwnd)
            if process_id > 0 and Config.game['window_process'] in psutil.Process(process_id).name():
                self.game_hwnd = hwnd
                break
        if self.game_hwnd:
            left, top, _, _ = GetClientRect(self.game_hwnd)
            self.left, self.top = ClientToScreen(self.game_hwnd, (left, top))
            logger.debug(f"Game found. HWND = {self.game_hwnd}.")
            logger.debug(f"Game Offset = (left {self.left}, top {self.top}).")
        else:
            logger.debug("Game not found.")

    def grab(self, force_new: bool = False):
        if force_new or self.cached_image is None or self.last_grab_time is None or time.perf_counter() - self.last_grab_time > 0.04:
            with self.cached_image_lock:
                self.last_grab_time = time.perf_counter()
            image = np.array(self.sct.grab(self.monitor_roi))
            with self.cached_image_lock:
                self.cached_image = image[self.top: self.top + self.height, self.left: self.left + self.width, :3]
        return self.cached_image

if __name__ == '__main__':
    a = Screen()
    a.find_d2r_window()
    cv2.imshow("A", a.grab())
    cv2.waitKey(0)
