import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QSplitter, QListView, QScrollArea, QVBoxLayout, QCheckBox, QPushButton
from photowidget import PhotoWidget
from flowlayout import FlowLayout

tag_classes = [
    "airplane", "apple", "backpack", "banana", "baseball bat",
    "baseball glove", "bear", "bed", "bench", "bicycle", "bird",
    "boat", "book", "bottle", "bowl", "broccoli", "bus", "cake",
    "car", "carrot", "cat", "cell phone", "chair", "clock", "couch",
    "cow", "cup", "dining table", "dog", "donot", "elephant",
    "fire hydrant", "fork", "frisbee", "giraffe", "hair dryer", "handbag",
    "horse", "hot dog", "keyboard", "kite", "knife", "laptop", "microwave",
    "motorcycle", "mouse", "orange", "oven", "parking meter", "person",
    "pizza", "potted plant", "refrigerator", "remote", "sandwich",
    "scissors", "sheep", "sink", "skateboard", "skis", "snowboard", "spoon", 
    "sports ball", "stop_sign", "suitcase", "surfboard", "teddy bear",
    "tennis racket", "tie", "toaster", "toilet", "toothbrush",
    "traffic light", "train", "truck", "tv", "umbrella", "vase",
    "wine glass", "zebra"
    ]

class MainWindow(QSplitter):
    def __init__(self):
        super().__init__()
        
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Photo tagger")
        self.resize(862, 600)
        
        self.tags_side = QWidget(self)
        self.tags_container = QScrollArea()
        self.tags = QWidget()
        self.tags_layout = QVBoxLayout()
        
        self.tags.setLayout(self.tags_layout)
        self.tags_container.setWidgetResizable(True)
        self.tags_container.setWidget(self.tags)
        self.tags_side_layout = QVBoxLayout()
        self.select_all = QPushButton("Select all", self)
        self.select_all.clicked.connect(self.selectAllTags)
        self.deselect_all = QPushButton("Deselect all", self)
        self.deselect_all.clicked.connect(self.deselectAllTags)
        self.tags_side_layout.addWidget(self.select_all)
        self.tags_side_layout.addWidget(self.deselect_all)
        self.tags_side_layout.addWidget(self.tags_container)
        self.tags_side.setLayout(self.tags_side_layout)
        self.addWidget(self.tags_side)
        
        self.photos_container = QScrollArea()
        self.photos = QWidget()
        self.flow_layout = FlowLayout()
        self.photos.setLayout(self.flow_layout)
        self.photos_container.setWidget(self.photos)
        self.photos_container.setWidgetResizable(True)
        self.addWidget(self.photos_container)
        
        self.tags_checkboxes = [QCheckBox(tag, self.tags) for tag in tag_classes]
        
        for tag_checkbox in self.tags_checkboxes:
            tag_checkbox.clicked.connect(self.updateImages)
            self.tags_layout.addWidget(tag_checkbox)
        
        self.updateDatabase()
        self.updateImages()
        
        self.setSizes([200, 662])
        self.show()
        
    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Exit",
            "Are you sure to quit?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    
    def clearImages(self):
        self.flow_layout.__del__()
    
    def addImages(self, images):
        for img_path in images:
            self.flow_layout.addWidget(PhotoWidget(self, img_path))

    def selectAllTags(self):
        for checkbox in self.tags_checkboxes:
            checkbox.setChecked(True)

        self.updateImages()
    
    def deselectAllTags(self):
        for checkbox in self.tags_checkboxes:
            checkbox.setChecked(False)

        self.updateImages()
    
    def getTags(self):
        tags = []
        
        for checkbox, tag in zip(self.tags_checkboxes, tag_classes):
            if checkbox.isChecked():
                tags.append(tag)
        
        if len(tags) == 0:
            tags = tag_classes[:]
        
        return tags
    
    def updateDatabase(self):
        # TODO: создание БД при её отсутствии
        
        # TODO: сканирование папки на изменения, обновление БД
        
        pass
    
    def updateImages(self):
        tags = self.getTags()
        # TODO: получение изображений из БД
        #images = 
        images = ["chi.png", "Screenshot.png", "chi.png", "Screenshot.png", "chi.png", "Screenshot.png"]
        
        self.clearImages()
        self.addImages(images)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    w = MainWindow()

    sys.exit(app.exec_())
