from PyQt5.QtWidgets import QWidget, QApplication, QFrame, QLabel, QMenu
from PyQt5.QtGui import QPixmap, QMouseEvent
from PyQt5.QtCore import Qt, QEvent, pyqtSignal
import subprocess, os, platform
import os.path

class PhotoWidget(QFrame):
    """
    Миниатюра изображения с подписью.

    :var change_tags: сигнал для запуска редактора тегов
    """

    change_tags = pyqtSignal(str)

    def __init__(self, parent: QWidget, filename: str):
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

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """
        Обработка событий от мыши - открытие изображения и меню действий.

        :param event: событие мыши
        :type event: QMouseEvent
        """
        if event.button() == Qt.LeftButton:
            self.openImage()
        elif event.button() == Qt.RightButton:
            self.list_menu = QMenu()
            menu_item = self.list_menu.addAction("Open image")
            menu_item.triggered.connect(self.openImage)
            menu_item = self.list_menu.addAction("Copy path")
            menu_item.triggered.connect(self.copyPath)
            menu_item = self.list_menu.addAction("Edit tags")
            menu_item.triggered.connect(self.editTags)
            self.list_menu.move(self.mapToGlobal(event.pos()))
            self.list_menu.show()

    def openImage(self) -> None:
        """
        Открытие изображения во внешнем приложении.
        """
        if platform.system() == 'Darwin': # macOS
            subprocess.call(('open', self.filename))
        elif platform.system() == 'Windows': # Windows
            os.startfile(self.filename)
        else:  # linux variants
            subprocess.call(('xdg-open', self.filename))

    def copyPath(self) -> None:
        """
        Копирование пути до изображения в буфер обмена.
        """
        clipboard = QApplication.clipboard()
        clipboard.setText(self.filename)
        QApplication.sendEvent(clipboard, QEvent(QEvent.Clipboard))

    def editTags(self) -> None:
        """
        Вызов редактора тегов.
        """
        self.change_tags.emit(self.filename)
