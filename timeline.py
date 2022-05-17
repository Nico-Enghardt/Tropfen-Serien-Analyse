from PyQt6.QtWidgets import QWidget
from PyQt6 import QtCore, QtGui
import math

class Timeline(QWidget):
    
    def __init__(self, parent):
        
        super(Timeline,self).__init__(parent)
        
        self.loadRatio = 0
        self.blurRatio = 0
        
        self.setMinimumSize(25,25)  
        self.show()
        
        self.previewImages = []
        self.parent = parent
        
    def paintEvent(self,event):
                
        qp = QtGui.QPainter()
        qp.begin(self)
        
    
        # pNumbers = self.determinePreviews()
    
        # for n,p in enumerate(pNumbers):
           
        #     if p+1 < len(self.previewImages):
           
        #         pixmap = self.previewImages[p]
               
        #         w, h = self.size().width(), self.size().height()
        #         qp.drawPixmap(pixmap.size().width()*n*1.01,0,pixmap)
        
        loadRatio = self.parent.getLoadedRatio()
        blurRatio = self.parent.getBlurredRatio()
        balanceRatio = self.parent.getBalancedRatio()
        
           
        qp.fillRect(0,5,self.size().width()*loadRatio,15,QtGui.QColor(219, 58, 46))
        qp.fillRect(0,5,self.size().width()*blurRatio,15,QtGui.QColor(39, 161, 242))
        qp.fillRect(0,5,self.size().width()*balanceRatio,15,QtGui.QColor(62, 235, 42))
        
        
        xpos = self.size().width()*self.parent.getCountRatio()-2
        
        if blurRatio > 0:    
            qp.fillRect(xpos,0,4,25,QtGui.QColor(10,10,10))
        
        qp.end()
        
    def determinePreviews(self):
        
        w, h = self.size().width(), self.size().height()
        # Calculate number of images neccessary to fill the timeline
        number = math.ceil(w/h*3/4)
        
        pNumbers = []
        
        for n in range(number-1):

            pNumbers.append(round(h/w*4/3*n*number))
        return pNumbers
        
    
    def loadPreviews(self,images):
        
        w, h = self.size().width(), self.size().height()
        
        for image in images:
            
            imageSource = image.fileName
            
            pixmapImage = QtGui.QPixmap(imageSource)
            
            self.previewImages.append(pixmapImage.scaled(w,h,QtCore.Qt.AspectRatioMode.KeepAspectRatio))
    
        
        
        
        