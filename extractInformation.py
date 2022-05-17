import cv2
import numpy as np
import math


def information(image):
    (contours, hierarchy) = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    ergebnisse = []
    for cnt in contours:
        if cv2.contourArea(cnt)>0:
            ergebnisse.append({
                'area': cv2.contourArea(cnt),
                'rand': cv2.arcLength(cnt, True)})

    if len(ergebnisse)>0:

        MdQ = sum(map(lambda erg: erg['rand']*erg['rand'] /
                erg['area']/4/math.pi, ergebnisse))/len(ergebnisse)
        
        #if sum(list(map(lambda x: x["area"],ergebnisse)))>12000000:
        #    print("Area over 12 Mio")
        return len(ergebnisse),list(map(lambda x: x["area"],ergebnisse)),MdQ
        
    return 0,[],1001

def getVolume(flaeche, reduced_phi):
    r = math.sqrt(flaeche/math.pi)
    return math.pow(r, 3)*math.pi*reduced_phi

def calcVolume(flaechen, kontaktwinkel):
    kontaktwinkel = float(kontaktwinkel)*math.pi/180
    cos = math.cos(kontaktwinkel)
    sin = math.sin(kontaktwinkel)
    reduced_phi = (2. - 3. * cos + math.pow(cos, 3.)) / \
        (3. * math.pow(sin, 3.))
    return sum(list(map(lambda x: getVolume(x, reduced_phi), flaechen)))