#!usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QWidget, QApplication, QCheckBox,
    QPushButton, QFrame,
    QSlider, QLabel,
    QProgressBar,
    QCalendarWidget)

from PyQt5.QtCore import Qt, QBasicTimer, QDate
from PyQt5.QtGui import QColor, QPixmap, QFont

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #self.showCheckbox()
        #self.showbutton()
        #self.showslider()
        self.showprogress()
        #self.showcalendar()

        self.setGeometry(300, 300, 250, 150)
        self.show()

    def showCheckbox(self):
        cb = QCheckBox('Show title', self)
        cb.move(20, 20)
        cb.toggle()
        cb.stateChanged.connect(self.changeTitle)

        self.setWindowTitle('QCheckBox')

    def changeTitle(self, state):
        if state == Qt.Checked:
            self.setWindowTitle('QCheckBox')
        else:
            self.setWindowTitle('')

    def showbutton(self):
        self.col = QColor(0, 0, 0)

        redb = QPushButton('Red', self)
        redb.setCheckable(True)
        redb.move(10, 10)

        redb.clicked[bool].connect(self.setColor)

        greenb = QPushButton('Green', self)
        greenb.setCheckable(True)
        greenb.move(10, 60)

        greenb.clicked[bool].connect(self.setColor)

        blueb = QPushButton('Blue', self)
        blueb.setCheckable(True)
        blueb.move(10, 110)

        blueb.clicked[bool].connect(self.setColor)

        self.square = QFrame(self)
        self.square.setGeometry(150, 20, 100, 100)
        self.square.setStyleSheet("QWidget { background-color: %s }" %self.col.name())

        self.setWindowTitle('Toggle button')

    def setColor(self, pressed):

        source = self.sender()

        if pressed:
            val = 255
        else: val = 0

        if source.text() == "Red":
            self.col.setRed(val)
        elif source.text() == "Green":
            self.col.setGreen(val)
        else:
            self.col.setBlue(val)

        self.square.setStyleSheet("QFrame { background-color: %s }" %self.col.name())

    def showslider(self):
        sld = QSlider(Qt.Horizontal, self)
        sld.setFocusPolicy(Qt.NoFocus)
        sld.setGeometry(30, 40, 100, 30)
        sld.valueChanged[int].connect(self.sliderchangevalue)

        self.font = QFont()
        self.font.setPointSize(10)
        self.label = QLabel(self)
        #self.label.setPixmap(QPixmap('audio.icon'))
        self.label.setText('Label')
        self.label.setFont(self.font)
        self.label.setGeometry(160, 40, 80, 30)
        self.setWindowTitle('QSlider')

    def sliderchangevalue(self, value):
        self.font.setPointSize(value)
        self.label.setFont(self.font)

    def showprogress(self):
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)

        self.btn = QPushButton('Start', self)
        self.btn.move(40, 80)
        self.btn.clicked.connect(self.doAction)

        self.timer = QBasicTimer()
        self.step = 0
        self.setWindowTitle('QProgressBar')

    def timerEvent(self, e):
        if self.step >= 100:
            self.timer.stop()
            self.btn.text('Finished')
            return

        self.step += 1
        self.pbar.setValue(self.step)

    def doAction(self):
        if self.timer.isActive():
            self.timer.stop()
            self.btn.setText('Start')
        else:
            self.timer.start(100, self)
            self.btn.setText('Stop')

    def showcalendar(self):
        cal = QCalendarWidget(self)
        cal.setGridVisible(True)
        cal.move(20, 20)
        cal.clicked[QDate].connect(self.showDate)

        self.lbl = QLabel(self)
        date = cal.selectedDate()
        self.lbl.setText(date.toString())
        self.lbl.move(130, 260)

        self.setWindowTitle('Calendar')

    def showDate(self, date):
        self.lbl.setText(date.toString())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())