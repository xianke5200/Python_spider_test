# -*- coding: utf-8 -*-

"""
PyQt5 little_tool

In this software, Include excel merge and serial

author: chenlue
last edited: 2020年7月
"""
import os

from PyQt5 import QtGui
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import  QButtonGroup, QFrame, QToolButton, QStackedLayout, \
     QDesktopWidget, QMessageBox, QMenu, QAction, \
     QDialog
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt

import time

import sys

from ex_pygui.little_tool.file_sqlite_copy import excel_window
from time_display import Ui_Dialog  # 显示自定义的弹出窗口
from segger_jlink import Segger_Dialog
from pic_to_bin import picbin_window
from MySerAsist import Serial_window

import binascii

Tool_dict = {
    'file_sqlite_define' : 0,
    'serial_define' : 1,
    'picbin_define' : 2,
    'segger_define' : 3
}

class Little_tool(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("小工具-CL-V1.00")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("my.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        # 窗口大小
        self.resize(800, 600)
        # self.setFixedSize(800, 600)  # 设置窗口为固定尺寸， 此时窗口不可调整大小
        # self.setMinimumSize(1800， 1000)  # 设置窗口最大尺寸
        # self.setMaximumSize(900， 300)  # 设置窗口最小尺寸
        # self.setWindowFlag(Qt.WindowStaysOnTopHint)   # 设置窗口顶层显示
        # self.setWindowFlags(Qt.FramelessWindowHint)  # 设置无边框窗口样式，不显示最上面的标题栏

        self.content_font = QFont("微软雅黑", 12, QFont.Medium)  # 定义字体样式

        self.excel_display = excel_window()
        self.Serial_display = Serial_window()
        self.picbin_display = picbin_window()
        self.segger_display = Segger_Dialog()

        self.center()

        self.__setup_ui__()

    # 控制窗口显示在屏幕中心的方法


    def center(self):
        # 获得窗口
        qr = self.frameGeometry()
        # 获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        # 显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    # 关闭窗口的时候,触发了QCloseEvent，需要重写closeEvent()事件处理程序，这样就可以弹出是否退出的确认窗口
    def closeEvent(self, event):
        reply = QMessageBox.question(self, "退出程序",  # 提示框标题
                                     "确定退出程序吗？",  # 消息对话框中显示的文本
                                     QMessageBox.Yes | QMessageBox.No,  # 指定按钮的组合 Yes和No
                                     QMessageBox.No  # 默认的按钮焦点,这里默认是No按钮
                                     )
        # 判断按钮的选择
        if reply == QMessageBox.Yes:
            self.excel_display.window_clear()
            try:
                self.Serial_display.window_clear()
            except:
                return
            self.segger_display.segger_setting_file_update()

            event.accept()
        else:
            event.ignore()

    def resizeEvent(self, e: QtGui.QResizeEvent):
        # print('%d, %d', e.size().width(), e.size().height())

        self.frame_tool.resize(e.size().width(), 25)
        self.main_frame.resize(e.size().width(), e.size().height() - 25)

        # 窗口1 大小跟随主窗口
        if 'file_sqlite_define' in Tool_dict:
            self.rom_frame.resize(e.size().width(), e.size().height() - 50)
            self.start_btn.setGeometry(e.size().width() * 0.3, e.size().height() * 0.8, 100, 40)
            self.quit_btn.setGeometry(e.size().width() * 0.6, e.size().height() * 0.8, 100, 40)
        # 窗口2 大小跟随主窗口
        if 'serial_define' in Tool_dict:
            self.custom_frame.resize(e.size().width(), e.size().height()-50)
        # 窗口3 大小跟随主窗口
        if 'picbin_define' in Tool_dict:
            self.picbin_frame.resize(e.size().width(), e.size().height() - 50)
        # 窗口4 大小跟随主窗口
        if 'picbin_define' in Tool_dict:
            self.segger_frame.resize(e.size().width(), e.size().height() - 50)

    # def keyPressEvent(self, a0: QtGui.QKeyEvent):
    #     self.textEdit.keyPressEvent(a0)
    #     if a0.type() == a0.KeyPress:
    #         print('key press')

    def __setup_ui__(self):
        # 工具栏
        self.frame_tool = QFrame(self)
        self.frame_tool.setObjectName("frame_tool")
        self.frame_tool.setGeometry(0, 0, self.width(), 25)
        self.frame_tool.setStyleSheet("border-color: rgb(0, 0, 0);")
        self.frame_tool.setFrameShape(QFrame.Panel)
        self.frame_tool.setFrameShadow(QFrame.Raised)

        self.btn_group = QButtonGroup(self.frame_tool)

        # 2. 工作区域
        self.main_frame = QFrame(self)
        self.main_frame.setGeometry(0, 25, self.width(), self.height() - self.frame_tool.height())
        # self.main_frame.setStyleSheet("background-color: rgb(65, 95, 255)")

        # 创建堆叠布局
        self.stacked_layout = QStackedLayout(self.main_frame)
        # self.setLayout(self.stacked_layout)

        help_btn_start_x = 0

        if 'file_sqlite_define' in Tool_dict:
            # 1.1 界面1按钮
            self.window1_btn = QToolButton(self.frame_tool)
            self.window1_btn.setCheckable(True)
            self.window1_btn.setText("固件标题修正")
            self.window1_btn.setObjectName("menu_btn")
            self.window1_btn.resize(100, 25)
            self.window1_btn.clicked.connect(lambda: self.click_window(Tool_dict['file_sqlite_define']))
            self.window1_btn.setAutoRaise(True)  # 去掉工具按钮的边框线如果是QPushButton按钮的话，就是用setFlat(True)这个方法，用法相同
            self.btn_group.addButton(self.window1_btn, 1)
            help_btn_start_x += self.window1_btn.width()
            main_frame1, self.rom_frame, self.start_btn, self.quit_btn = self.excel_display.setupUi(self.main_frame,
                                                                                                    self.width(),
                                                                                                    self.height(), self)
            self.stacked_layout.addWidget(main_frame1)

        if 'serial_define' in Tool_dict:
            # 1.2 界面2按钮
            self.window2_btn = QToolButton(self.frame_tool)
            self.window2_btn.setCheckable(True)
            self.window2_btn.setText("串口小工具")
            self.window2_btn.setObjectName("menu_btn")
            self.window2_btn.resize(100, 25)
            self.window2_btn.move(help_btn_start_x, 0)
            self.window2_btn.clicked.connect(lambda: self.click_window(Tool_dict['serial_define']))
            self.window2_btn.setAutoRaise(True)
            self.btn_group.addButton(self.window2_btn, 2)
            help_btn_start_x += self.window2_btn.width()
            main_frame2, self.custom_frame = self.Serial_display.setupUi(self.main_frame, self.width())
            self.stacked_layout.addWidget(main_frame2)
            self.Serial_display.serial_update()

        if 'picbin_define' in Tool_dict:
            # 1.3 界面3按钮
            self.window3_btn = QToolButton(self.frame_tool)
            self.window3_btn.setCheckable(True)
            self.window3_btn.setText("图片转换")
            self.window3_btn.setObjectName("menu_btn")
            self.window3_btn.resize(100, 25)
            self.window3_btn.move(help_btn_start_x, 0)
            self.window3_btn.clicked.connect(lambda : self.click_window(Tool_dict['picbin_define']))
            self.window3_btn.setAutoRaise(True)
            self.btn_group.addButton(self.window3_btn, 3)
            help_btn_start_x += self.window3_btn.width()
            main_frame3, self.picbin_frame = self.picbin_display.setupUi(self.main_frame, self.width())
            self.stacked_layout.addWidget(main_frame3)

        if 'segger_define' in Tool_dict:
            # 1.4 界面4按钮
            self.window4_btn = QToolButton(self.frame_tool)
            self.window4_btn.setCheckable(True)
            self.window4_btn.setText("Segger工具")
            self.window4_btn.setObjectName("menu_btn")
            self.window4_btn.resize(100, 25)
            self.window4_btn.move(help_btn_start_x, 0)
            self.window4_btn.clicked.connect(lambda: self.click_window(Tool_dict['segger_define']))
            self.window4_btn.setAutoRaise(True)
            self.btn_group.addButton(self.window4_btn, 4)
            help_btn_start_x += self.window4_btn.width()
            main_frame4, self.segger_frame = self.segger_display.setupUi(self.main_frame, self.width())
            self.stacked_layout.addWidget(main_frame4)
            self.segger_display.segger_settint_file_check()

        # 1.5 帮助下拉菜单栏
        # 创建帮助工具按钮
        help_btn = QToolButton(self.frame_tool)
        help_btn.setText("帮助")
        help_btn.setObjectName("menu_btn")
        help_btn.resize(100, 25)
        help_btn.move(help_btn_start_x, 0)
        help_btn.setAutoRaise(True)
        help_btn.setPopupMode(QToolButton.InstantPopup)
        # 创建关于菜单
        help_menu = QMenu("帮助", self.frame_tool)
        feedback_action = QAction(QIcon("xxx.png"), "反馈", help_menu)
        feedback_action.triggered.connect(self.click_feedback)
        about_action = QAction(QIcon("xxx.png"), "关于", help_menu)
        about_action.triggered.connect(self.click_about)
        # 把两个QAction放入help_menu
        help_menu.addAction(feedback_action)
        help_menu.addAction(about_action)
        # 把help_menu放入help_btn
        help_btn.setMenu(help_menu)

        # self.layout = QBoxLayout(QBoxLayout.BottomToTop)
        # self.layout_test = QBoxLayout(QBoxLayout.LeftToRight)
        # self.frame_tool.setLayout(self.layout)
        # #self.layout.addWidget(self.frame_tool)
        # # self.layout.addWidget(self.main_frame)
        # self.layout_test.addWidget(self.window1_btn)
        # self.layout_test.addWidget(self.window2_btn)
        # self.layout_test.addWidget(help_btn)
        # self.layout.addLayout(self.layout_test)
        # self.layout.addLayout(self.stacked_layout)

    def click_window(self, arg):
        if self.stacked_layout.currentIndex() != arg:
            self.stacked_layout.setCurrentIndex(arg)
            # self.frame1_bar.showMessage("欢迎使用")
            self.Serial_display.serial_update()
            self.segger_display.segger_settint_file_check()


    def click_feedback(self, event):
        QMessageBox.about(self, "反馈", "抱歉无法反馈")

    def click_about(self, event):
        # QMessageBox.about(self, "关于", "抱歉，没有文档")
        self.di = QDialog()
        timedisplay = Ui_Dialog()
        timedisplay.setupUi(self.di)
        now = time.localtime()
        timedisplay.label.setText('%02d:%02d:%02d' %(now.tm_hour, now.tm_min, now.tm_sec))
        timedisplay.pushButton.clicked.connect(self.di.close)
        self.di.setWindowModality(Qt.ApplicationModal) #锁定子窗口，关闭子窗口后才可以操作父窗口

        self.di.show()

        abot_timer = QTimer(self.di)
        abot_timer.timeout.connect(lambda :timedisplay.label.setText('%02d:%02d:%02d' %(time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)))
        abot_timer.start(1000)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Little_tool()
    window.show()
    sys.exit(app.exec_())