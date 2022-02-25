import cv2
from findBubbles import *
from extractInformation import *
import matplotlib.pyplot as plt

img = cv2.imread("../../Writing/Graphiken/Tropfenerkennung/WOxverd20210311090950406.png")
img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#img = balanceLight(img)

cv2.imshow("image",cv2.resize(img,(800,600)))

def findLight(gray):
    numbers = []
    der = []
    count = 0
    for i in range(0,256):
        params = parameters.copy()
        params["upper_limit"] = 255-i;
        numbers.append(information(findBubbles(gray,params))[0])
        if len(numbers) > 1:
            der.append(numbers[i] - numbers[i-1])
        if len(der) > 4 and der[i-1]+der[i-2]+der[i-3]+der[i-4]+der[i-5]>0:
            count +=1
        if count >=3:
            return 255-i+2,numbers,der
    return 0,numbers,der

def findDark(gray):
    numbers = []
    mins = []
    for ll in range(0,255):
        darkImg = extractDarks(gray,ll)
        numbers.append(information(darkImg)[0])
        darkImg = cv2.resize(darkImg,(800,600));
        cv2.putText(darkImg,str(ll),(700,540),cv2.FONT_HERSHEY_COMPLEX,1.0,(255,184,79))
        cv2.putText(darkImg,str(ll),(700,560),cv2.FONT_HERSHEY_COMPLEX,1.0,(0,0,0))
        cv2.imwrite("./Fotos/AutoDark/"+str(ll)+".png",darkImg)

        #,str(ll),(400,200),cv2.FONT_HERSHEY_SIMPLEX,500,(255,184,79))

    for x in range(1,254):
        #First Version:
        if numbers[x] + 3 < numbers[x-1] and numbers[x] + 3< numbers[x+1] :
            mins.append(x)

        # Einfluss weiter entfernter Werte mit einbeziehen

    if len(mins) == 0:
        return parameters["lower_limit"],numbers
    return mins[0],numbers

def optimalParameters(img,dname):

    deleteDenoised()
    denoised = getDenoised(img,parameters["blur"])

    parameters["lower_limit"],nL = findDark(denoised)
    parameters["upper_limit"],nU,der = findLight(denoised)

    result = findBubbles(img, parameters)

    plt.figure()
    fig, axs = plt.subplots(2,2)
    
    axs[0,0].imshow(cv2.cvtColor(img,cv2.COLOR_GRAY2RGB))
    axs[1,0].imshow(cv2.cvtColor(result,cv2.COLOR_GRAY2RGB))
    axs[0,1].scatter(range(0,255), nL, c='b')
    axs[0,1].set_title("Lower_limit="+str(parameters["lower_limit"]))
    axs[1,1].scatter(range(255,255-len(nU),-1), nU, c='r')
    axs[1,1].set_title("Upper_limit="+str(parameters["upper_limit"]))
    fig.set_size_inches(16,9)
    fig.savefig(dname,dpi=100)
    plt.close()

    return information(result)


findDark(img)

cv2.waitKey(0)