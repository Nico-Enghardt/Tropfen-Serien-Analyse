from PyQt6.QtWidgets import QWidget
from PyQt6 import QtCore, QtGui

class Timeline(QWidget):
    
    def __init__(self, parent):
        
        super(Timeline,self).__init__(parent)
        
        self.loadRatio = 0
        self.blurRatio = 0
        
        self.setMinimumSize(100,100)  
        self.show()
        
    def paintEvent(self,event):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.fillRect(0,0,self.size().width()*self.loadRatio,15,QtGui.QColor(219, 58, 46))
        qp.fillRect(0,0,self.size().width()*self.blurRatio,15,QtGui.QColor(39, 161, 242))
        
        qp.end()