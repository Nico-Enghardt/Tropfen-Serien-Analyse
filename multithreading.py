import sys
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QPainter, QColor, QFont
from PyQt6.QtCore import Qt
import random


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.text = "Лев Николаевич Толстой\nАнна Каренина"

        self.setMinimumSize(50, 50)
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Points')
        self.show()
    
    def paintEvent(self, event):

        qp = QPainter()
        qp.begin(self)
        self.drawMyStuff(qp)
        qp.end()

    def drawMyStuff(self,qp):
        qp.setPen(QColor(255,200,255))
        qp.fillRect(20,50,100,200,QColor(255,200,255))

    def drawText(self, event, qp):

        qp.setPen(QColor(168, 168, 200))
        qp.setFont(QFont('Decorative', 10))
        qp.drawText(event.rect(), Qt.AlignmentFlag.AlignCenter, self.text)

    def drawPoints(self, qp):
    
        qp.setPen(Qt.GlobalColor.red)
        size = self.size()

        for i in range(100000):

            x = random.randint(1, size.width() - 1)
            y = random.randint(1, size.height() - 1)
            qp.drawPoint(x, y)


def main():

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()