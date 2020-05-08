"""
@author: Кириллов А.В., ИУ7-82Б

Основной файл приложения, реализация главного окна.
"""

import sys
import os.path
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QSplitter, QListView, QScrollArea, QVBoxLayout, QCheckBox, QPushButton, QLabel
from PyQt5.QtGui import QCloseEvent
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
    """
    Основное окно приложения из списка тегов, поля с картинками и
    редактора тегов.
    """

    def __init__(self):
        super().__init__()
        
        self.initUI()
    
    def initUI(self) -> None:
        """
        Инициализация окна приложения
        """
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
        
    def closeEvent(self, event: QCloseEvent) -> None:
        """
        Вывод диалога при выходе.
        """
        reply = QMessageBox.question(self, "Exit",
            "Are you sure to quit?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    
    def clearImages(self) -> None:
        """
        Очистка области просмотра от изображений.
        """
        self.flow_layout.__del__()
    
    def addImages(self, images: list) -> None:
        """
        Добавление изображений в область просмотра.

        :param images: список путей до изображений
        :type images: list
        """
        for img_path in images:
            img = PhotoWidget(self, img_path)
            img.change_tags.connect(self.updateTags)
            self.flow_layout.addWidget(img)

    def selectAllTags(self) -> None:
        """
        Отметить все теги, как выбранные.
        """
        for checkbox in self.tags_checkboxes:
            checkbox.setChecked(True)

        self.updateImages()
    
    def deselectAllTags(self) -> None:
        """
        Отметить все теги, как не выбранные.
        """
        for checkbox in self.tags_checkboxes:
            checkbox.setChecked(False)

        self.updateImages()
    
    def getTags(self) -> list:
        """
        Получить список тегов для поиска изображений.

        :rtype: list
        """
        tags = []

        for checkbox, tag in zip(self.tags_checkboxes, tag_classes):
            if checkbox.isChecked():
                tags.append(tag)
        
        if len(tags) == 0:
            tags = tag_classes[:]
        
        return tags
    
    def updateDatabase(self) -> None:
        """
        Обновление содержимого БД при запуске приложения.
        """
        # TODO: создание БД при её отсутствии
        
        # TODO: сканирование папки на изменения, обновление БД
        
        pass
    
    def updateImages(self) -> None:
        """
        Вывод изображений, соответствующих выбранным тегам.
        """
        tags = self.getTags()
        # TODO: получение изображений из БД
        #images = 
        images = []
        
        self.clearImages()
        self.addImages(images)
    
    def updateTags(self, name: str) -> None:
        """
        Отображение редактора тегов для изображения.

        :param name: путь до изображения
        :type name: str
        """
        picker = TagsPicker(self, name)
        picker.show()

class TagsPicker(QWidget):
    """
    Редактор тегов для изображения.

    :param parent: родительский виджет
    :type parent: QWidget
    :param filename: путь до редактируемого изображения
    :type filename: str
    """

    def __init__(self, parent: QWidget, filename: str):
        super().__init__(parent)

        self.filename = filename

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
        self.save = QPushButton("Save tags", self)
        self.save.clicked.connect(self.saveTags)
        self.cancel = QPushButton("Cancel", self)
        self.cancel.clicked.connect(self.closePanel)
        self.tags_side_layout.addWidget(QLabel(os.path.split(filename)[-1]))
        self.tags_side_layout.addWidget(self.select_all)
        self.tags_side_layout.addWidget(self.deselect_all)
        self.tags_side_layout.addWidget(self.tags_container)
        self.tags_side_layout.addWidget(self.save)
        self.tags_side_layout.addWidget(self.cancel)
        self.setLayout(self.tags_side_layout)

        # TODO: получить теги файла из БД
        tags_list = []

        self.tags_checkboxes = [QCheckBox(tag, self.tags) for tag in tag_classes]

        for tag_checkbox, tag in zip(self.tags_checkboxes, tag_classes):
            tag_checkbox.setChecked(tag in tags_list)
            self.tags_layout.addWidget(tag_checkbox)

    def selectAllTags(self) -> None:
        """
        Отметить все теги, как выбранные.
        """
        for checkbox in self.tags_checkboxes:
            checkbox.setChecked(True)

    def deselectAllTags(self) -> None:
        """
        Отметить все теги, как не выбранные.
        """
        for checkbox in self.tags_checkboxes:
            checkbox.setChecked(False)

    def saveTags(self) -> None:
        """
        Сохранение новых тегов изображения в БД.
        """
        tags = []

        for checkbox, tag in zip(self.tags_checkboxes, tag_classes):
            if checkbox.isChecked():
                tags.append(tag)

        if len(tags) == 0:
            QMessageBox.warning(self, "No tags assigned",
                "No tags assigned at all!\nChanges will not saved")
        else:
            # TODO: сохранить новые теги
            pass

        self.closePanel()

    def closePanel(self) -> None:
        """
        Закрытие редактора тегов.
        """
        self.deleteLater()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    w = MainWindow()

    sys.exit(app.exec_())
