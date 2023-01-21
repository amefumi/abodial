import keyboard
from config import Config
from human_behavior import wait


class Keyboard:
    @staticmethod
    def select_difficulty():
        if Config().bot['difficulty'] == 'normal':
            keyboard.send('r')
        elif Config().bot['difficulty'] == 'nightmare':
            keyboard.send('n')
        else:
            keyboard.send('h')

    @staticmethod
    def set_no_pick():
        keyboard.send('enter')
        wait(0.1, 0.25)
        keyboard.write('/nopickup', delay=.20)
        keyboard.send('enter')

    @staticmethod
    def set_fps():
        keyboard.send('enter')
        wait(0.1, 0.25)
        keyboard.write('/fps', delay=.20)
        keyboard.send('enter')

    @staticmethod
    def repeat_last_command():
        keyboard.send('enter')
        wait(0.1, 0.25)
        keyboard.send('up')
        wait(0.1, 0.25)
        keyboard.send('enter')
        wait(0.1, 0.25)

    @staticmethod
    def esc():
        keyboard.send('esc')
