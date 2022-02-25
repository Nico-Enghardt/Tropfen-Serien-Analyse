import cv2
from tqdm import tqdm
from findBubbles import *
from PyQt6.QtCore import QObject, pyqtSignal
from extractInformation import *

class Picture():
    
    def __init__(self,fileName):
        
        self.fileName = fileName
        self.picture = cv2.imread(fileName)[:,:,0]
        self.blurredPicture = []
        self.Areas = None
        self.Volume = None
        
class Pictures(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
        
    def loadNBlur(self,parent,fileNames):
        self.images = [];
        
        print("Let's continue")
        
        for file in tqdm(fileNames):
            self.images.append(Picture(file))
            
        print("Loading files done")
        
        for image in tqdm(self.images):
            #image.blurredPicture = getDenoised(image.picture,parent.parameters["blur"])
            print(image)

        print("Blurring files done")
        
    def getImage(self,number):
        return self.images[number].picture,self.images[number].blurredPicture
    
    def getAnalysis(self,bildmanipulation,kontaktwinkel):
        
        n, areas, R =  information(bildmanipulation)
        
        return n, areas, R