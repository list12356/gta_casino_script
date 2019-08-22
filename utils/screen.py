import ctypes
from win32api import GetSystemMetrics


# Need to setup dpi awareness for windows 10!
errocode = ctypes.windll.shcore.SetProcessDpiAwareness(2)
RES_WIDTH = GetSystemMetrics(0)
RES_HEIGHT = GetSystemMetrics(1)
SCALE_RATIO_W = RES_WIDTH/1920
SCALE_RATIO_H = RES_HEIGHT/1080

POS_START = (1400*SCALE_RATIO_W, 911*SCALE_RATIO_H)
POS_CANCEL = (1273*SCALE_RATIO_W, 995*SCALE_RATIO_H)
POS_HORSE1 = (413*SCALE_RATIO_W, 329*SCALE_RATIO_H)
POS_INC_BET = (1526*SCALE_RATIO_W, 520*SCALE_RATIO_H)
POS_PLACE_BET = (1416*SCALE_RATIO_W, 801*SCALE_RATIO_H)

# x y w h
ODDS_BOUNDING_BOX = [
    [175, 370, 65, 40],
    [175, 485, 65, 40],
    [175, 605, 65, 40],
    [175, 720, 65, 40],
    [175, 840, 65, 40],
    [175, 960, 65, 40],
]