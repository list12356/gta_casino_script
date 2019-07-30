import time
import sys
import os
import ctypes
from pynput import keyboard
from pynput.mouse import Button, Controller

MOUSE_PRIMARY = Button.left
mouse = Controller()
# Need to setup dpi awareness for windows 10!
awareness = ctypes.c_int()
errocode = ctypes.windll.shcore.SetProcessDpiAwareness(2)

def on_press(key):
    pass

def on_release_start(key):
    try:
        if key == keyboard.Key.f6:
            return False
    except:
        pass


def on_release_exit(key):
    try:
        if key == keyboard.Key.esc:
            os._exit(1)
    except:
        pass
    try:
        if key.char == 'q':
            os._exit(1) 
    except:
        pass

def click(x, y):
    mouse.position = (x, y)
    mouse.press(MOUSE_PRIMARY)
    time.sleep(0.5)
    mouse.release(MOUSE_PRIMARY)

def perform_bet():
    while(True):
        time.sleep(0.5)
        click(1400, 911)
        time.sleep(1)
        click(413, 329)
        time.sleep(1)
        for i in range(10):
            click(1526, 527)
            time.sleep(0.2)
        click(1416, 801)
        time.sleep(35)
        click(939, 1008)
        time.sleep(1)

def main():

    with keyboard.Listener(on_press=on_press, on_release=on_release_start) as listener:
        listener.join()

    stop_listener = keyboard.Listener(on_press=on_press, on_release=on_release_exit)
    stop_listener.start()
    print("start betting...")
    perform_bet()

main()
    