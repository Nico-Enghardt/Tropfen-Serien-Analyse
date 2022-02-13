from PyQt6 import QtWidgets
from PyQt6.QtGui import QPixmap
from PyQt6 import uic
import sys, os

basedir = os.path.dirname(__file__)

class Wrapper(QtWidgets.QMainWindow):
    def __init__(self):
        super(Wrapper, self).__init__()
        uic.loadUi("./Design.ui",self)
        
        self.ClickmeButton.setText("Hello!")
        
        
        
        
        picture = QPixmap("./Kursfoto.jpg")
        
        self.firstLabelGoodMorning.setPixmap(picture)
        self.firstLabelGoodMorning.setGeometry(5,10,500,300)
        
        self.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = Wrapper()
    app.exec()
    
