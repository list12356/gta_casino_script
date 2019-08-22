import time
import sys
import os

from pynput import keyboard
from pynput.mouse import Button, Controller
from utils.image import get_odds_list
from utils.prob import calc_return
from utils.screen import POS_HORSE1, POS_INC_BET, POS_PLACE_BET, POS_START, POS_CANCEL

# TODO: use config file
MOUSE_PRIMARY = Button.right
MOUSE_SECONDARY = Button.left
mouse = Controller()
VERBOSE = True
DEBUG = True

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

def click_secondary():
    mouse.press(MOUSE_SECONDARY)
    time.sleep(0.5)
    mouse.release(MOUSE_SECONDARY)

def perform_bet():
    # Not a graceful way to import, just need to match the actual resolution of the game
    
    while(True):
        time.sleep(0.5)
        click(*POS_START)
        time.sleep(1)
        # judge the return
        odds = get_odds_list()
        reward = calc_return(odds)
        if VERBOSE:
            print("Round info:")
            print("odds: {!s}".format(','.join([str(x) for x in odds])))
            print("reward: {!s}".format(reward))
        if reward < 1.2 or DEBUG:
            if VERBOSE:
                print("low reward/debugging, skipping......")
            if DEBUG:
                time.sleep(5)
            click(*POS_CANCEL)
            time.sleep(0.5)
            click_secondary()
            time.sleep(0.5)
            click(*POS_START)
            continue

        click(*POS_HORSE1)
        time.sleep(1)
        for i in range(15):
            click(*POS_INC_BET)
            time.sleep(0.2)
        click(*POS_PLACE_BET)
        time.sleep(35)
        click_secondary()
        time.sleep(1)

def main():

    with keyboard.Listener(on_press=on_press, on_release=on_release_start) as listener:
        listener.join()

    stop_listener = keyboard.Listener(on_press=on_press, on_release=on_release_exit)
    stop_listener.start()
    print("start betting...")
    perform_bet()

main()
    