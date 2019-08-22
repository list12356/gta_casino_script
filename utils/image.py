
import os
import cv2
import numpy as np
from PIL import ImageGrab

from utils.screen import ODDS_BOUNDING_BOX

TEMPLATE_NUMBERS = {}
for filename in os.listdir("./img/templates/"):
    number = filename.split('.')[0]
    img = cv2.imread("./img/templates/" + filename, 0)
    TEMPLATE_NUMBERS[number] = img


def get_odds_list(img=None):
    if img is None:
        img = np.array(ImageGrab.grab())
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    odds = []
    for y, x, h, w in ODDS_BOUNDING_BOX:
        cropped_img = img[x:x+w, y:y+h]
        result  = get_number(cropped_img)
        if 'e' in result:
            num = 1
        else:
            try: 
                num = int(''.join(result[:-2]))
            except:
                continue
        odds.append(num)
        
    return odds

def get_number(img):
    threshold = 0.9
    result_dict = {}
    for key, template in TEMPLATE_NUMBERS.items():
        corr = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(corr >= threshold)
        if not np.any(corr >= threshold):
            continue
        last_x = -10
        for pt in zip(*loc[::-1]):
            # avoid overlapping detection
            if pt[0] - last_x > 10:
                result_dict[pt[0]] = key
            last_x = pt[0]
    
    result = [result_dict[x] for x in sorted(result_dict.keys())]
    return result