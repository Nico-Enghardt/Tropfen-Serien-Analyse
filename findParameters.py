import cv2
from findBubbles import *
from extractInformation import *

def findDark(gray):
    numbers = []
    mins = []
    for ll in range(0,255):
        darkImg = extractDarks(gray,ll)
        numbers.append(information(darkImg)[0])
        darkImg = cv2.resize(darkImg,(800,600));
        #cv2.putText(darkImg,str(ll),(700,540),cv2.FONT_HERSHEY_COMPLEX,1.0,(255,184,79))
        #cv2.putText(darkImg,str(ll),(700,560),cv2.FONT_HERSHEY_COMPLEX,1.0,(0,0,0))
        #cv2.imwrite("./Fotos/AutoDark/"+str(ll)+".png",darkImg)


    for x in range(1,254):
        #First Version:
        if numbers[x] + 3 < numbers[x-1] and numbers[x] + 3< numbers[x+1] :
            mins.append(x)

        # Einfluss weiter entfernter Werte mit einbeziehen

    if len(mins) == 0:
        return 0,numbers
    return mins[0],numbers