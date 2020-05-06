import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from photowidget import PhotoWidget

""" TODO:
mainwindow
    splitter
        scrollarea (horizontal layout)
            checkbox (tag)
        scrollarea (grid layout)
            photowidget (2 labels)
"""

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Photo tagger")
        
        self.test = PhotoWidget(self, "./chi.png")
        
        self.show()
        
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Exit',
            "Are you sure to quit?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()    

if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = MainWindow()

    sys.exit(app.exec_())
