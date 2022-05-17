import numpy as np
from PyQt6 import QtGui

def MonoCv2ToQPixmap(monoOpencvImage):
    
    h, w = monoOpencvImage.shape

    # Add 3 Channels
    comparison = np.stack((monoOpencvImage, monoOpencvImage, monoOpencvImage), axis=2)

    bytesPerLine = w * 3
    qPicture = QtGui.QImage(comparison.data, w, h,
                bytesPerLine, QtGui.QImage.Format.Format_BGR888)

    qPixmap = QtGui.QPixmap(qPicture)
    
    return qPixmap
    
    