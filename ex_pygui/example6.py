#!usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit,QInputDialog, QApplication,
    QFrame, QColorDialog,
    QVBoxLayout, QSizePolicy, QLabel, QFontDialog,
    QMainWindow, QTextEdit, QAction, QFileDialog)

from PyQt5.QtGui import QColor, QIcon

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #self.inputdialog()
        #self.colordialog()
        #self.fontdialog()
        self.filedialog()

        self.setGeometry(300, 300, 290, 150)
        self.show()

    def inputdialog(self):
        self.btn = QPushButton('Dialog', self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.showDialog)

        self.le = QLineEdit(self)
        self.le.move(130, 22)

        self.setWindowTitle('Input dialog')

    def showDialog(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter your name')

        if ok:
            self.le.setText(str(text))

    def colordialog(self):
        col = QColor(0, 0, 0)
        self.btn = QPushButton('Dialog', self)
        self.btn.move(20, 20)

        self.btn.clicked.connect(self.showColor)

        self.frm = QFrame(self)
        self.frm.setStyleSheet('QWidget { background-color: %s }' %col.name())
        self.frm.setGeometry(130, 22, 100, 100)
        self.setWindowTitle('Color dialog')

    def showColor(self):
        col = QColorDialog.getColor()

        if col.isValid():
            self.frm.setStyleSheet('QWidget { background-color: %s }' %col.name())

    def fontdialog(self):
        vbox = QVBoxLayout()
        btn = QPushButton('Dialog', self)
        btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        btn.move(20, 20)
        vbox.addWidget(btn)
        btn.clicked.connect(self.showFont)

        self.lbl = QLabel('Knowledge only matters', self)
        self.lbl.move(130, 20)

        vbox.addWidget(self.lbl)
        self.setLayout(vbox)

        self.setWindowTitle('Font dialog')

    def showFont(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.lbl.setFont(font)

    def filedialog(self):
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.statusBar()

        openFile = QAction(QIcon('breath_time.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showFile)

        menubar = self.menuBar()
        fileMeni = menubar.addMenu('&File')
        fileMeni.addAction(openFile)

        self.setWindowTitle('File dialog')

    def showFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        if fname[0]:
            with open(fname[0], 'r') as f:
                data = f.read()
                self.textEdit.setText(data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())