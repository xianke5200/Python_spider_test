#!usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QWidget, QApplication, QHBoxLayout, QLabel,
                             QLineEdit,
                            QFrame, QSplitter, QStyleFactory,
                             QComboBox)

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #self.showpixmap()
        #self.showlineedit()
        #self.showsplitter()
        self.showcombox()

        self.setGeometry(300, 300, 250, 150)
        self.show()

    def showpixmap(self):
        hbox = QHBoxLayout(self)
        pixmap = QPixmap('breath_time.png')

        lbl = QLabel(self)
        lbl.setPixmap(pixmap)
        hbox.addWidget(lbl)
        self.setLayout(hbox)

        self.setWindowTitle('Red Rock')

    def showlineedit(self):
        self.lbl = QLabel(self)
        qle = QLineEdit(self)
        qle.move(60, 100)
        self.lbl.move(60, 40)
        qle.textChanged[str].connect(self.onChanged)

        self.setWindowTitle('QLineEdit')

    def onChanged(self, text):
        self.lbl.setText(text)
        self.lbl.adjustSize()

    def showsplitter(self):
        hbox = QHBoxLayout(self)

        topleft = QFrame(self)
        topleft.setFrameShape(QFrame.StyledPanel)

        topright = QFrame(self)
        topright.setFrameShape(QFrame.StyledPanel)

        bottom = QFrame(self)
        bottom.setFrameShape(QFrame.StyledPanel)

        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(topleft)
        splitter1.addWidget(topright)

        splitter2 = QSplitter(Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(bottom)

        hbox.addWidget(splitter2)
        self.setLayout(hbox)

        self.setWindowTitle('QSplitter')

    def showcombox(self):
        self.lbl = QLabel("Ubuntu", self)
        combolist = ["Ubuntu", "Mandriva", "Fedora", "Arch", "Gentoo"]
        combo = QComboBox(self)
        combo.addItems(combolist)
        #combo.addItem("Mandriva")
        #combo.addItem("Fedora")
        #combo.addItem("Arch")
        #combo.addItem("Gentoo")

        combo.move(50, 50)
        self.lbl.move(50, 150)

        combo.activated[str].connect(self.onActived)

        self.setWindowTitle("QComboBox")

    def onActived(self, text):
        self.lbl.setText(text)
        self.lbl.adjustSize()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())