#!usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton, QLineEdit)
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag
from PyQt5 import QtGui

class Button(QPushButton):
    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        if e.mineData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.setText(e.mineData.text())

class Button1(QPushButton):
    def __init__(self, title, parent):
        super(Button1, self).__init__(title, parent)

    def mouseMoveEvent(self, e: QtGui.QMouseEvent):
        if e.button() != Qt.RightButton:
            return
        mimeData = QMimeData()
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())

        dropAction = drag.exec_(Qt.MoveAction)

    def mousePressEvent(self, e: QtGui.QMouseEvent):
        QPushButton.mousePressEvent(self, e)
        if e.button() == Qt.LeftButton:
            print('press')

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #self.simpleDrag()
        self.simpleDrag2()

        self.setGeometry(300, 300, 250, 150)

    def simpleDrag(self):
        edit = QLineEdit('', self)
        edit.setDragEnabled(True)
        edit.move(30, 65)

        button = Button("Button", self)
        button.move(190, 65)

        self.setWindowTitle('Simple drag & drop')

    def simpleDrag2(self):
        self.setAcceptDrops(True)
        self.button1 = Button1('Button', self)
        self.button1.move(100, 65)

        self.setWindowTitle('Click or Move')

    def dragEnterEvent(self, a0: QtGui.QDragEnterEvent):
        a0.accept()

    def dropEvent(self, a0: QtGui.QDropEvent):
        position = a0.pos()
        self.button1.move(position)

        a0.setDropAction(Qt.MoveAction)
        a0.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    app.exec_()