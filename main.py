import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QSplitter, QListView, QScrollArea
from photowidget import PhotoWidget
from flowlayout import FlowLayout

""" TODO:
mainwindow
    splitter
        scrollarea (horizontal layout)
            checkbox (tag)
        scrollarea (grid layout)
            photowidget (2 labels)
"""

class MainWindow(QSplitter):
    def __init__(self):
        super().__init__()
        
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Photo tagger")
        
        self.listview = QListView(self)
        self.addWidget(self.listview)
        
        self.photos_container = QScrollArea()
        self.photos = QWidget()
        flow_layout = FlowLayout()
        flow_layout.addWidget(PhotoWidget(self, "./Screenshot.png"))
        flow_layout.addWidget(PhotoWidget(self, "./Screenshot.png"))
        flow_layout.addWidget(PhotoWidget(self, "./chi.png"))
        self.photos.setLayout(flow_layout)
        self.photos_container.setWidget(self.photos)
        self.photos_container.setWidgetResizable(True)
        self.addWidget(self.photos_container)
        
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
