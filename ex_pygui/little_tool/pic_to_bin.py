# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pic_to_bin.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 633)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(40, 20, 711, 541))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.tableWidget_bin_file = QtWidgets.QTableWidget(self.widget)
        self.tableWidget_bin_file.setObjectName("tableWidget_bin_file")
        self.tableWidget_bin_file.setColumnCount(0)
        self.tableWidget_bin_file.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget_bin_file, 3, 0, 1, 8)
        self.bin_dir_btn = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bin_dir_btn.sizePolicy().hasHeightForWidth())
        self.bin_dir_btn.setSizePolicy(sizePolicy)
        self.bin_dir_btn.setObjectName("bin_dir_btn")
        self.gridLayout.addWidget(self.bin_dir_btn, 2, 7, 1, 1)
        self.start_btn = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.start_btn.sizePolicy().hasHeightForWidth())
        self.start_btn.setSizePolicy(sizePolicy)
        self.start_btn.setObjectName("start_btn")
        self.gridLayout.addWidget(self.start_btn, 6, 7, 1, 1)
        self.pic_dir_btn = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pic_dir_btn.sizePolicy().hasHeightForWidth())
        self.pic_dir_btn.setSizePolicy(sizePolicy)
        self.pic_dir_btn.setObjectName("pic_dir_btn")
        self.gridLayout.addWidget(self.pic_dir_btn, 0, 7, 1, 1)
        self.tableWidget_pic_file = QtWidgets.QTableWidget(self.widget)
        self.tableWidget_pic_file.setObjectName("tableWidget_pic_file")
        self.tableWidget_pic_file.setColumnCount(0)
        self.tableWidget_pic_file.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget_pic_file, 1, 0, 1, 8)
        self.checkBox_flash = QtWidgets.QCheckBox(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_flash.sizePolicy().hasHeightForWidth())
        self.checkBox_flash.setSizePolicy(sizePolicy)
        self.checkBox_flash.setObjectName("checkBox_flash")
        self.gridLayout.addWidget(self.checkBox_flash, 6, 0, 1, 1)
        self.checkBox_alpha = QtWidgets.QCheckBox(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_alpha.sizePolicy().hasHeightForWidth())
        self.checkBox_alpha.setSizePolicy(sizePolicy)
        self.checkBox_alpha.setObjectName("checkBox_alpha")
        self.gridLayout.addWidget(self.checkBox_alpha, 6, 1, 1, 1)
        self.refresh_btn = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refresh_btn.sizePolicy().hasHeightForWidth())
        self.refresh_btn.setSizePolicy(sizePolicy)
        self.refresh_btn.setObjectName("refresh_btn")
        self.gridLayout.addWidget(self.refresh_btn, 6, 2, 1, 1)
        self.lineEdit_bin_dir = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_bin_dir.setObjectName("lineEdit_bin_dir")
        self.gridLayout.addWidget(self.lineEdit_bin_dir, 2, 0, 1, 7)
        self.lineEdit_pic_dir = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_pic_dir.setObjectName("lineEdit_pic_dir")
        self.gridLayout.addWidget(self.lineEdit_pic_dir, 0, 0, 1, 7)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
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
        self.bin_dir_btn.setText(_translate("MainWindow", "bin文件夹"))
        self.start_btn.setText(_translate("MainWindow", "开始"))
        self.pic_dir_btn.setText(_translate("MainWindow", "文件夹..."))
        self.checkBox_flash.setText(_translate("MainWindow", "外部flash"))
        self.checkBox_alpha.setText(_translate("MainWindow", "透明度"))
        self.refresh_btn.setText(_translate("MainWindow", "刷新"))