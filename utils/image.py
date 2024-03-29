
import os
import cv2
import numpy as np
import imutils
import torch

from imutils import contours
from PIL import ImageGrab

from model.model import TwoLayerNet
from utils.screen import ODDS_BOUNDING_BOX

TEMPLATE_NUMBERS = {}
for filename in os.listdir("./img/templates/"):
    number = filename.split('.')[0]
    img = cv2.imread("./img/templates/" + filename, 0)
    TEMPLATE_NUMBERS[number] = img

DEBUG_NUM = 0

model = TwoLayerNet()
model.load_state_dict(torch.load("./saved_model"))

def get_odds_list(img=None):
    if img is None:
        img = np.array(ImageGrab.grab())
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    odds = []
    for x, y, w, h in ODDS_BOUNDING_BOX:
        cropped_img = img[y:y+h, x:x+w]
        result  = get_number(cropped_img)
        try: 
            num = int(''.join(result))
        except:
            continue
        odds.append(num)
    return odds



def get_number(img):
    global DEBUG_NUM
    threshold = 0.9

    img2 = img.copy()
    img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)

    # if evens
    corr = cv2.matchTemplate(img, TEMPLATE_NUMBERS["e"], cv2.TM_CCOEFF_NORMED)
    if np.max(corr) > 0.9:
        return ['1']
    # cut at the slash symbol
    corr = cv2.matchTemplate(img, TEMPLATE_NUMBERS["slash"], cv2.TM_CCOEFF_NORMED)
    _, seg_x = np.unravel_index(np.argmax(corr), corr.shape)
    img = img[:, :seg_x + 1]
    group = cv2.threshold(img, 0, 255,
        cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
 
    # detect the contours of each individual digit in the group,
    # then sort the digit contours from left to right
    digitCnts = cv2.findContours(group.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    digitCnts = imutils.grab_contours(digitCnts)
    digitCnts = contours.sort_contours(digitCnts,
        method="left-to-right")[0]
    groupOutput = []
    for c in digitCnts:
        # compute the bounding box of the individual digit, extract
        # the digit, and resize it to have the same fixed size as
        # the reference OCR-A images
        (x, y, w, h) = cv2.boundingRect(c)
        roi = img[y:y + h, x:x + w]
        # cv2.imwrite('{!s}.png'.format(DEBUG_NUM), roi)
        # DEBUG_NUM += 1
        cv2.rectangle(img2, (x, y), (x + w, y + h), (0,0,255), 2)
 
        # initialize a list of template matching scores
        roi = cv2.resize(roi, (14, 28))    
        outputs = model(torch.FloatTensor(roi).unsqueeze(0))
        _, predicted = torch.max(outputs, 1)

        groupOutput.append(str(int(predicted.data[0])))
    # cv2.imwrite('{!s}.png'.format(DEBUG_NUM), img2)
    # DEBUG_NUM += 1
    return groupOutput