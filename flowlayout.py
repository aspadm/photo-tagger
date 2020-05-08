from PyQt5 import QtCore, QtWidgets

class FlowLayout(QtWidgets.QLayout):
    """
    Размечает область таким образом, что не поместившиеся в одну
    строку виджеты переносятся на следующую.
    """
    def __init__(self, parent=None, margin=0, spacing=-1):
        super().__init__(parent)

        if parent is not None:
            self.setContentsMargins(margin)

        self.setSpacing(spacing)

        self.itemList = []

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item: QtWidgets.QLayoutItem) -> None:
        """
        Добавить элемент в разметку.
        """
        self.itemList.append(item)

    def count(self) -> int:
        """
        Число элементов в разметке.
        """
        return len(self.itemList)

    def itemAt(self, index: int) -> QtWidgets.QLayoutItem:
        """
        Получение ссылки на элемент внутри разметки по индексу.
        """
        if index >= 0 and index < len(self.itemList):
            return self.itemList[index]

        return None

    def takeAt(self, index: int) -> QtWidgets.QLayoutItem:
        """
        Извлечение элемента из разметки по индексу.
        """
        if index >= 0 and index < len(self.itemList):
            return self.itemList.pop(index)

        return None

    def expandingDirections(self) -> QtCore.Qt.Orientations:
        """
        Разметка распространяется по горизонтали.
        """
        return QtCore.Qt.Orientations(QtCore.Qt.Orientation(0))

    def hasHeightForWidth(self) -> bool:
        """
        Поддерживает рассчёт высоты по ширине.
        """
        return True

    def heightForWidth(self, width: int) -> int:
        """
        Рассчитать высоту по ширине разметки.
        """
        height = self._doLayout(QtCore.QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect: QtCore.QRect) -> None:
        """
        Задание размеров и положения разметки.
        """
        super().setGeometry(rect)
        self._doLayout(rect, False)

    def sizeHint(self) -> QtCore.QSize:
        """
        Желаемый размер.
        """
        return self.minimumSize()

    def minimumSize(self) -> QtCore.QSize:
        """
        Минимальный размер.
        """
        size = QtCore.QSize()

        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())

        if self.parent() != None:
            margins = self.contentsMargins()
            size += QtCore.QSize(margins.left() + margins.right(),
                                 margins.top() + margins.bottom())

        return size

    def _doLayout(self, rect: QtCore.QRect, testOnly: bool) -> int:
        """
        Пересчёт размеров разметки и расстановка элементов.
        """
        x = rect.x()
        y = rect.y()
        lineHeight = 0

        for item in self.itemList:
            wid = item.widget()
            spaceX = self.spacing() + wid.style().layoutSpacing(
                QtWidgets.QSizePolicy.PushButton,
                QtWidgets.QSizePolicy.PushButton,
                QtCore.Qt.Horizontal)

            spaceY = self.spacing() + wid.style().layoutSpacing(
                QtWidgets.QSizePolicy.PushButton, 
                QtWidgets.QSizePolicy.PushButton, 
                QtCore.Qt.Vertical)

            nextX = x + item.sizeHint().width() + spaceX
            if nextX - spaceX > rect.right() and lineHeight > 0:
                x = rect.x()
                y = y + lineHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                lineHeight = 0

            if not testOnly:
                item.setGeometry(
                    QtCore.QRect(QtCore.QPoint(x, y), item.sizeHint()))

            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())

        return y + lineHeight - rect.y()

if __name__ == "__main__":
    import sys

    class Window(QtWidgets.QWidget):
        def __init__(self):
            super(Window, self).__init__()

            flowLayout = FlowLayout()
            flowLayout.addWidget(QtWidgets.QPushButton("Short"))
            flowLayout.addWidget(QtWidgets.QPushButton("Longer"))
            flowLayout.addWidget(QtWidgets.QPushButton("Different text"))
            flowLayout.addWidget(QtWidgets.QPushButton("More text"))
            flowLayout.addWidget(QtWidgets.QPushButton("Even longer button text"))
            self.setLayout(flowLayout)

            self.setWindowTitle("Flow Layout")

    app = QtWidgets.QApplication(sys.argv)
    mainWin = Window()
    mainWin.show()
    sys.exit(app.exec_())
