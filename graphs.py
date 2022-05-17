from PyQt6.QtWidgets import QWidget, QStackedLayout
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PyQt6.QtCore import Qt

import sys


class Diagram(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.setGeometry(400,500,700,500)
        self.setWindowTitle("Diagramm")
        
        self.widgetLayout = QStackedLayout()
        
        self.setLayout(self.widgetLayout)
        
    
    def displayStatistics(self,analysis):
        
        self.show()
    
    def displayDarkCurve(self,numberArray):
                
        series = QLineSeries()
        
        for i, number in enumerate(numberArray):
            series.append(i,number)
      
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Analyse zum Finden des Dunkelparameters")
        
        abszisse = QValueAxis()
        abszisse.setRange(0,250)
        abszisse.setTickCount(26)
    
        ordinate = QValueAxis()
        ordinate.setRange(0,max(numberArray))
    
        chart.addAxis(ordinate,Qt.AlignmentFlag.AlignLeft)
        chart.addAxis(abszisse,Qt.AlignmentFlag.AlignBottom)
        
        chartView = QChartView(chart)
        
               
        self.widgetLayout.addWidget(chartView)
        
        self.widgetLayout.setCurrentWidget(chartView)
        
        self.show()
        
    #def closeEvent(self,e):
        
        #self.resetLayout()
