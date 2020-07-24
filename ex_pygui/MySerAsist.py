# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MySerAsist.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(817, 717)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 0, 811, 661))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.ser_databit = QtWidgets.QComboBox(self.layoutWidget)
        self.ser_databit.setObjectName("ser_databit")
        self.gridLayout.addWidget(self.ser_databit, 5, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 6, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.layoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 7, 0, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 6, 2, 1, 4)
        self.ser_refresh = QtWidgets.QPushButton(self.layoutWidget)
        self.ser_refresh.setObjectName("ser_refresh")
        self.gridLayout.addWidget(self.ser_refresh, 1, 3, 1, 1)
        self.ser_stopbit = QtWidgets.QComboBox(self.layoutWidget)
        self.ser_stopbit.setObjectName("ser_stopbit")
        self.gridLayout.addWidget(self.ser_stopbit, 6, 1, 1, 1)
        self.ser_sendtimer = QtWidgets.QCheckBox(self.layoutWidget)
        self.ser_sendtimer.setObjectName("ser_sendtimer")
        self.gridLayout.addWidget(self.ser_sendtimer, 4, 2, 1, 1)
        self.ser_checkbit = QtWidgets.QComboBox(self.layoutWidget)
        self.ser_checkbit.setObjectName("ser_checkbit")
        self.gridLayout.addWidget(self.ser_checkbit, 7, 1, 1, 1)
        self.ser_hex_display = QtWidgets.QCheckBox(self.layoutWidget)
        self.ser_hex_display.setObjectName("ser_hex_display")
        self.gridLayout.addWidget(self.ser_hex_display, 1, 4, 1, 2)
        self.label_7 = QtWidgets.QLabel(self.layoutWidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 5, 2, 1, 4)
        self.ser_num = QtWidgets.QComboBox(self.layoutWidget)
        self.ser_num.setObjectName("ser_num")
        self.gridLayout.addWidget(self.ser_num, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.layoutWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 4, 4, 1, 1)
        self.ser_clearbtn = QtWidgets.QPushButton(self.layoutWidget)
        self.ser_clearbtn.setObjectName("ser_clearbtn")
        self.gridLayout.addWidget(self.ser_clearbtn, 1, 6, 1, 1)
        self.textEdit = QtWidgets.QTextEdit(self.layoutWidget)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 7)
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.ser_file_select = QtWidgets.QLineEdit(self.layoutWidget)
        self.ser_file_select.setObjectName("ser_file_select")
        self.gridLayout.addWidget(self.ser_file_select, 11, 0, 1, 6)
        self.set_openbtn = QtWidgets.QPushButton(self.layoutWidget)
        self.set_openbtn.setObjectName("set_openbtn")
        self.gridLayout.addWidget(self.set_openbtn, 1, 2, 1, 1)
        self.ser_sendtmr_time = QtWidgets.QLineEdit(self.layoutWidget)
        self.ser_sendtmr_time.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ser_sendtmr_time.sizePolicy().hasHeightForWidth())
        self.ser_sendtmr_time.setSizePolicy(sizePolicy)
        self.ser_sendtmr_time.setObjectName("ser_sendtmr_time")
        self.gridLayout.addWidget(self.ser_sendtmr_time, 4, 3, 1, 1)
        self.ser_bdrate = QtWidgets.QComboBox(self.layoutWidget)
        self.ser_bdrate.setObjectName("ser_bdrate")
        self.gridLayout.addWidget(self.ser_bdrate, 4, 1, 1, 1)
        self.ser_sendhex = QtWidgets.QCheckBox(self.layoutWidget)
        self.ser_sendhex.setObjectName("ser_sendhex")
        self.gridLayout.addWidget(self.ser_sendhex, 7, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 5, 0, 1, 1)
        self.ser_send_filebtn = QtWidgets.QPushButton(self.layoutWidget)
        self.ser_send_filebtn.setObjectName("ser_send_filebtn")
        self.gridLayout.addWidget(self.ser_send_filebtn, 10, 6, 1, 1)
        self.ser_rw_combo = QtWidgets.QComboBox(self.layoutWidget)
        self.ser_rw_combo.setObjectName("ser_rw_combo")
        self.gridLayout.addWidget(self.ser_rw_combo, 10, 5, 1, 1)
        self.ser_rw_checkbox = QtWidgets.QCheckBox(self.layoutWidget)
        self.ser_rw_checkbox.setObjectName("ser_rw_checkbox")
        self.gridLayout.addWidget(self.ser_rw_checkbox, 10, 0, 1, 1)
        self.ser_file_select_btn = QtWidgets.QPushButton(self.layoutWidget)
        self.ser_file_select_btn.setObjectName("ser_file_select_btn")
        self.gridLayout.addWidget(self.ser_file_select_btn, 11, 6, 1, 1)
        self.ser_sendbtn = QtWidgets.QPushButton(self.layoutWidget)
        self.ser_sendbtn.setObjectName("ser_sendbtn")
        self.gridLayout.addWidget(self.ser_sendbtn, 6, 6, 1, 1)
        self.send_with_enter = QtWidgets.QCheckBox(self.layoutWidget)
        self.send_with_enter.setObjectName("send_with_enter")
        self.gridLayout.addWidget(self.send_with_enter, 4, 5, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 817, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_4.setText(_translate("MainWindow", "停止位"))
        self.label_5.setText(_translate("MainWindow", "校验位"))
        self.ser_refresh.setText(_translate("MainWindow", "刷新串口"))
        self.ser_sendtimer.setText(_translate("MainWindow", "定时发送"))
        self.ser_hex_display.setText(_translate("MainWindow", "Hex显示"))
        self.label_7.setText(_translate("MainWindow", "字符串输入框"))
        self.label_2.setText(_translate("MainWindow", "波特率"))
        self.label_6.setText(_translate("MainWindow", "ms/次"))
        self.ser_clearbtn.setText(_translate("MainWindow", "清除窗口"))
        self.label.setText(_translate("MainWindow", "串口号"))
        self.set_openbtn.setText(_translate("MainWindow", "打开串口"))
        self.ser_sendhex.setText(_translate("MainWindow", "Hex发送"))
        self.label_3.setText(_translate("MainWindow", "数据位"))
        self.ser_send_filebtn.setText(_translate("MainWindow", "发送文件"))
        self.ser_rw_checkbox.setText(_translate("MainWindow", "选中读写文件"))
        self.ser_file_select_btn.setText(_translate("MainWindow", "..."))
        self.ser_sendbtn.setText(_translate("MainWindow", "发送"))
        self.send_with_enter.setText(_translate("MainWindow", "加回车换行"))
