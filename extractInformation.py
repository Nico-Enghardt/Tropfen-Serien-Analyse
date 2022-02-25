import cv2
import numpy as np
import math


def information(image):
    (contours, hierarchy) = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    ergebnisse = []

    # Need to add new option for segmentet areas

    for cnt in contours:
        if cv2.contourArea(cnt)>0:
            ergebnisse.append({
                'area': cv2.contourArea(cnt),
                'rand': cv2.arcLength(cnt, True)})

    if len(ergebnisse)>0:

        MdQ = sum(map(lambda erg: erg['rand']*erg['rand'] /
                erg['area']/4/math.pi, ergebnisse))/len(ergebnisse)
        
        if sum(list(map(lambda x: x["area"],ergebnisse)))>12000000:
            print("Area over 12 Mio")
        return len(ergebnisse),list(map(lambda x: x["area"],ergebnisse)),MdQ
        
    return 0,[],1001
