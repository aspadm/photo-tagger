from PyQt5.QtWidgets import QFrame, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os.path

class PhotoWidget(QFrame):
    def __init__(self, parent, filename):
        super().__init__(parent)
        
        self.filename = filename
        #self.setFrameStyle(QFrame.Panel)
        self.setFixedSize(160, 160)

        self.preview_label = QLabel("", parent=self)
        self.preview_label.setPixmap(QPixmap(filename).scaled(128, 128,
            aspectRatioMode=Qt.KeepAspectRatio))
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setGeometry(16, 4, 128, 128)
        
        self.text_label = QLabel(os.path.split(filename)[-1], parent=self)
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setGeometry(4, 132, 152, 28)
