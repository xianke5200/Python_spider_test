# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'segger_jlink.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFrame, QMainWindow, QStatusBar, QFileDialog, QMessageBox

core_type = ["Cortex-M0",
        "Cortex-M1",
        "Cortex-M3",
        "Cortex-M4",
        "Cortex-M7",
        "Cortex-M0+"]

class Segger_Dialog(object):
    def __init__(self):
        self.jlinkarm_path = 0
        self.rtt_start_addr = 0
        self.program_path = 0
        self.program_addr = 0
        self.core_type = 0

    def setupUi(self, frame, width):
        """
            Jlink/CMSIS-DAP SEGGER RTT打印调试，数据发送，烧录
        """
        # 第4个布局
        main_frame4 = QMainWindow()
        frame4_bar = QStatusBar()
        frame4_bar.setObjectName("frame4_bar")
        main_frame4.setStatusBar(frame4_bar)
        frame4_bar.showMessage("欢迎进入segger工具")

        self.segger_frame = QFrame(main_frame4)
        self.segger_frame.setGeometry(0, 0, width, frame.height() - 25)
        self.segger_frame.setFrameShape(QFrame.Panel)
        self.segger_frame.setFrameShadow(QFrame.Raised)

        self.frame = frame

        self.gridLayout = QtWidgets.QGridLayout(self.segger_frame)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.segger_rttmap_tbtn = QtWidgets.QToolButton(self.segger_frame)
        self.segger_rttmap_tbtn.setObjectName("segger_rttmap_tbtn")
        self.segger_rttmap_tbtn.setEnabled(False)
        self.gridLayout.addWidget(self.segger_rttmap_tbtn, 4, 6, 1, 1)
        self.segger_rttmap_tbtn.clicked.connect(self.segger_rttmap_tbtn_clicked)
        self.label = QtWidgets.QLabel(self.segger_frame)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.segger_frame)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 4, 2, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.segger_frame)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 4, 4, 1, 2)
        self.segger_mcu_combox = QtWidgets.QComboBox(self.segger_frame)
        self.segger_mcu_combox.setObjectName("segger_mcu_combox")
        self.gridLayout.addWidget(self.segger_mcu_combox, 4, 3, 1, 1)
        self.segger_jlinkarm_tbtn = QtWidgets.QToolButton(self.segger_frame)
        self.segger_jlinkarm_tbtn.setObjectName("segger_jlinkarm_tbtn")
        self.gridLayout.addWidget(self.segger_jlinkarm_tbtn, 4, 2, 1, 1)
        self.segger_jlinkarm_tbtn.clicked.connect(self.segger_jlinkarm_tbtn_clicked)
        self.label_4 = QtWidgets.QLabel(self.segger_frame)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 8, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.segger_frame)
        self.label_5.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_5.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 8, 1, 1, 1)
        self.segger_rttmap_rbtn = QtWidgets.QRadioButton(self.segger_frame)
        self.segger_rttmap_rbtn.setObjectName("segger_rttmap_rbtn")
        self.gridLayout.addWidget(self.segger_rttmap_rbtn, 2, 5, 2, 1)
        self.segger_rttmap_rbtn.toggled.connect(self.segger_rttmap_rbtn_clicked)
        self.segger_jlinkarm_line = QtWidgets.QLineEdit(self.segger_frame)
        self.segger_jlinkarm_line.setObjectName("segger_jlinkarm_line")
        self.gridLayout.addWidget(self.segger_jlinkarm_line, 4, 0, 1, 2)
        self.label_3 = QtWidgets.QLabel(self.segger_frame)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 5, 0, 1, 1)
        self.segger_send_data_line = QtWidgets.QLineEdit(self.segger_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.segger_send_data_line.sizePolicy().hasHeightForWidth())
        self.segger_send_data_line.setSizePolicy(sizePolicy)
        self.segger_send_data_line.setObjectName("segger_send_data_line")
        self.gridLayout.addWidget(self.segger_send_data_line, 6, 0, 2, 7)
        self.program_addr_line = QtWidgets.QLineEdit(self.segger_frame)
        self.program_addr_line.setObjectName("program_addr_line")
        self.gridLayout.addWidget(self.program_addr_line, 8, 2, 1, 5)
        self.segger_program_line = QtWidgets.QLineEdit(self.segger_frame)
        self.segger_program_line.setObjectName("segger_program_line")
        self.gridLayout.addWidget(self.segger_program_line, 9, 0, 1, 6)
        self.program_file_tbtn = QtWidgets.QToolButton(self.segger_frame)
        self.program_file_tbtn.setObjectName("program_file_tbtn")
        self.gridLayout.addWidget(self.program_file_tbtn, 9, 6, 1, 1)
        self.program_file_tbtn.clicked.connect(self.program_file_tbtn_clicked)
        self.segger_clear_btn = QtWidgets.QPushButton(self.segger_frame)
        self.segger_clear_btn.setObjectName("segger_clear_btn")
        self.gridLayout.addWidget(self.segger_clear_btn, 6, 7, 1, 1)
        self.segger_clear_btn.clicked.connect(self.segger_clear_btn_clicked)
        self.segger_link_btn = QtWidgets.QPushButton(self.segger_frame)
        self.segger_link_btn.setObjectName("segger_link_btn")
        self.gridLayout.addWidget(self.segger_link_btn, 4, 7, 1, 1)
        self.segger_link_btn.clicked.connect(self.segger_link_btn_clicked)
        self.segger_send_btn = QtWidgets.QPushButton(self.segger_frame)
        self.segger_send_btn.setObjectName("segger_send_btn")
        self.gridLayout.addWidget(self.segger_send_btn, 8, 7, 1, 1)
        self.segger_send_btn.clicked.connect(self.segger_send_btn_clicked)
        self.segger_program_btn = QtWidgets.QPushButton(self.segger_frame)
        self.segger_program_btn.setObjectName("segger_program_btn")
        self.gridLayout.addWidget(self.segger_program_btn, 9, 7, 1, 1)
        self.segger_program_btn.clicked.connect(self.segger_program_btn_clicked)
        self.segger_hexsend_check = QtWidgets.QCheckBox(self.segger_frame)
        self.segger_hexsend_check.setObjectName("segger_hexsend_check")
        self.gridLayout.addWidget(self.segger_hexsend_check, 8, 8, 1, 1)
        self.segger_hexsend_check.stateChanged.connect(self.segger_hexsend_check_checked)
        self.segger_hexdisp_check = QtWidgets.QCheckBox(self.segger_frame)
        self.segger_hexdisp_check.setObjectName("segger_hexdisp_check")
        self.gridLayout.addWidget(self.segger_hexdisp_check, 6, 8, 1, 1)
        self.segger_hexdisp_check.stateChanged.connect(self.segger_hexdisp_check_checked)
        self.segger_wave_check = QtWidgets.QCheckBox(self.segger_frame)
        self.segger_wave_check.setObjectName("segger_wave_check")
        self.gridLayout.addWidget(self.segger_wave_check, 4, 8, 1, 1)
        self.segger_wave_check.stateChanged.connect(self.segger_wave_check_checked)
        self.segger_disp_text = QtWidgets.QTextEdit(self.segger_frame)
        self.segger_disp_text.setLineWrapColumnOrWidth(0)
        self.segger_disp_text.setObjectName("segger_disp_text")
        self.gridLayout.addWidget(self.segger_disp_text, 0, 0, 1, 9)

        self.retranslateUi()

        frame4_bar_frame = QFrame(main_frame4)
        frame4_bar_frame.setGeometry(0, frame.height(), width, 25)

        return main_frame4, self.segger_frame

    def segger_settint_file_check(self):
        with open("setting.ini", 'a+') as f:
            f.seek(0)
            data = f.readline()
            while data:
                if 'JLINKARM_PATH' in data:
                    self.jlinkarm_path = f.readline()
                    self.segger_jlinkarm_line.setText(self.jlinkarm_path)
                    # print(self.jlinkarm_path)
                if 'RTT_ADDR' in data:
                    self.rtt_start_addr = int(f.readline(), 16)
                    self.lineEdit_2.setText('0x%x' %(self.rtt_start_addr))
                    # print(self.rtt_start_addr)
                if '[PROGRAM_PATH]' in data:
                    self.program_path = f.readline()
                    self.segger_program_line.setText(self.program_path)
                    # print(self.rtt_start_addr)
                if '[PROGRAM_ADDR]' in data:
                    self.program_addr = int(f.readline(), 16)
                    self.program_addr_line.setText('0x%x' %(self.program_addr))
                    # print(self.rtt_start_addr)
                data = f.readline()

        for i in range(len(core_type)):
            self.segger_mcu_combox.addItem(core_type[i])

        self.core_type = self.segger_mcu_combox.currentText()

    def segger_setting_file_update(self):
        with open("setting.ini", 'w+') as f:
            f.write('[JLINKARM_PATH]\r\n')
            f.write(self.jlinkarm_path+'\r\n')
            f.write('\r\n')
            f.write('[RTT_ADDR]\r\n')
            f.write('0x%x\r\n' %(self.rtt_start_addr))
            f.write('\r\n')
            f.write('[PROGRAM_PATH]\r\n')
            f.write(self.program_path + '\r\n')
            f.write('\r\n')
            f.write('[PROGRAM_ADDR]\r\n')
            f.write('0x%x\r\n' %(self.program_addr))

    def retranslateUi(self):
        self.segger_rttmap_tbtn.setText("...")
        self.label.setText("jlinkARM.dll路径:")
        self.label_2.setText("RTT LOG地址:")
        self.segger_jlinkarm_tbtn.setText("...")
        self.label_4.setText("烧录文件路径:")
        self.label_5.setText("烧录地址:")
        self.segger_rttmap_rbtn.setText(".map路径")
        self.label_3.setText("填入发送数据:")
        self.program_file_tbtn.setText("...")
        self.segger_clear_btn.setText("清空显示")
        self.segger_link_btn.setText("连接")
        self.segger_send_btn.setText("发送")
        self.segger_program_btn.setText("烧录")
        self.segger_hexsend_check.setText("Hex发送")
        self.segger_hexdisp_check.setText("Hex显示")
        self.segger_wave_check.setText("波形显示")

    def segger_jlinkarm_tbtn_clicked(self):
        """
            点击选择JlinkARM.dll的文件路径
        """
        self.jlinkarm_path, ok1 = QFileDialog.getOpenFileName(self.frame,
                                                "文件选择",
                                                "./",
                                                "All Files (*);;dll Files (.dll)")
        if ok1:
            self.segger_jlinkarm_line.setText(self.jlinkarm_path)

    def segger_rttmap_tbtn_clicked(self):
        """
            点击选择.map的文件路径
        """
        file, ok1 = QFileDialog.getOpenFileName(self.frame,
                                                              "文件选择",
                                                              "./",
                                                              "All Files (*);;dll Files (.map)")
        if ok1:
            with open(file, 'r+') as f:
                data = f.readline()
                while data:
                    if 'segger_rtt.o' in data and '.bss' in data:
                        linedata = data.split(' ')
                        addr = 0
                        for i in range(len(linedata)):
                            if not linedata[i]:
                                continue
                            else:
                                addr = linedata[i]
                                break
                        try:
                            self.rtt_start_addr = int(addr, 16)
                        except:
                            data = f.readline()
                            continue
                        else:
                            self.lineEdit_2.setText('0x%x' %(self.rtt_start_addr))
                    data = f.readline()

    def segger_rttmap_rbtn_clicked(self):
        if self.segger_rttmap_rbtn.isChecked():
            self.segger_rttmap_tbtn.setEnabled(True)
        else:
            self.segger_rttmap_tbtn.setEnabled(False)

    def segger_link_btn_clicked(self):
        self.core_type = self.segger_mcu_combox.currentText()

    def segger_clear_btn_clicked(self):
        self.segger_disp_text.clear()

    def segger_send_btn_clicked(self):
        linedata = self.segger_send_data_line.text()

    def program_file_tbtn_clicked(self):
        """
            点击选择需要烧录的文件路径
        """
        self.program_path, ok1 = QFileDialog.getOpenFileName(self.frame,
                                                              "文件选择",
                                                              "./",
                                                              "All Files (*);;dll Files (.bin);;dll Files (.hex)")
        if ok1:
            self.segger_program_line.setText(self.program_path)

    def segger_program_btn_clicked(self):
        try:
            self.program_addr = int(self.program_addr_line.text(), 16)
            program_file = open(self.program_path, 'r')
            self.core_type = self.segger_mcu_combox.currentText()
        except:
            QMessageBox.warning(self.frame, '警告', '烧录参数错误')

    def segger_wave_check_checked(self):
        return

    def segger_hexdisp_check_checked(self):
        return

    def segger_hexsend_check_checked(self):
        return