import cv2
from tqdm import tqdm
from findBubbles import *
from PyQt6.QtCore import QRunnable, pyqtSlot
from extractInformation import *
import time

class Picture():
    
    def __init__(self,fileName):
        
        self.fileName = fileName
        self.picture = cv2.imread(fileName)[:,:,0]
        self.blurredPicture = []
        self.Areas = None
        self.Volume = None
        
class Pictures(QRunnable):
    
    @pyqtSlot()
        
    def loadNBlur(self,parent,fileNames):
        self.images = [];
        
        print("Let's load!")
        
        for i, file in enumerate(fileNames):
            self.images.append(Picture(file))
            parent.timeline.loadRatio = i/len(fileNames)
            parent.timeline.update()
        
        for i, image in enumerate(self.images):
            image.blurredPicture = getDenoised(image.picture,parent.parameters["blur"])
            #time.sleep(0.01)
            parent.timeline.blurRatio = i/len(fileNames)
            parent.timeline.update()

        parent.refreshButtonStates()
        parent.reloadImage() 
        
    def getImage(self,number):
        return self.images[number].picture,self.images[number].blurredPicture
    
    def getAnalysis(self,bildmanipulation,kontaktwinkel):
        
        n, areas, R =  information(bildmanipulation)
        
        return n, areas, R
    
    def play(self,parent):
        for i in range(len(self.images)-1-parent.count):
            if not parent.playing:
                break
            time.sleep(0.3)
            parent.count += 1
            parent.reloadImage()
        parent.playing = False
        
