from PyQt6.QtCore import QRunnable, pyqtSlot

import cv2, time

from findBubbles import *
from findParameters import *
from extractInformation import *


class Picture():
    
    def __init__(self,fileName):
        
        self.fileName = fileName
        self.picture = cv2.imread(fileName)[:,:,0]
        w,h,c = 
        if w > 2000 or h > 2000:
            self.picture = cv2.resize(self.picture,(w/4,h/4))
        #self.blurredPicture = None
        #self.balancedPicture = None
        self.Areas = None
        self.Volume = None
        
class Pictures(QRunnable):
    
    @pyqtSlot()
    
    def __init__(self):
        self.images = []
        self.length = 0
        
        
    def loadNBlur(self,parent,fileNames):
        self.images = [];
        self.length = len(fileNames)
        self.loadedNr = -1
        self.blurredNr = -1
        self.balancedNr = -1 
        
        for i, file in enumerate(fileNames):
            if parent.isVisible():
                self.images.append(Picture(file))
                self.loadedNr += 1
                parent.timeline.update()
        
        for image in self.images:
            if parent.isVisible():
                
                image.blurredPicture = getDenoised(image.picture,parent.parameters["blur"])
                image.darkParameter,image.numberArray = findDark(image.blurredPicture)
                
                self.blurredNr += 1
                
                parent.generalUpdate()

    def balanceSeries(self,parent):
                
        for i,image in enumerate(self.images):
        
            image.balancedPicture = balanceLight(image.picture)
            image.blurredPicture = getDenoised(image.balancedPicture,parent.parameters["blur"])
            
            self.balancedNr += 1
                   
            parent.timeline.update()
    
    def getLoadedRatio(self):
        
        return (self.loadedNr)/(self.length-1)
    
    def getBlurredRatio(self):
        
        return (self.blurredNr)/(self.length-1)
      
    def getBalancedRatio(self):
        return (self.balancedNr)/(self.length-1)
    
    def getBlurredNumber(self):
        
        if hasattr(self,"blurredNr"):
            return self.blurredNr
        
        return 0
      
    def getImage(self,number):
        return self.images[number].picture,self.images[number].blurredPicture
    
    def hasImage(self,number):
        
        if len(self.images)<number:
            return False
        
        if not hasattr(self.images[number],"blurredPicture"):
            return False
        
        return True
    
    def hasBalanced(self,number):
        
        if len(self.images)<number or not hasattr(self.images[number],"balancedPicture"):
            return False
        
        return True
    
    def getDarkParameter(self,number):
        
        if self.hasImage(number):
            
            return self.images[number].darkParameter,self.images[number].numberArray
    
    def getAnalysis(self,bildmanipulation):
        
        n, areas, R =  information(bildmanipulation)
        
        return n, areas, R
    
    def play(self,parent):
        
        while parent.getCount() < self.getBlurredNumber():
            if not parent.playing:
                break
            time.sleep(0.3)
            parent.count += 1
            parent.generalUpdate()
        parent.playPause()
        
    def doneWithBlurring(self):
        if self.length == self.blurredNr:          
            return True
        return False