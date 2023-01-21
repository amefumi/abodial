import os
import time
import random


def curve():
    pass


def wait(lower, higher=None):
    if higher is None:
        higher = lower
    time.sleep(random.uniform(lower, higher))
