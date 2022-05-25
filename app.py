from PyQt6 import QtWidgets, QtGui, uic
from PyQt6.QtCore import QThreadPool, Qt
from PyQt6.QtGui import QAction
import sys, os, csv

from files import *

from findBubbles import *
from pictureClasses import *
from timeline import Timeline
from conversions import *
from graphs import *
from extractInformation import *

basedir = os.path.dirname(__file__)

class Wrapper(QtWidgets.QMainWindow):
    def __init__(self):
        super(Wrapper, self).__init__()
        uic.loadUi("./Design.ui", self)
        
        self.setWindowTitle("Tropfen-Serien-Analyse")

        self.count = 0
        self.parameters = {'upper_limit': 200, 'lower_limit': 40,
                           'blur': 10, 'glow': 3, 'siebsize': 10, 'gapsfill': 10}
        self.revealValue = 50
        self.useDarkAnalysis = False
        
        self.changeLight(self.parameters["upper_limit"])
        self.changeDark(self.parameters["lower_limit"])
        self.changeGlow(self.parameters["glow"])
        self.changeSieb(self.parameters["siebsize"])
        self.changeGapfill(self.parameters["gapsfill"])
        self.revealSlider.setValue(self.revealValue)
        
        self.lightsSlider.sliderMoved.connect(self.changeLight)
        self.darksSlider.sliderMoved.connect(self.changeDark)
        self.glowSlider.sliderMoved.connect(self.changeGlow)
        self.siebSlider.sliderMoved.connect(self.changeSieb)
        self.lueckenSlider.sliderMoved.connect(self.changeGapfill)
        self.revealSlider.sliderMoved.connect(self.changeReveal)
        
        self.lightsNumber.editingFinished.connect(self.changeLight)
        self.darksNumber.valueChanged.connect(self.changeDark)
        self.glowNumber.valueChanged.connect(self.changeGlow)
        self.siebNumber.valueChanged.connect(self.changeSieb)
        self.lueckenNumber.valueChanged.connect(self.changeGapfill)
        
        self.darkAnalysisBox.value = False
        self.darkAnalysisBox.stateChanged.connect(self.changeDarkAnalysisState)
        
        self.balanceBox.value = False
        self.balanceInitiated = False
        self.balanceBox.stateChanged.connect(self.changeBalanceState)
        
        self.showSmoothBox.stateChanged.connect(self.reloadImage)
        
        # Load control buttons

        self.backwardsButton.clicked.connect(self.decrease)
        self.forwardsButton.clicked.connect(self.increase)
        self.playButton.clicked.connect(self.playPause)

        folder = "./Icons/"
        if not os.path.exists("./Icons/"):
            folder = "./"

        forwardsIcon = QtGui.QIcon(folder+"forwards.png")
        backwardsIcon = QtGui.QIcon(folder+"backwards.png")
        self.playIcon = QtGui.QIcon(folder+"play.png")
        self.pauseIcon = QtGui.QIcon(folder+"pause.png")

        self.forwardsButton.setIcon(forwardsIcon)
        self.backwardsButton.setIcon(backwardsIcon)
        self.playButton.setIcon(self.playIcon)
        
        self.playing = False

        # Load Menu bar
        self.QAction_load = QAction("Bilderserie laden")
        self.QAction_render = QAction("Gif rendern")
        self.QAction_save = QAction("Analyse speichern")

        self.QAction_load.triggered.connect(self.loadSeries)
        self.QAction_render.triggered.connect(self.renderMovie)
        self.QAction_save.triggered.connect(self.saveAnalysis)
        
        self.analysis = {}

        self.menubar.addAction(self.QAction_load)
        self.menubar.addAction(self.QAction_render)
        self.menubar.addAction(self.QAction_save)

        # Load timeline
        
        self.timeline = Timeline(self)
        self.timelineContainer.addWidget(self.timeline)
        
        self.kontaktWinkelBox.valueChanged.connect(self.generalUpdate)
        self.statistics.setText("")

        # Load Diagram Window
        self.darkAnalyseBtn.clicked.connect(self.openDarkDiagram)
        self.diagramWindow = Diagram()

        # Threading
        self.threadPool = QThreadPool()
        self.show()

    def resizeEvent(self,e):
        self.generalUpdate()

    def generalUpdate(self):
        self.refreshButtonStates()
        self.reloadImage(self.count)
        self.timeline.update()
        if self.useDarkAnalysis:
            self.changeDark(self.Pictures.getDarkParameter(self.count)[0])

    def loadSeries(self):

        fileNames, filter = QtWidgets.QFileDialog.getOpenFileNames(
            directory="/media/nico/Elements/WJ-Experimente Fotos/Beleuchtet/TiO2-behandelt/Kondensieren/Versuch-2")
        
        #fileNames = filesToBeLoaded10P
        
        self.Pictures = Pictures()
        self.threadPool.start(lambda: self.Pictures.loadNBlur(self,fileNames))
        
        self.refreshButtonStates()

    def reloadImage(self,count,display=True):
        
    
        if not hasattr(self,"Pictures"):
            return
    
        if not self.Pictures.hasImage(int(count)):
            return
        
        cv2Picture, blurredPicture = self.Pictures.getImage(int(self.count))
        
        if hasattr(self.Pictures.images[count],"balancedPicture"):
            cv2Picture = self.Pictures.images[count].balancedPicture
        
        bildAnalyse = findBubbles(cv2Picture, self.parameters,denoised=blurredPicture)

        # Analysenstatistik
        n, areas, R = self.Pictures.getAnalysis(bildAnalyse)
                
        n, A, k, V, R = self.getStatistics(n, areas, R)     
               
        if(display):
            self.statistics.setText(f"Bild Nr. {self.count}/{self.Pictures.length} \nTropfenzahl: n = {n} \nFläche: A = {A:.2f} mm²\nBenetzungsgrad: k = {k:.1f} %\nVolumen: V = {V:.3f} mm³ \nRundheit: R = {R:.2f}")
            
            revealSplit = int(self.revealValue/100*bildAnalyse.shape[1])
            
            if self.showSmoothBox.isChecked():
                cv2Picture = blurredPicture

            comparison = np.concatenate((cv2Picture[:, :revealSplit], bildAnalyse[:, revealSplit:]), axis=1)
            qPixmap = MonoCv2ToQPixmap(comparison)
            
            qPixmap = qPixmap.scaled(self.firstLabelGoodMorning.size(),Qt.AspectRatioMode.KeepAspectRatio)

            self.firstLabelGoodMorning.setPixmap(qPixmap)
            
        else:
            return n, A, k, V, R

    def getStatistics(self, n, areas, R):
        
        # Berechnet zusätzlich zur Tropfenzahl n und der Rundheit R auch die benetze Fläche A, das Volumen V wird geschätzt (unter der Annahme von idealen Kugelsegmenttropfen)
        
        A = sum(areas)
        k = A/12000000 * 100
        V = calcVolume(areas,self.kontaktWinkelBox.value())
        
        # Umrechnungen
        A = A/1180/1180
        
        V = V/math.pow(1180,3)
        
        # Returns [n] = 1; [A] = mm²; [k] = %; [V] = mm³; [R] = 1
        
        return n, A, k, V, R

    def refreshButtonStates(self):
        
        self.playButton.setEnabled(True)
        self.forwardsButton.setEnabled(True)
        self.backwardsButton.setEnabled(True)        
        
        if(self.count==0):
            self.backwardsButton.setEnabled(False)
        
        if(hasattr(self,"Pictures") and hasattr(self.Pictures,"images") and self.count==self.Pictures.getBlurredNumber()):
            self.forwardsButton.setEnabled(False)
            self.playButton.setEnabled(False)
            
        if(not hasattr(self,"Pictures")):
            self.playButton.setEnabled(False)
            self.forwardsButton.setEnabled(False)
            self.backwardsButton.setEnabled(False) 

    # Functions concerning Buttons and Count
    def increase(self):
        self.count += 1
        self.generalUpdate()
        self.refreshButtonStates()

    def decrease(self):
        self.count -= 1
        self.generalUpdate()
        self.refreshButtonStates()
        
    def playPause(self):
        if self.playing:
            self.playButton.setIcon(self.playIcon)
            self.playing = False
        else:
            self.playButton.setIcon(self.pauseIcon)
            self.playing = True
            self.threadPool.start(lambda: self.Pictures.play(self))


    def getCount(self):
        
        return self.count

    def getCountRatio(self):
        if hasattr(self,"Pictures"):
            return self.getCount()/(self.Pictures.length-1)
        
        return 0

    # Functions handling Dark-Parameter Analyse

    def changeDarkAnalysisState(self):
        
        self.useDarkAnalysis = not self.useDarkAnalysis
        
        if self.useDarkAnalysis and hasattr(self,"Pictures"):
            self.darksSlider.setEnabled(False)
            self.changeDark(self.Pictures.getDarkParameter(self.count)[0])
        else:
            self.darksSlider.setEnabled(True)
    
    def openDarkDiagram(self):
        
        param, numberArray = self.Pictures.getDarkParameter(self.getCount())
               
        self.diagramWindow.displayDarkCurve(numberArray)

    def changeBalanceState(self):
        
        self.balanceInitiated = True
        
        
        self.threadPool.start(lambda: self.Pictures.balanceSeries(self))
        

    # Functions controlling slider changes
    def changeLight(self, value):
        self.parameters['upper_limit'] = value
        self.lightsNumber.setValue(value)
        self.lightsSlider.setValue(value)
        self.reloadImage(self.count)

    def changeDark(self, value):
        self.parameters['lower_limit'] = value
        self.darksNumber.setValue(value)
        self.darksSlider.setValue(value)
        self.reloadImage(self.count)

    def changeGlow(self, value):
        self.parameters['glow'] = value
        self.glowNumber.setValue(value)
        self.glowSlider.setValue(value)
        self.reloadImage(self.count)

    def changeSieb(self, value):
        self.parameters['siebsize'] = value + 1
        self.siebNumber.setValue(value)
        self.siebSlider.setValue(value)
        self.reloadImage(self.count)

    def changeGapfill(self, value):
        self.parameters['gapsfill'] = value + 1
        self.lueckenNumber.setValue(value)
        self.lueckenSlider.setValue(value)
        self.reloadImage(self.count)

    def changeReveal(self,value):
        self.revealValue = value
        self.reloadImage(self.count)

    # Functions handling MenuBar functions
    def saveAnalysis(self):
        print("Executing saveAnalysis()…")
        
        if not self.Pictures.doneWithBlurring():
            return
        
        fileName,filter = QtWidgets.QFileDialog.getSaveFileName(self,"Save Analysis as CSV-File")
        file = open(fileName,"w")
        
        writer = csv.writer(file)
        writer.writerow(["Tropfenzahl n","benetzte Fläche A/mm²","Benetzungsgrad k/%","Gesamtvolumen V/mm³","Durschnittsrundheit R","Kontaktwinkel φ/°","","darks","ligths","glow","sieb","lückenfüllen","darkParameterAnalyse"])
        
        if not self.Pictures.doneWithBlurring():
            print("Unterbreche saveAnalysis, weil noch nicht alle Bilder geblurrt sind.")
            return
        
        for picNr in range(self.Pictures.length):
            newAnalysis = self.reloadImage(picNr,display=False)
            print(picNr,newAnalysis)    
            writer.writerow(newAnalysis+(self.kontaktWinkelBox.value(),"",self.parameters["upper_limit"],self.parameters["lower_limit"],self.parameters["glow"],self.parameters["siebsize"],self.parameters["gapsfill"]))
            
        file.close()

    def renderMovie(self):
        print("Executing renderMovie()…")

    def keyPressEvent(self,e):
        if e.key() == Qt.Key.Key_Escape.value:
            self.close()
            
    # Handler functions
    
    def getLoadedRatio(self):
        
        if hasattr(self,"Pictures"):
            return self.Pictures.getLoadedRatio()
        return 0
        
    def getBlurredRatio(self):
            
        if hasattr(self,"Pictures"):
            return self.Pictures.getBlurredRatio()
        return 0
    
    def getBalancedRatio(self):
            
        if hasattr(self,"Pictures"):
            return self.Pictures.getBalancedRatio()
        return 0
    
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = Wrapper()
    app.setWindowIcon(QtGui.QIcon(os.path.join(basedir, 'Icon.ico')))
    app.exec()
