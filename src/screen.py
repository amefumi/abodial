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
from copy import deepcopy
from config import Config


class Screen:
    """
    Screen class is used to obtain the position of the game window and provide a fast screen capture interface.
    Note that Screen is singleton and can only be used after the game has been run.
    """
    _instance = None

    game_hwnd = None
    monitor = {
        "left": None,
        "top": None,
        "width": Config.ui['window_width'],
        "height": Config.ui['window_height'],
    }

    sct = mss()
    rt_image = None
    rt_image_lock = threading.Lock()
    rt_grab_time = 0

    find_window_thread = None
    find_window_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Screen, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def start(self):
        self._find_d2r_window()
        if self.find_window_thread is None:
            self.find_window_thread = threading.Thread(target=self.find_d2r_window, daemon=True)
        if not self.find_window_thread.is_alive():
            self.find_window_thread.start()

    def stop(self):
        if self.find_window_thread is not None:
            self.find_window_thread.join()
            self.game_hwnd = None
            self.rt_image = None

    def _find_d2r_window(self):
        if not self.game_hwnd:
            window_list = []
            EnumWindows(lambda w, l: l.append(w), window_list)
            for hwnd in window_list:
                _, process_id = GetWindowThreadProcessId(hwnd)
                if process_id > 0 and Config.game['window_process'] in psutil.Process(process_id).name():
                    self.game_hwnd = hwnd
                    break
        if self.game_hwnd:
            try:
                left, top, _, _ = GetClientRect(self.game_hwnd)
                with self.find_window_lock:
                    self.monitor["left"], self.monitor["top"] = ClientToScreen(self.game_hwnd, (left, top))
            except BaseException:
                self.game_hwnd = None
        else:
            logger.debug("Game not found.")

    def find_d2r_window(self):
        while True:
            self._find_d2r_window()
            time.sleep(1)

    def grab(self, require_new: bool = False):
        """
        Create screenshots that contain only the contents of the game window. If the time of two screenshots is
        less than 40ms, the last cached screenshot will be returned (because the actual in-game operation frame
        rate is 25FPS).
        :param require_new: bool. If it is true, a new screenshot is forced to be returned.
        :return: Screenshots that contain only the contents of the game window.
        """
        c = time.perf_counter()
        if require_new or time.perf_counter() - self.rt_grab_time > 0.04 or self.rt_image is None:
            with self.find_window_lock:
                image = np.asarray(self.sct.grab(self.monitor))
            with self.rt_image_lock:
                self.rt_image = image[:, :, :3]
        print(time.perf_counter() - c)
        return self.rt_image


if __name__ == '__main__':
    a = Screen()
    a.start()
    while True:
        cv2.imshow("A", a.grab())
        cv2.waitKey(0)