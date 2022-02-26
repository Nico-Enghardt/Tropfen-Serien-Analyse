from PyQt6 import QtWidgets, QtGui, uic
from PyQt6.QtCore import QThreadPool, QObject, Qt, pyqtSignal,QCoreApplication
from PyQt6.QtGui import QAction, QPixmap, QPainter, QPen
import sys, os, time, cv2
from files import *

from findBubbles import *
from pictureClasses import *
from timeline import Timeline

basedir = os.path.dirname(__file__)

class Wrapper(QtWidgets.QMainWindow):
    def __init__(self):
        super(Wrapper, self).__init__()
        uic.loadUi("./Design.ui", self)

        self.count = 0
        self.parameters = {'upper_limit': 100, 'lower_limit': 10,
                           'blur': 40, 'glow': 3, 'siebsize': 31, 'gapsfill': 40}
        self.revealValue = 50
        
        self.lightsSlider.setValue(100)
        self.darksSlider.setValue(10)
        self.glowSlider.setValue(3)
        self.siebSlider.setValue(31)
        self.lueckenSlider.setValue(40)
        self.revealSlider.setValue(self.revealValue)
        

        self.lightsSlider.sliderMoved.connect(self.changeLight)
        self.darksSlider.sliderMoved.connect(self.changeDark)
        self.glowSlider.sliderMoved.connect(self.changeGlow)
        self.siebSlider.sliderMoved.connect(self.changeSieb)
        self.lueckenSlider.sliderMoved.connect(self.changeGapfill)
        self.revealSlider.sliderMoved.connect(self.changeReveal)
        
        # Load control buttons

        self.backwardsButton.clicked.connect(self.decrease)
        self.forwardsButton.clicked.connect(self.increase)
        self.playButton.clicked.connect(self.playPause)

        forwardsIcon = QtGui.QIcon("Icons/forwards.png")
        backwardsIcon = QtGui.QIcon("Icons/backwards.png")
        self.playIcon = QtGui.QIcon("Icons/play.png")
        self.pauseIcon = QtGui.QIcon("Icons/pause.png")

        self.forwardsButton.setIcon(forwardsIcon)
        self.backwardsButton.setIcon(backwardsIcon)
        self.playButton.setIcon(self.playIcon)
        
        self.playing = False

        # Load Menu bar
        self.QAction_load = QAction("Load Series")
        self.QAction_render = QAction("Render Movie")
        self.QAction_save = QAction("Save Analysis")

        self.QAction_load.triggered.connect(self.loadSeries)
        self.QAction_render.triggered.connect(self.renderMovie)
        self.QAction_save.triggered.connect(self.saveAnalysis)

        self.menubar.addAction(self.QAction_load)
        self.menubar.addAction(self.QAction_render)
        self.menubar.addAction(self.QAction_save)

        # Load timeline
        
        self.timeline = Timeline(self)
        self.timelineContainer.addWidget(self.timeline)

        # Threading
        self.threadPool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadPool.maxThreadCount())

        self.show()

    def resizeEvent(self,e):
        self.reloadImage()

    def loadSeries(self):

        #fileNames, filter = QtWidgets.QFileDialog.getOpenFileNames(
        #    directory="/media/nico/Elements/WJ-Experimente Fotos/Beleuchtet/TiO2-behandelt/Kondensieren/Versuch-2/")
        
        fileNames = filesToBeLoaded10P
        
        self.Pictures = Pictures()
        self.threadPool.start(lambda: self.Pictures.loadNBlur(self,fileNames))
        #self.Pictures.loadNBlur(self,fileNames)
        
        self.refreshButtonStates()

    def reloadImage(self):
    
        cv2Picture, blurredPicture = self.Pictures.getImage(int(self.count))
        bildAnalyse = findBubbles(cv2Picture, self.parameters,denoised=blurredPicture)

        # Analysenstatistik
        n, areas, R = self.Pictures.getAnalysis(bildAnalyse,self.kontaktWinkelBox.value)
        
        self.statistics.setText(f"Tropfenzahl: {n}  Fläche: {sum(areas)}  Rundheit: {R}")

        h, w = bildAnalyse.shape
        
        revealSplit = int(self.revealValue/100*w)

        comparison = np.concatenate(
            (cv2Picture[:, :revealSplit], bildAnalyse[:, revealSplit:]), axis=1)

        # Add 3 Channels
        comparison = np.stack((comparison, comparison, comparison), axis=2)

        bytesPerLine = w * 3
        qPicture = QtGui.QImage(comparison.data, w, h,
                    bytesPerLine, QtGui.QImage.Format.Format_BGR888)

        qPixmap = QtGui.QPixmap(qPicture)
        qPixmap = qPixmap.scaled(self.firstLabelGoodMorning.size(),Qt.AspectRatioMode.KeepAspectRatio)

        self.firstLabelGoodMorning.setPixmap(qPixmap)
        
    def refreshButtonStates(self):
        self.playButton.setEnabled(True)
        self.forwardsButton.setEnabled(True)
        self.backwardsButton.setEnabled(True)        
        
        if(self.count==0):
            self.backwardsButton.setEnabled(False)
        
        if(hasattr(self.Pictures,"images") and self.count==len(self.Pictures.images)-1):
            self.forwardsButton.setEnabled(False)
            self.playButton.setEnabled(False)

    def increase(self):
        self.count += 1
        self.refreshButtonStates()
        self.reloadImage()

    def decrease(self):
        self.count -= 1
        self.refreshButtonStates()
        self.reloadImage()

    def playPause(self):
        if self.playing:
            self.playButton.setIcon(self.playIcon)
            self.playing = False
            print("Paused …")
        else:
            self.playButton.setIcon(self.pauseIcon)
            self.playing = True
            self.threadPool.start(lambda: self.Pictures.play(self))
            print("Playing …")

    def changeLight(self, value):
        self.parameters['upper_limit'] = value
        self.reloadImage()

    def changeDark(self, value):
        self.parameters['lower_limit'] = value
        self.reloadImage()

    def changeGlow(self, value):
        self.parameters['glow'] = value
        self.reloadImage()

    def changeSieb(self, value):
        self.parameters['siebsize'] = value + 1
        self.reloadImage()

    def changeGapfill(self, value):
        self.parameters['gapsfill'] = value + 1
        self.reloadImage()

    def changeReveal(self,value):
        self.revealValue = value
        self.reloadImage()

    def saveAnalysis(self):
        print("Executing saveAnalysis()…")

    def renderMovie(self):
        print("Executing renderMovie()…")

    def keyPressEvent(self,e):
        if e.key() == Qt.Key.Key_Escape.value:
            self.close()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = Wrapper()

    app.exec()
