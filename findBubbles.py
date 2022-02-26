import cv2
import numpy as np
#from parameters import parameters
#from segmentation import *

def deleteDenoised():
    global denoised
    denoised = []

def extractLights(image, limit, glow):
    red, white_dots = cv2.threshold(image, limit, 255, cv2.THRESH_BINARY)
    white_dots = dilate(white_dots, glow)
    #white_dots = cv2.cvtColor(white_dots,cv2.COLOR_BGR2GRAY)
    return white_dots

def extractDarks(image, limit):
    red, not_black_bubbles = cv2.threshold(
        image, limit, 255, cv2.THRESH_BINARY)

    black_bubbles = cv2.bitwise_not(not_black_bubbles)
    #black_bubbles = cv2.cvtColor(black_bubbles,cv2.COLOR_BGR2GRAY)
    return black_bubbles

def fillHoles(binary):

    if len(binary.shape) > 2:
        binary = cv2.cvtColor(binary, cv2.COLOR_BGR2GRAY)

    contours,hierarchy  = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    filled = cv2.drawContours(binary, contours, -1, (255), -1)
    
    return filled

def dilate(binary, strength):
    return cv2.dilate(binary, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (strength, strength)), iterations=1)

def removeNoise(binary, strength):
    return cv2.morphologyEx(binary, cv2.MORPH_OPEN, np.ones((strength, strength),dtype=np.uint8))

def fillGaps(binary, strength):
    return cv2.morphologyEx(binary, cv2.MORPH_CLOSE, np.ones((strength, strength),dtype=np.uint8))

def getDenoised(raw,blurvalue):

    denoised =  cv2.fastNlMeansDenoising(raw, 6, blurvalue, 15)
    return denoised

def balanceLight(input):
    light_map = cv2.GaussianBlur(input,(1001,1001),400)
    light_map = light_map.astype(np.double)   
    input = input.astype(np.double)
    input = cv2.divide(input,light_map)
    min = np.amin(input)
    max = np.amax(input)
    input = input - min
    max = np.amax(input)
    input = input * 255/max
    input = input.astype(np.uint8)
    return input

def findBubbles(input, params,denoised=[]):
    
    #input = balanceLight(input)

    if denoised==[]:
        denoised = getDenoised(input,40)

    lights = extractLights(input, params['upper_limit'], params['glow'])


    # Auto-Detect dark parameter --------------------------
    darks = extractDarks(denoised, params['lower_limit'])

    mix = cv2.bitwise_or(lights, darks)

    mix = fillGaps(mix, params['gapsfill'])
    mix = removeNoise(mix, params['siebsize'])

    #mix = fillHoles(mix)

    return mix # Will be more colourful after segmentation