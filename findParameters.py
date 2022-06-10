import cv2
from findBubbles import *
from extractInformation import *

def findDark(gray):
    numbers = []
    mins = []
    for ll in range(0,255):
        darkImg = extractDarks(gray,ll)
        numbers.append(information(darkImg)[0])


    for x in range(1,254):
        #First Version:
        if numbers[x] + 3 < numbers[x-1] and numbers[x] + 3< numbers[x+1] :
            mins.append(x)

        # Einfluss weiter entfernter Werte mit einbeziehen

    if len(mins) == 0:
        return 0,numbers
    return mins[0],numbers

def findDarkDerivative(gray):
    
    numbers = []
    mins = []
    for ll in range(0,255):
        darkImg = extractDarks(gray,ll)
        numbers.append(information(darkImg)[0])
    
    diffs = []
    
    for i in range(0,254):
        diffs.append(range[i+1]-range[i])
        print(diffs[-1])

    min = np.min(diffs)
    
    perfectValue = diffs.index(min)

    return perfectValue,numbers