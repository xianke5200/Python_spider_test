# -*- coding: utf-8 -*-

"""
PyQt5 little_tool

In this software, Include excel merge and serial

author: chenlue
last edited: 2020年7月
"""
import os

import xlrd
import xlwt
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QButtonGroup, QFrame, QToolButton, QStackedLayout, \
    QWidget, QStatusBar, QBoxLayout, QLabel, QDesktopWidget, QMessageBox, QMenu, QAction, QFileDialog, QLineEdit, \
    QGridLayout, QComboBox, QDialog, QProgressBar
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QIcon, QTextCursor, QImage, QPalette, QPixmap, qRgb, qRed, qAlpha, qBlue, qGreen
from PyQt5.QtCore import Qt

from PIL import Image
import time

import serial
import threading

import serial.tools.list_ports

import sys

from excel_db import excel_db
from time_display import Ui_Dialog  # 显示自定义的弹出窗口

import binascii

baudrates = ['110', '300', '600', '1200',
            '2400', '4800', '9600', '14400',
            '19200', '38400', '56000', '57600',
            '115200', '128000', '230400', '256000',
            '460800', '500000', '512000', '600000',
            '750000', '921600', '1000000', '1500000',
            '2000000']
databits = ['5', '6', '7', '8']
stopbits = ['1', '1.5', '2']
checkbits = ['N', 'O', 'E', 'M', 'S']

sr_select = ['', '读取文件', '发送文件']

class Little_tool(QWidget):
    def __init__(self, n = 1):
        super().__init__()

        self.setWindowTitle("测试")
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

        self.language_dict = {}
        self.layout_count = n
        self.layout_list = []
        self.lineedit_list = []
        self.combo_list = []

        self.ed = excel_db() #创建数据库
        self.ed.connect()
        self.ed.create()

        self.filepath_list = []
        self.filename_list = []

        self.filepath_bin_list = []
        self.filename_bin_list = []

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
            #excel window
            self.ed.dbClose()#关闭数据库
            self.ed.dbRemove()#删除数据库文件
            #serial window
            self.sendtmr.stop()
            self.sendfile_tmr.stop()
            # self.ser_thread.stop()
            self.recvtmr.stop()
            self.ser.close()
            try:
                self.sfile.close()
                self.rfile.close()
            except:
                return

            event.accept()
        else:
            event.ignore()

    def resizeEvent(self, e: QtGui.QResizeEvent):
        # print('%d, %d', e.size().width(), e.size().height())
        # 窗口1 大小跟随主窗口
        self.frame_tool.resize(e.size().width(), 25)
        self.main_frame.resize(e.size().width(), e.size().height() - 25)
        self.rom_frame.resize(e.size().width(), e.size().height() - 50)
        # 窗口2 大小跟随主窗口
        self.start_btn.setGeometry(e.size().width() * 0.3, e.size().height() * 0.8, 100, 40)
        self.quit_btn.setGeometry(e.size().width() * 0.6, e.size().height() * 0.8, 100, 40)

        self.custom_frame.resize(e.size().width(), e.size().height()-50)
        self.picbin_frame.resize(e.size().width(), e.size().height() - 50)

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

        # 1.1 界面1按钮
        self.window1_btn = QToolButton(self.frame_tool)
        self.window1_btn.setCheckable(True)
        self.window1_btn.setText("固件标题修正")
        self.window1_btn.setObjectName("menu_btn")
        self.window1_btn.resize(100, 25)
        self.window1_btn.clicked.connect(self.click_window1)
        self.window1_btn.setAutoRaise(True)  # 去掉工具按钮的边框线如果是QPushButton按钮的话，就是用setFlat(True)这个方法，用法相同

        # 1.2 界面2按钮
        self.window2_btn = QToolButton(self.frame_tool)
        self.window2_btn.setCheckable(True)
        self.window2_btn.setText("串口小工具")
        self.window2_btn.setObjectName("menu_btn")
        self.window2_btn.resize(100, 25)
        self.window2_btn.move(self.window1_btn.width(), 0)
        self.window2_btn.clicked.connect(self.click_window2)
        self.window2_btn.setAutoRaise(True)

        # 1.3 界面3按钮
        self.window3_btn = QToolButton(self.frame_tool)
        self.window3_btn.setCheckable(True)
        self.window3_btn.setText("图片转换")
        self.window3_btn.setObjectName("menu_btn")
        self.window3_btn.resize(100, 25)
        self.window3_btn.move(self.window2_btn.x() + self.window2_btn.width(), 0)
        self.window3_btn.clicked.connect(self.click_window3)
        self.window3_btn.setAutoRaise(True)

        self.btn_group = QButtonGroup(self.frame_tool)
        self.btn_group.addButton(self.window1_btn, 1)
        self.btn_group.addButton(self.window2_btn, 2)
        self.btn_group.addButton(self.window3_btn, 3)

        # 1.3 帮助下拉菜单栏
        # 创建帮助工具按钮
        help_btn = QToolButton(self.frame_tool)
        help_btn.setText("帮助")
        help_btn.setObjectName("menu_btn")
        help_btn.resize(100, 25)
        help_btn.move(self.window3_btn.x() + self.window3_btn.width(), 0)
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

        # 2. 工作区域
        self.main_frame = QFrame(self)
        self.main_frame.setGeometry(0, 25, self.width(), self.height() - self.frame_tool.height())
        # self.main_frame.setStyleSheet("background-color: rgb(65, 95, 255)")

        # 创建堆叠布局
        self.stacked_layout = QStackedLayout(self.main_frame)
        #self.setLayout(self.stacked_layout)

        main_frame1 = self.window1_UI(self.main_frame)
        main_frame2 = self.window2_UI(self.main_frame)
        main_frame3 = self.window3_UI(self.main_frame)

        # 把两个布局放进去
        self.stacked_layout.addWidget(main_frame1)
        self.stacked_layout.addWidget(main_frame2)
        self.stacked_layout.addWidget(main_frame3)

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

    def click_window1(self):
        if self.stacked_layout.currentIndex() != 0:
            self.stacked_layout.setCurrentIndex(0)
            #self.frame1_bar.showMessage("欢迎使用")

    def click_window2(self):
        if self.stacked_layout.currentIndex() != 1:
            self.stacked_layout.setCurrentIndex(1)
            self.serial_update()
            #self.frame2_bar.showMessage("欢迎进入frame2")
            #QDesktopServices.openUrl(QUrl("https://www.csdn.net/"))  # 点击window2按钮后，执行这个槽函数的时候，会在浏览器自动打开这个网址

    def click_window3(self):
        if self.stacked_layout.currentIndex() != 2:
            self.stacked_layout.setCurrentIndex(2)

    def click_feedback(self, event):
        QMessageBox.about(self, "反馈", "抱歉无法反馈")

    def click_about(self, event):
        #QMessageBox.about(self, "关于", "抱歉，没有文档")
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

    def window1_UI(self, frame):
        """
            Excel固件列表语言更新程序UI布局
        """
        # 第一个布局
        main_frame1 = QMainWindow()
        frame1_bar = QStatusBar()
        frame1_bar.setObjectName("frame1_bar")
        main_frame1.setStatusBar(frame1_bar)
        frame1_bar.showMessage("欢迎进入")

        self.rom_frame = QFrame(main_frame1)
        self.rom_frame.setGeometry(0, 0, self.width(), frame.height() - 25)
        self.rom_frame.setFrameShape(QFrame.Panel)
        self.rom_frame.setFrameShadow(QFrame.Raised)

        realtime_lable = QLabel(self.rom_frame)
        realtime_lable.setText(
            '%04d/%02d/%02d-%02d:%02d:%02d' % (time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday,
                                               time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec))
        realtime_lable.setGeometry(self.width() - 50, frame.height() - 25, 50, 25)
        frame1_bar.addPermanentWidget(realtime_lable)
        real_timer = QTimer(frame1_bar)
        real_timer.timeout.connect(lambda: realtime_lable.setText(
            '%04d/%02d/%02d-%02d:%02d:%02d' % (time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday,
                                               time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)))
        real_timer.start(500)

        # 创建布局管理器
        self.layout1 = QBoxLayout(QBoxLayout.TopToBottom, self.rom_frame)
        tab_lay = QBoxLayout(QBoxLayout.LeftToRight, self.rom_frame)
        tab_lay1 = QBoxLayout(QBoxLayout.LeftToRight, self.rom_frame)
        # self.tab_lay2 = QBoxLayout(QBoxLayout.LeftToRight)

        output_title = QLabel('dest', self.rom_frame)
        output_title.setGeometry(self.width() * 0.1, self.height() * 0.1, 10, 4)
        self.output_file = QLineEdit(self.rom_frame)
        DirButton = QPushButton(self.rom_frame)
        DirButton.setObjectName('query Button')
        DirButton.setText('...')
        DirButton.setStatusTip('Click to select file')
        DirButton.clicked.connect(lambda x,y=0:self.file_select(x, y))
        addButton = QPushButton(self.rom_frame)
        addButton.resize(5, 2)
        addButton.setObjectName('add Button')
        addButton.setText('+')
        addButton.setStatusTip('Click to add source select')
        addButton.clicked.connect(self.add_file_select)
        self.lineedit_list.append(self.output_file)

        output_title1 = QLabel('src1', self.rom_frame)
        self.output_file1 = QLineEdit(self.rom_frame)
        DirButton1 = QPushButton(self.rom_frame)
        DirButton1.setObjectName('query Button')
        DirButton1.setText('...')
        DirButton1.setStatusTip('Click to select source file')
        DirButton1.clicked.connect(lambda x,y=1:self.file_select(x, y))
        self.combo1 = QComboBox(self.rom_frame)
        self.lineedit_list.append(self.output_file1)
        self.combo_list.append(self.combo1)

        '''
        # 超链接
        self.super_link = QLabel(rom_frame)
        self.super_link.setText("""
            超链接: <a href="https://blog.csdn.net/s_daqing">点击打开查看</a>
            """)
        self.super_link.setGeometry(20, 30, 300, 25)
        self.super_link.setFont(self.content_font)  # 使用字体样式
        self.super_link.setOpenExternalLinks(True)  # 使其成为超链接
        self.super_link.setTextInteractionFlags(Qt.TextBrowserInteraction)  # 双击可以复制文本
        '''
        self.start_btn = QPushButton("开 始", self.rom_frame)
        self.start_btn.setGeometry(self.width() * 0.3, self.height() * 0.85, 100, 40)
        self.start_btn.clicked.connect(self.write_excel_file)
        self.quit_btn = QPushButton("退 出", self.rom_frame)
        self.quit_btn.setGeometry(self.width() * 0.6, self.height() * 0.85, 100, 40)
        self.quit_btn.setStatusTip("点击关闭程序")
        # self.quit_btn.clicked.connect(QCoreApplication.instance().quit)  # 点击退出可以直接退出
        self.quit_btn.clicked.connect(self.close)  # 点击退出按钮的退出槽函数

        tab_lay.addWidget(output_title, 1)
        tab_lay.addWidget(self.output_file, 20)
        tab_lay.addWidget(DirButton, 1)
        tab_lay.addWidget(addButton, 1)

        tab_lay1.addWidget(output_title1, 1)
        tab_lay1.addWidget(self.output_file1, 20)
        tab_lay1.addWidget(DirButton1, 1)
        tab_lay1.addWidget(self.combo1, 1)

        # self.tab_lay2.addStretch(2)
        # self.tab_lay2.addWidget(start_btn, 1)
        # self.tab_lay2.addStretch(2)
        # self.tab_lay2.addWidget(quit_btn, 1)
        # self.tab_lay2.addStretch(2)

        # 给管理器对象设置父控件
        self.rom_frame.setLayout(self.layout1)
        main_frame1.setCentralWidget(self.rom_frame)

        self.layout1.setContentsMargins(0, 0, 0, 0)  # 设置布局的左上右下外边距
        self.layout1.setSpacing(0)  # 设置子控件的内边距

        self.layout_list.append(tab_lay)
        self.layout_list.append(tab_lay1)
        #self.layout_list.append(self.tab_lay2)

        for i in range(len(self.layout_list)):
            self.layout1.addLayout(self.layout_list[i])
        # self.layout1.addStretch(10)  # 设置空间之间的上下间距
        # self.layout1.addLayout(self.tab_lay2)
        self.layout1.addStretch(1)  # 设置空间之间的上下间距

        frame1_bar_frame = QFrame(main_frame1)
        frame1_bar_frame.setGeometry(0, frame.height(), self.width(), 25)

        return main_frame1

    def add_file_select(self):
        """
            添加多个固件语言列表
        """
        self.layout_count += 1
        if(self.layout_count > 8):
            return
        tab_lay_add = QBoxLayout(QBoxLayout.LeftToRight)
        text = 'src%d' % (self.layout_count)

        if self.layout_count == 2:
            output_title2 = QLabel(text, self.rom_frame)
            self.output_file2 = QLineEdit(self.rom_frame)
            DirButton2 = QPushButton(self.rom_frame)
            DirButton2.setObjectName('query Button')
            DirButton2.setText('...')
            DirButton2.setStatusTip('Click to select source file')
            DirButton2.clicked.connect(lambda x,y=2:self.file_select(x, y))
            self.combo2 = QComboBox(self.rom_frame)
            self.lineedit_list.append(self.output_file2)
            self.combo_list.append(self.combo2)

            tab_lay_add.addWidget(output_title2, 1)
            tab_lay_add.addWidget(self.output_file2, 20)
            tab_lay_add.addWidget(DirButton2, 1)
            tab_lay_add.addWidget(self.combo2, 1)
        elif self.layout_count == 3:
            output_title3 = QLabel(text, self.rom_frame)
            self.output_file3 = QLineEdit(self.rom_frame)
            DirButton3 = QPushButton(self.rom_frame)
            DirButton3.setObjectName('query Button')
            DirButton3.setText('...')
            DirButton3.setStatusTip('Click to select source file')
            DirButton3.clicked.connect(lambda x,y=3:self.file_select(x, y))
            self.combo3 = QComboBox(self.rom_frame)
            self.lineedit_list.append(self.output_file3)
            self.combo_list.append(self.combo3)

            tab_lay_add.addWidget(output_title3, 1)
            tab_lay_add.addWidget(self.output_file3, 20)
            tab_lay_add.addWidget(DirButton3, 1)
            tab_lay_add.addWidget(self.combo3, 1)
        elif self.layout_count == 4:
            output_title4 = QLabel(text, self.rom_frame)
            self.output_file4 = QLineEdit(self.rom_frame)
            DirButton4 = QPushButton(self.rom_frame)
            DirButton4.setObjectName('query Button')
            DirButton4.setText('...')
            DirButton4.setStatusTip('Click to select source file')
            DirButton4.clicked.connect(lambda x,y=4:self.file_select(x, y))
            self.combo4 = QComboBox(self.rom_frame)
            self.lineedit_list.append(self.output_file4)
            self.combo_list.append(self.combo4)

            tab_lay_add.addWidget(output_title4, 1)
            tab_lay_add.addWidget(self.output_file4, 20)
            tab_lay_add.addWidget(DirButton4, 1)
            tab_lay_add.addWidget(self.combo4, 1)
        elif self.layout_count == 5:
            output_title5 = QLabel(text, self.rom_frame)
            self.output_file5 = QLineEdit(self.rom_frame)
            DirButton5 = QPushButton(self.rom_frame)
            DirButton5.setObjectName('query Button')
            DirButton5.setText('...')
            DirButton5.setStatusTip('Click to select source file')
            DirButton5.clicked.connect(lambda x,y=5:self.file_select(x, y))
            self.combo5 = QComboBox(self.rom_frame)
            self.lineedit_list.append(self.output_file5)
            self.combo_list.append(self.combo5)

            tab_lay_add.addWidget(output_title5, 1)
            tab_lay_add.addWidget(self.output_file5, 20)
            tab_lay_add.addWidget(DirButton5, 1)
            tab_lay_add.addWidget(self.combo5, 1)
        elif self.layout_count == 6:
            output_title6 = QLabel(text, self.rom_frame)
            self.output_file6 = QLineEdit(self.rom_frame)
            DirButton6 = QPushButton(self.rom_frame)
            DirButton6.setObjectName('query Button')
            DirButton6.setText('...')
            DirButton6.setStatusTip('Click to select source file')
            DirButton6.clicked.connect(lambda x,y=6:self.file_select(x, y))
            self.combo6 = QComboBox(self.rom_frame)
            self.lineedit_list.append(self.output_file6)
            self.combo_list.append(self.combo6)

            tab_lay_add.addWidget(output_title6, 1)
            tab_lay_add.addWidget(self.output_file6, 20)
            tab_lay_add.addWidget(DirButton6, 1)
            tab_lay_add.addWidget(self.combo6, 1)
        elif self.layout_count == 7:
            output_title7 = QLabel(text, self.rom_frame)
            self.output_file7 = QLineEdit(self.rom_frame)
            DirButton7 = QPushButton(self.rom_frame)
            DirButton7.setObjectName('query Button')
            DirButton7.setText('...')
            DirButton7.setStatusTip('Click to select source file')
            DirButton7.clicked.connect(lambda x,y=7:self.file_select(x, y))
            self.combo7 = QComboBox(self.rom_frame)
            self.lineedit_list.append(self.output_file7)
            self.combo_list.append(self.combo7)

            tab_lay_add.addWidget(output_title7, 1)
            tab_lay_add.addWidget(self.output_file7, 20)
            tab_lay_add.addWidget(DirButton7, 1)
            tab_lay_add.addWidget(self.combo7, 1)
        elif self.layout_count == 8:
            output_title8 = QLabel(text, self.rom_frame)
            self.output_file8 = QLineEdit(self.rom_frame)
            DirButton8 = QPushButton(self.rom_frame)
            DirButton8.setObjectName('query Button')
            DirButton8.setText('...')
            DirButton8.setStatusTip('Click to select source file')
            DirButton8.clicked.connect(lambda x,y=8:self.file_select(x, y))
            self.combo8 = QComboBox(self.rom_frame)
            self.lineedit_list.append(self.output_file8)
            self.combo_list.append(self.combo8)

            tab_lay_add.addWidget(output_title8, 1)
            tab_lay_add.addWidget(self.output_file8, 20)
            tab_lay_add.addWidget(DirButton8, 1)
            tab_lay_add.addWidget(self.combo8, 1)

        #self.layout1.addWidget(QLabel('please select the source file'))
        #self.layout1.addLayout(tab_lay_add)
        #self.layout1.addStretch(1)#设置空间之间的上下间距
        self.layout_list.append(tab_lay_add)

        for i in range(len(self.layout_list)):
            self.layout1.addLayout(self.layout_list[i])
            self.layout1.setStretch(2*i, 0)
        self.layout1.addStretch(1)  # 设置空间之间的上下间距

        self.rom_frame.update()

    def file_select(self, press, index):
        """
            文件选择回调
        """
        file, ok1 = QFileDialog.getOpenFileName(self,
                                                  "Excel文件选择",
                                                  "./",
                                                  "Excel Files (*.xlsx);;All Files (*)")
        if not file.endswith('.xlsx'):
            QMessageBox.about(self, "错误", "请选择Excel文件")
            return
        if ok1:
            self.lineedit_list[index].setText(file)
            print(file, ok1, index)
            print(self.output_file.text())
            # 读取excel 文件语言列表
            read_data = self.read_excel_file(self.lineedit_list[index].text(), 0, None, None, None)
            if index == 0:
                return
            self.write_sqlite(self.combo_list[index-1].currentText(), index)
            self.combo_list[index-1].addItems(read_data[1:])
            self.combo_list[index-1].activated[str].connect(lambda str, param = index : self.write_sqlite(str, param))

    def read_excel_file(self, filename, start_row, end_row, start_col, end_col):
        """
            读取excel文档数据
            start_row：读取数据的起始行
            end_row：读取数据的结束行
            start_col：读取数据的起始列
            end_col：读取数据的结束列
        """
        # 打开文件
        workbook = xlrd.open_workbook(filename)
        # 获取所有sheet
        sheet_name = workbook.sheet_names()[0]

        # 根据sheet索引或者名称获取sheet内容
        sheet = workbook.sheet_by_index(0)  # sheet索引从0开始
        # sheet = workbook.sheet_by_name('Sheet1')

        # print (workboot.sheets()[0])
        # sheet的名称，行数，列数
        print(sheet.name, sheet.nrows, sheet.ncols)

        # if start_row > end_row or start_col > end_col:
        #     return
        # if start_row > sheet.nrows or start_col > sheet.ncols:
        #     return
        if end_col and end_row > sheet.nrows:
            end_row = sheet.nrows
        if end_col and end_col > sheet.ncols:
            end_col = sheet.ncols

        # 获取整行和整列的值（数组）
        if start_row == None:
            result = sheet.col_values(start_col)  # 获取第2行内容
            print(result)
            return result
        elif start_col == None:
            result = sheet.row_values(start_row)
            print(result)
            return result
        elif end_row == None or end_col == None:
            result = sheet.cell_value(start_row, start_col)
            print(result)
            return result
        else:
            result_temp = []
            for i in range(end_row - start_row):
                result_temp.append(sheet.row_values(start_row+i)[start_col:end_col])
            print(result_temp)
            return result_temp

    def write_excel_file(self):
        """
            将数据写入新的Excel文档
        """
        data_list = self.ed.getAll(0)
        if not data_list:
            return
        workbook = xlwt.Workbook()
        mySheet = workbook.add_sheet('固件语言列表')
        dest_data = self.read_excel_file(self.lineedit_list[0].text(), 0, 1024, 0, 1024)
        print(len(dest_data), len(dest_data[0]))

        for i in range(len(data_list)):
            first_row = self.read_excel_file(data_list[i][0], 0, None, None, None)
            dest_col = 0
            for first_row_index in range(len(first_row)):
                if first_row[first_row_index] == data_list[i][1]:
                    dest_col = first_row_index
                    break
            dest_col_data = self.read_excel_file(data_list[i][0], None, None, dest_col, None)
            dest_all_data = self.read_excel_file(data_list[i][0], 0, 1024, 0, 1024)
            print("源列序号：%d" %(dest_col))
            print("源列数据：", dest_col_data)

            mySheet_first_row_data = self.read_excel_file(self.lineedit_list[0].text(), 0, None, None, None)
            mySheet_dest_col = 0
            for mysheet_first_row_index in range(len(mySheet_first_row_data)):
                if mySheet_first_row_data[mysheet_first_row_index] == data_list[i][1]:
                    mySheet_dest_col = mysheet_first_row_index
                    break
            else:
                mySheet_dest_col = len(mySheet_first_row_data)
            print("目标列序号：%d" % (mySheet_dest_col))

            max_row = max(len(dest_data), len(dest_all_data))
            max_col = max(len(dest_data[0]), len(dest_all_data[0]))

            for dest_all_data_row in range(max_row):
                for j in range(max_col):
                    if j == mySheet_dest_col and dest_all_data_row < len(dest_all_data):
                        # print('dest ',dest_all_data_row, j, dest_col_data[dest_all_data_row])
                        mySheet.write(dest_all_data_row, j, dest_col_data[dest_all_data_row])

        for source_row in range(len(dest_data)):
            for source_dest in range(len(dest_data[0])):
                    # print(source_row, source_dest, dest_data[source_row][source_dest])
                    try:
                        mySheet.write(source_row, source_dest, dest_data[source_row][source_dest])
                    except Exception as e:
                        print("over write pass: {}".format(e))

        now = time.localtime()
        QMessageBox.about(self, "结束", "文件已复制完成")
        workbook.save('SN_设备侧_固件标题语言'+'%s%s%s%s%s%s' %(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)+'.xls')

    def write_sqlite(self, str, param):
        """
           将数据写入数据库
           文件路径和对应语言和序号
       """
        self.ed.delete(param)
        self.ed.insert(self.lineedit_list[param].text(), str, param)
        self.ed.dbDump()

    def window2_UI(self, frame):
        """
            串口程序UI布局
        """
        # 第二个布局
        main_frame2 = QMainWindow()
        frame2_bar = QStatusBar()
        frame2_bar.setObjectName("frame2_bar")
        main_frame2.setStatusBar(frame2_bar)
        frame2_bar.showMessage("欢迎进入串口小工具")

        self.custom_frame = QFrame(main_frame2)
        self.custom_frame.setGeometry(0, 0, self.width(), frame.height() - 25)
        self.custom_frame.setFrameShape(QFrame.Panel)
        self.custom_frame.setFrameShadow(QFrame.Raised)

        self.gridLayout = QGridLayout(self.custom_frame)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.ser_databit = QtWidgets.QComboBox(self.custom_frame)
        self.ser_databit.setObjectName("ser_databit")
        self.gridLayout.addWidget(self.ser_databit, 5, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.custom_frame)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 6, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.custom_frame)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 7, 0, 1, 1)
        self.ser_display_lineedit = QtWidgets.QLineEdit(self.custom_frame)
        self.ser_display_lineedit.setObjectName("ser_display")
        self.gridLayout.addWidget(self.ser_display_lineedit, 6, 2, 1, 4)
        self.ser_refresh = QtWidgets.QPushButton(self.custom_frame)
        self.ser_refresh.setObjectName("ser_refresh")
        self.ser_refresh.clicked.connect(self.serial_update)
        self.gridLayout.addWidget(self.ser_refresh, 1, 3, 1, 1)
        self.ser_stopbit = QtWidgets.QComboBox(self.custom_frame)
        self.ser_stopbit.setObjectName("ser_stopbit")
        self.gridLayout.addWidget(self.ser_stopbit, 6, 1, 1, 1)
        self.ser_sendtimer = QtWidgets.QCheckBox(self.custom_frame)
        self.ser_sendtimer.setObjectName("ser_sendtimer")
        self.ser_sendtimer.stateChanged.connect(self.sendtmr_switch)
        self.gridLayout.addWidget(self.ser_sendtimer, 4, 2, 1, 1)
        self.ser_checkbit = QtWidgets.QComboBox(self.custom_frame)
        self.ser_checkbit.setObjectName("ser_checkbit")
        self.gridLayout.addWidget(self.ser_checkbit, 7, 1, 1, 1)
        self.ser_hex_display = QtWidgets.QCheckBox(self.custom_frame)
        self.ser_hex_display.setObjectName("ser_hex_display")
        self.ser_hex_display.stateChanged.connect(self.rdata2hex)
        self.gridLayout.addWidget(self.ser_hex_display, 1, 4, 1, 2)
        self.label_7 = QtWidgets.QLabel(self.custom_frame)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 5, 2, 1, 4)
        self.ser_num = QtWidgets.QComboBox(self.custom_frame)
        self.ser_num.setObjectName("ser_num")
        self.gridLayout.addWidget(self.ser_num, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.custom_frame)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.custom_frame)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 4, 4, 1, 1)
        self.ser_clearbtn = QtWidgets.QPushButton(self.custom_frame)
        self.ser_clearbtn.setObjectName("ser_clearbtn")
        self.ser_clearbtn.clicked.connect(self.ser_textedit_clear)
        self.gridLayout.addWidget(self.ser_clearbtn, 1, 6, 1, 1)
        self.textEdit = QtWidgets.QTextEdit(self.custom_frame)
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setFocusPolicy(Qt.NoFocus)
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 7)
        self.label = QtWidgets.QLabel(self.custom_frame)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.ser_file_select = QtWidgets.QLineEdit(self.custom_frame)
        self.ser_file_select.setObjectName("ser_file_select")
        self.gridLayout.addWidget(self.ser_file_select, 11, 0, 1, 6)
        self.set_openbtn = QtWidgets.QPushButton(self.custom_frame)
        self.set_openbtn.setObjectName("set_openbtn")
        self.set_openbtn.clicked.connect(self.oc_serial)
        self.gridLayout.addWidget(self.set_openbtn, 1, 2, 1, 1)
        self.ser_sendbtn = QtWidgets.QPushButton(self.custom_frame)
        self.ser_sendbtn.setObjectName("ser_sendbtn")
        self.ser_sendbtn.setEnabled(False)
        self.ser_sendbtn.clicked.connect(self.ser_senddata)
        self.gridLayout.addWidget(self.ser_sendbtn, 6, 6, 1, 1)
        self.ser_sendtmr_time = QtWidgets.QLineEdit(self.custom_frame)
        self.ser_sendtmr_time.setEnabled(True)
        self.ser_sendtmr_time.setText('100')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ser_sendtmr_time.sizePolicy().hasHeightForWidth())
        self.ser_sendtmr_time.setSizePolicy(sizePolicy)
        self.ser_sendtmr_time.setObjectName("ser_sendtmr_time")
        self.ser_sendtmr_time.textChanged.connect(self.sendtmr_switch)
        self.gridLayout.addWidget(self.ser_sendtmr_time, 4, 3, 1, 1)
        self.ser_bdrate = QtWidgets.QComboBox(self.custom_frame)
        self.ser_bdrate.setObjectName("ser_bdrate")
        self.gridLayout.addWidget(self.ser_bdrate, 4, 1, 1, 1)
        self.ser_sendhex = QtWidgets.QCheckBox(self.custom_frame)
        self.ser_sendhex.setObjectName("ser_sendhex")
        self.ser_sendhex.stateChanged.connect(self.sdata2hex)
        self.gridLayout.addWidget(self.ser_sendhex, 7, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.custom_frame)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 5, 0, 1, 1)
        self.ser_send_filebtn = QtWidgets.QPushButton(self.custom_frame)
        self.ser_send_filebtn.setObjectName("ser_send_filebtn")
        self.ser_send_filebtn.setEnabled(False)
        self.ser_send_filebtn.clicked.connect(self.ser_rw_sendfile_btn_clicked)
        self.gridLayout.addWidget(self.ser_send_filebtn, 10, 6, 1, 1)
        self.ser_rw_combo = QtWidgets.QComboBox(self.custom_frame)
        self.ser_rw_combo.setObjectName("ser_rw_combo")
        self.ser_rw_combo.setEnabled(False)
        self.ser_rw_combo.activated[str].connect(self.ser_rw_combo_changed)
        self.gridLayout.addWidget(self.ser_rw_combo, 10, 5, 1, 1)
        self.ser_rw_checkbox = QtWidgets.QCheckBox(self.custom_frame)
        self.ser_rw_checkbox.setObjectName("ser_rw_checkbox")
        self.ser_rw_checkbox.stateChanged.connect(self.send_file_select)
        self.gridLayout.addWidget(self.ser_rw_checkbox, 10, 0, 1, 1)
        self.ser_file_select_btn = QtWidgets.QPushButton(self.custom_frame)
        self.ser_file_select_btn.setObjectName("ser_file_select_btn")
        self.ser_file_select_btn.clicked.connect(self.ser_rw_selectbtn_clicked)
        self.gridLayout.addWidget(self.ser_file_select_btn, 11, 6, 1, 1)
        self.send_with_enter = QtWidgets.QCheckBox(self.custom_frame)
        self.send_with_enter.setObjectName("send_with_enter")
        self.gridLayout.addWidget(self.send_with_enter, 4, 5, 1, 1)

        self.sendfile_time_lable = QLabel(self.rom_frame)
        self.sendfile_time_lable.setText('文件发送时长: 0ms' )
        self.sendfile_time_lable.setVisible(False)
        self.sendfile_time_lable.setGeometry(100, frame.height(), 50, 25)
        frame2_bar.addPermanentWidget(self.sendfile_time_lable)

        self.send_bar = QProgressBar(self.rom_frame)
        self.send_bar.setGeometry(50, frame.height(), 50, 20)
        self.send_bar.setVisible(False)
        frame2_bar.addPermanentWidget(self.send_bar)

        self.sr_lable = QLabel(self.rom_frame)
        self.sr_lable.setText('S:       R:      ')
        self.sr_lable.setGeometry(100, frame.height(), 50, 25)
        frame2_bar.addPermanentWidget(self.sr_lable)

        self.label_4.setText("停止位")
        self.label_5.setText("校验位")
        self.ser_refresh.setText("刷新串口")
        self.ser_sendtimer.setText("定时发送")
        self.ser_hex_display.setText("Hex显示")
        self.label_7.setText("字符串输入框")
        self.label_2.setText("波特率")
        self.label_6.setText("ms/次")
        self.ser_clearbtn.setText("清除窗口")
        self.label.setText("串口号")
        self.set_openbtn.setText("打开串口")
        self.ser_sendbtn.setText("发送")
        self.ser_sendhex.setText("Hex发送")
        self.label_3.setText("数据位")
        self.ser_send_filebtn.setText("读写文件")
        self.ser_rw_checkbox.setText("选中读写文件")
        self.ser_file_select_btn.setText("...")
        self.send_with_enter.setText("加回车换行")

        self.ser_bdrate.addItems(baudrates)
        self.ser_bdrate.setCurrentIndex(12)
        self.ser_databit.addItems(databits)
        self.ser_databit.setCurrentIndex(3)
        self.ser_stopbit.addItems(stopbits)
        self.ser_checkbit.addItems(checkbits)
        self.ser_rw_combo.addItems(sr_select)

        # self.ser_thread = ser_recvthread(self.ser_recv)
        # self.ser_thread_working = False

        self.ser_mutex = threading.Lock()
        self.sendtmr = QTimer(self.custom_frame)
        self.sendtmr.timeout.connect(self.ser_senddata)

        self.recvtmr = QTimer(self.custom_frame)
        self.recvtmr.timeout.connect(self.ser_recv)

        self.sendfile_tmr = QTimer(self.custom_frame)
        self.sendfile_tmr.timeout.connect(self.ser_send_progerss)
        self.is_sendfile = False

        self.ser_working = False
        self.ser = serial.Serial()
        # self.ser.close()
        self.ser_recv_datalen = 0
        self.ser_send_datalen = 0
        self.read_data_file = False

        frame2_bar_frame = QFrame(main_frame2)
        frame2_bar_frame.setGeometry(0, frame.height(), self.width(), 25)

        return main_frame2

    def oc_serial(self):
        """
            打开关闭串口
        """
        if self.ser_working == False:
            try:
                self.ser.port = self.ser_num.currentText()
                self.ser.baudrate = int(self.ser_bdrate.currentText())
                self.ser.bytesize = int(self.ser_databit.currentText())
                self.ser.stopbits = int(self.ser_stopbit.currentText())
                self.ser.parity = self.ser_checkbit.currentText()
                # self.ser = serial.Serial(self.ser_num.currentText(), int(self.ser_bdrate.currentText()))
                self.ser.open()
            except:
                QMessageBox.critical(self, '串口打开失败', '没有可用的串口或当前串口被占用')
                return None
            self.ser_working = True
            self.set_openbtn.setText("关闭串口")
            if self.ser_rw_checkbox.isChecked() == False:
                self.ser_sendbtn.setEnabled(True)
            else:
                self.ser_send_filebtn.setEnabled(True)
            self.sendtmr_switch()
            # if not self.ser_thread_working:
            #     self.ser_thread_working = True
            #     self.ser_thread.start()
            # self.ser_thread.resume()
            self.recvtmr.start(0.001)
        else:
            self.recvtmr.stop()
            # self.ser_thread.pause()
            self.sendfile_tmr.stop()
            try:
                self.ser.close()
            except:
                QMessageBox.critical(self, '串口关闭失败', '串口关闭失败')
                return None

            if self.is_sendfile:
                self.sfile.close()
                self.is_sendfile = False
                self.file_send_len = 0
                self.snd_bar_value = 0
                self.ser_send_filebtn.setText('发送文件')
                self.ser_file_select.setEnabled(True)
            self.set_openbtn.setText("打开串口")
            self.ser_sendbtn.setEnabled(False)
            self.ser_send_filebtn.setEnabled(False)
            self.ser_working = False

    def serial_update(self):
        """
            更新串口端口显示
        """
        self.ser_num.clear()
        plist = list(serial.tools.list_ports.comports())
        for i in range(0, len(plist)):
            plist_0 = list(plist[i])
            #print('串口号：', list(plist[i]),str(plist_0[0]))
            self.ser_num.addItem(plist_0[0])
        if self.ser.is_open:
            self.oc_serial()

    def sendtmr_switch(self):
        """
            发送数据定时器开关
        """
        if self.ser_sendtimer.isChecked():
            self.sendtmr.stop()
            try:
                time_msec = int(self.ser_sendtmr_time.text())
            except:
                QMessageBox.critical(self, '发送失败', '发送时间为空')
                return
            try:
                if time_msec == 0:
                    time_msec = 1
                    self.ser_sendtmr_time.setText('1')
                self.sendtmr.start(time_msec)
            except:
                QMessageBox.critical(self, '定时发送失败', '超时时间超过预期')
                return
        else:
            self.sendtmr.stop()

    def ser_senddata(self):
        """
           发送数据回调
       """
        if self.ser.is_open == False:
            QMessageBox.critical(self, '发送失败', '串口未打开')
            self.sendtmr.stop()
            return
        if self.send_with_enter.isChecked():
            data = self.ser_display_lineedit.text() + '\n'
        else:
            data = self.ser_display_lineedit.text()
        self.ser.write(data.encode())
        self.ser_send_datalen += len(data)
        self.sr_lable.setText('S: %d    R: %d   ' %(self.ser_send_datalen, self.ser_recv_datalen))

    def ser_recv(self):
        """
                串口数据接受回调函数，同时将数据显示到textEdit中
        """
        self.ser_mutex.acquire()
        ser_datalen = self.ser.inWaiting()
        if(ser_datalen):
            data_recv = self.ser.read(ser_datalen)
            #print(data_recv, len(data_recv), ser_datalen)
            # 串口接收到的字符串为b'123',要转化成unicode字符串才能输出到窗口中去
            self.ser_recv_datalen += ser_datalen
            self.textEdit.moveCursor(QTextCursor.End)
            if self.ser_hex_display.isChecked():
                out_s = ''
                for i in range(0, len(data_recv)):
                    out_s = out_s + '{:02X}'.format(data_recv[i]) + ' '
                self.textEdit.insertPlainText(out_s)
            else:
                self.textEdit.insertPlainText(data_recv.decode('iso-8859-1'))
            self.sr_lable.setText('S: %d    R: %d   ' % (self.ser_send_datalen, self.ser_recv_datalen))
            if self.read_data_file:
                if data_recv != '':
                    try:
                        self.rfile.write(data_recv)
                    except:
                        self.read_data_file = False
                        self.rfile.close()
                        self.ser_send_filebtn.setText('读取文件')
                        QMessageBox.critical(self, '读取错误', '读取写入文件出错')
                else:
                    self.read_data_file = False
                    self.rfile.close()
                    self.ser_send_filebtn.setText('读取文件')
                    QMessageBox.critical(self, '接收成功', '读取写入文件成功')
        self.ser_mutex.release()

    def rdata2hex(self):
        """
                接收数据转化为16进制显示
        """
        data_text = self.textEdit.toPlainText()
        if self.ser_hex_display.isChecked():
            pass
            # out_bytes = bytes.fromhex(data_text.replace('\r', '').replace('\n', ''))#self.data2hex(data_text)
            # #print(out_bytes[0])
            # #out_s = ''.join(['%02x ' % b for b in out_bytes])
            # out_s = self.data2hex(out_bytes)
            # self.textEdit.clear()
            # self.textEdit.insertPlainText(out_s)
        else:
            pass
            #self.textEdit.insertPlainText(data_text.decode('iso-8859-1'))

    def sdata2hex(self):
        """
            发送数据转化为16进制发送
            功能未完善
        """
        if self.ser_sendhex.isChecked():
            # data_temp = self.ser_display_lineedit.text()
            # data = ''
            # for i in range(0, len(data_temp)):
            #     data = data + '%02x' %(int(data_temp[i])) + ' '
            # self.ser_display_lineedit.setText(data)
            pass

    def data2hex(self, text):
        """
            textEdit内容转化为hex格式数据显示
            功能未完善
        """
        high_hex = 30
        low_hex = 30
        result = ''
        for i in range(len(text)):
            high_hex = text[i]//10
            low_hex = text[i]%10
            result += str(high_hex) + ' ' + str(low_hex) + ' '
        return result

    def ser_textedit_clear(self):
        """
           清空textEdit内容
       """
        self.textEdit.clear()
        self.ser_send_datalen = 0
        self.ser_recv_datalen = 0
        self.sr_lable.setText('S: %d    R: %d   ' % (self.ser_send_datalen, self.ser_recv_datalen))
        #self.textEdit.moveCursor(QTextCursor.End)

    def send_file_select(self):
        """
           单选框：开启读写文件功能，同时关闭定时发送功能和手动发送数据的功能
       """
        if self.ser_rw_checkbox.isChecked():
            self.sendtmr.stop()
            self.ser_sendtimer.setCheckState(False)
            self.ser_sendtimer.setEnabled(False)
            self.ser_sendbtn.setEnabled(False)
            self.ser_rw_combo.setEnabled(True)
            if self.ser.is_open:
                self.ser_send_filebtn.setEnabled(True)
        else:
            self.ser_sendtimer.setEnabled(True)
            self.ser_sendbtn.setEnabled(True)
            self.ser_rw_combo.setEnabled(False)
            self.ser_send_filebtn.setEnabled(False)
            self.send_bar.setVisible(False)
            self.sendfile_time_lable.setVisible(False)
        self.read_data_file = False

    def ser_rw_combo_changed(self, str):
        """
            下拉框：选择发送文件或读取文件
        """
        if self.ser_rw_combo.currentText() != '':
            self.ser_send_filebtn.setText(str)
        else:
            self.ser_send_filebtn.setText('读写文件')
            self.send_bar.setVisible(False)
            self.sendfile_time_lable.setVisible(False)

    def ser_rw_sendfile_btn_clicked(self):
        """
            发送文件按键回调：点击开始发送文件
        """
        if self.ser_rw_combo.currentText() == '发送文件':
            self.read_data_file = False
            if self.is_sendfile == False:
                self.is_sendfile = True
                self.file_send_len = 0
                self.snd_bar_value = 0
                self.sendfile_time = 0

                self.ser_send_filebtn.setText('结束发送')
                # with open(self.ser_file_select.text()) as sfile:
                #     for data in sfile.readlines():
                #         self.ser.write(data.encode())
                #         self.file_send_len += len(data)
                #         self.snd_bar_value = self.file_send_len *100// self.send_file_size
                #         if file_data == '':
                #             self.snd_bar_value = 99
                #         self.send_bar.setValue(self.snd_bar_value)
                #         print(self.file_send_len, self.send_file_size)
                try:
                    if self.ser_file_select.text().endswith('bin'):
                        self.sfile = open(self.ser_file_select.text(), 'rb')
                    else:
                        self.sfile = open(self.ser_file_select.text(), 'r')
                except:
                    self.is_sendfile = False
                    self.file_send_len = 0
                    self.snd_bar_value = 0
                    self.ser_send_filebtn.setText('发送文件')
                    QMessageBox.critical(self, '文件发送失败', '文件不存在或已被其他程序打开')
                    return
                self.ser_rw_combo.setEnabled(False)
                self.send_bar.setVisible(True)
                self.ser_file_select_btn.setEnabled(False)
                self.sendfile_time_lable.setVisible(True)
                self.sendfile_tmr.start(100)
            else:
                self.is_sendfile = False
                self.file_send_len = 0
                self.snd_bar_value = 0
                self.sendfile_tmr.stop()
                self.sfile.close()
                self.ser_send_filebtn.setText('发送文件')
                self.ser_rw_combo.setEnabled(True)
                self.ser_file_select.setEnabled(True)
                self.ser_file_select_btn.setEnabled(True)
        elif self.ser_rw_combo.currentText() == '读取文件':
            self.send_bar.setVisible(False)
            self.sendfile_time_lable.setVisible(False)
            if self.read_data_file == False:
                self.read_data_file = True
                self.ser_send_filebtn.setText('停止')
                self.rfile = open('read_file_%04d%02d%02d%02d%02d%02d.bin' %(
                                time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday,
                                time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec), 'wb')
            else:
                self.read_data_file = False
                self.ser_send_filebtn.setText('读取文件')
                self.rfile.close()
        else:
            self.send_bar.setVisible(False)
            self.sendfile_time_lable.setVisible(False)
            self.ser_send_filebtn.setText('读写文件')
            self.read_data_file = False

    def ser_rw_selectbtn_clicked(self):
        """
            点击选择要发送的文件
        """
        file, ok1 = QFileDialog.getOpenFileName(self,
                                                "文件选择",
                                                "./",
                                                "All Files (*);;Txt Files (.txt);;Bin Files (.bin)")
        if ok1:
            self.ser_file_select.setText(file)
            self.send_file_size = os.path.getsize(file)

    def ser_send_progerss(self):
        """
           文件发送定时器回调函数
       """
        try:
            # if self.ser_file_select.text(). endswith('bin'):
            #     pass
            # else:
                if self.send_file_size < 1024:
                    file_data = self.sfile.read(self.send_file_size)
                else:
                    file_data = self.sfile.read(1024)
        except:
            self.is_sendfile = False
            self.file_send_len = 0
            self.snd_bar_value = 0
            self.sendfile_tmr.stop()
            self.ser_send_filebtn.setText('发送文件')
            self.send_bar.setVisible(False)
            self.sendfile_time_lable.setVisible(False)
            self.ser_file_select_btn.setEnabled(True)
            self.ser_rw_combo.setEnabled(True)
            QMessageBox.critical(self, '文件发送失败', '文件不存在或已被其他程序打开')
            return
        self.ser_file_select.setEnabled(False)
        if self.ser_file_select.text().endswith('bin'):
            self.ser.write(file_data)
        else:
            self.ser.write(file_data.encode())
        self.file_send_len += len(file_data)
        self.snd_bar_value = self.file_send_len * 100 // self.send_file_size
        self.send_bar.setValue(self.snd_bar_value)
        self.sendfile_time += 100
        self.sendfile_time_lable.setText('文件发送时长: %dms' % (self.sendfile_time))
        self.ser_send_datalen += len(file_data)
        self.sr_lable.setText('S: %d    R: %d   ' % (self.ser_send_datalen, self.ser_recv_datalen))
        if file_data == '' or self.snd_bar_value >= 100:
            self.snd_bar_value = 100
            self.ser_file_select.setEnabled(True)
            self.sendfile_tmr.stop()
            self.sfile.close()
            self.ser_send_filebtn.setText('发送文件')
            self.ser_file_select_btn.setEnabled(True)
            self.ser_rw_combo.setEnabled(True)
            QMessageBox.about(self, '发送完成', '文件发送成功')

        # print(self.file_send_len, self.send_file_size)


    def window3_UI(self, frame):
        """
            图片转换程序UI布局
        """
        # 第二个布局
        main_frame3 = QMainWindow()
        frame3_bar = QStatusBar()
        frame3_bar.setObjectName("frame3_bar")
        main_frame3.setStatusBar(frame3_bar)
        frame3_bar.showMessage("欢迎进入图片转换")

        self.picbin_frame = QFrame(main_frame3)
        self.picbin_frame.setGeometry(0, 0, self.width(), frame.height() - 25)
        self.picbin_frame.setFrameShape(QFrame.Panel)
        self.picbin_frame.setFrameShadow(QFrame.Raised)

        self.gridLayout = QtWidgets.QGridLayout(self.picbin_frame)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.tableWidget_bin_file = QtWidgets.QTableWidget(self.picbin_frame)
        self.tableWidget_bin_file.setObjectName("tableWidget_bin_file")
        self.tableWidget_bin_file.setColumnCount(0)
        self.tableWidget_bin_file.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget_bin_file, 3, 0, 1, 8)
        self.bin_dir_btn = QtWidgets.QPushButton(self.picbin_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bin_dir_btn.sizePolicy().hasHeightForWidth())
        self.bin_dir_btn.setSizePolicy(sizePolicy)
        self.bin_dir_btn.setObjectName("bin_dir_btn")
        self.gridLayout.addWidget(self.bin_dir_btn, 2, 7, 1, 1)
        self.bin_dir_btn.clicked.connect(self.bin_btn_clicked)
        self.main3_start_btn = QtWidgets.QPushButton(self.picbin_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main3_start_btn.sizePolicy().hasHeightForWidth())
        self.main3_start_btn.setSizePolicy(sizePolicy)
        self.main3_start_btn.setObjectName("start_btn")
        self.gridLayout.addWidget(self.main3_start_btn, 6, 7, 1, 1)
        self.main3_start_btn.clicked.connect(self.start_btn_clicked)
        self.pic_dir_btn = QtWidgets.QPushButton(self.picbin_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pic_dir_btn.sizePolicy().hasHeightForWidth())
        self.pic_dir_btn.setSizePolicy(sizePolicy)
        self.pic_dir_btn.setObjectName("pic_dir_btn")
        self.gridLayout.addWidget(self.pic_dir_btn, 0, 7, 1, 1)
        self.pic_dir_btn.clicked.connect(self.pic_btn_cliked)
        self.tableWidget_pic_file = QtWidgets.QTableWidget(self.picbin_frame)
        self.tableWidget_pic_file.setObjectName("tableWidget_pic_file")
        self.tableWidget_pic_file.setColumnCount(0)
        self.tableWidget_pic_file.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget_pic_file, 1, 0, 1, 8)
        self.checkBox_flash = QtWidgets.QCheckBox(self.picbin_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_flash.sizePolicy().hasHeightForWidth())
        self.checkBox_flash.setSizePolicy(sizePolicy)
        self.checkBox_flash.setObjectName("checkBox_flash")
        self.gridLayout.addWidget(self.checkBox_flash, 6, 0, 1, 1)
        self.checkBox_flash.stateChanged.connect(self.flash_ex_checked)
        self.checkBox_alpha = QtWidgets.QCheckBox(self.picbin_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_alpha.sizePolicy().hasHeightForWidth())
        self.checkBox_alpha.setSizePolicy(sizePolicy)
        self.checkBox_alpha.setObjectName("checkBox_alpha")
        self.gridLayout.addWidget(self.checkBox_alpha, 6, 1, 1, 1)
        self.checkBox_alpha.stateChanged.connect(self.alpha_checked)
        self.refresh_btn = QtWidgets.QPushButton(self.picbin_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refresh_btn.sizePolicy().hasHeightForWidth())
        self.refresh_btn.setSizePolicy(sizePolicy)
        self.refresh_btn.setObjectName("refresh_btn")
        self.gridLayout.addWidget(self.refresh_btn, 6, 2, 1, 1)
        self.refresh_btn.clicked.connect(self.refresh_btn_clicked)
        self.lineEdit_bin_dir = QtWidgets.QLineEdit(self.picbin_frame)
        self.lineEdit_bin_dir.setObjectName("lineEdit_bin_dir")
        self.gridLayout.addWidget(self.lineEdit_bin_dir, 2, 0, 1, 7)
        self.lineEdit_pic_dir = QtWidgets.QLineEdit(self.picbin_frame)
        self.lineEdit_pic_dir.setObjectName("lineEdit_pic_dir")
        self.gridLayout.addWidget(self.lineEdit_pic_dir, 0, 0, 1, 7)

        self.bin_dir_btn.setText("bin文件夹")
        self.main3_start_btn.setText("开始")
        self.pic_dir_btn.setText("文件夹...")
        self.checkBox_flash.setText("外部flash")
        self.checkBox_alpha.setText("透明度")
        self.refresh_btn.setText("刷新")

        frame3_bar_frame = QFrame(main_frame3)
        frame3_bar_frame.setGeometry(0, frame.height(), self.width(), 25)

        return main_frame3

    def scan_data(self, dir):
        for root, dirs, files in os.walk(dir):
            # return root#当前目录路径
            # return dirs#当前路径下所有子目录
            # return files  # 当前路径下所有非目录子文件
            for file in files:
                if os.path.splitext(file)[-1] == '.bmp' or os.path.splitext(file)[-1] == '.png':
                    file_path = os.path.join(root, file).replace('\\', '/')
                    self.filepath_list.append(file_path)
                    self.filename_list.append(file)
        # print(self.filepath_list)
        # print(self.filename_list)

    def scan_bin(self, dir):
        for root, dirs, files in os.walk(dir):
            # return root#当前目录路径
            # return dirs#当前路径下所有子目录
            # return files  # 当前路径下所有非目录子文件
            for file in files:
                if os.path.splitext(file)[-1] == '.bin':
                    file_path = os.path.join(root, file).replace('\\', '/')
                    self.filepath_bin_list.append(file_path)
                    self.filename_bin_list.append(file)

    def pic_btn_cliked(self):
        pic_dir_path = QFileDialog.getExistingDirectory(self)

        if pic_dir_path:
            self.lineEdit_pic_dir.setText(pic_dir_path)
            self.refresh_btn_clicked()

    def bin_btn_clicked(self):
        bin_dir_path = QFileDialog.getExistingDirectory(self)
        if bin_dir_path:
            self.lineEdit_bin_dir.setText(bin_dir_path)
            self.refresh_btn_clicked()

    def refresh_btn_clicked(self):
        dir  = self.lineEdit_pic_dir.text()
        self.filename_list.clear()
        self.filepath_list.clear()
        self.scan_data(dir)
        self.tableWidget_pic_file.clear()
        self.tableWidget_pic_file.setRowCount(len(self.filename_list))
        self.tableWidget_pic_file.setColumnCount(3)
        self.tableWidget_pic_file.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_pic_file.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget_pic_file.setHorizontalHeaderLabels(['透明度', '内外flash', '文件'])
        for i in range(len(self.filepath_list)):
            file_element = self.filepath_list[i].split('.')
            if 'alpha' in file_element:
                self.tableWidget_pic_file.setItem(i, 0, QTableWidgetItem('yes'))
            elif 'point' in file_element:
                self.tableWidget_pic_file.setItem(i, 0, QTableWidgetItem('point'))
            elif 'pAA' in file_element:
                self.tableWidget_pic_file.setItem(i, 0, QTableWidgetItem('pAA'))
            else:
                self.tableWidget_pic_file.setItem(i, 0, QTableWidgetItem('no'))

            if 'mcu' in file_element:
                self.tableWidget_pic_file.setItem(i, 1, QTableWidgetItem('force_mcu'))
            else:
                self.tableWidget_pic_file.setItem(i, 1, QTableWidgetItem('mcu'))
            self.tableWidget_pic_file.setItem(i, 2, QTableWidgetItem(self.filepath_list[i]))
        self.checkBox_flash.setChecked(False)
        self.checkBox_alpha.setChecked(False)

        dir = self.lineEdit_bin_dir.text()
        self.filename_bin_list.clear()
        self.filepath_bin_list.clear()
        self.scan_bin(dir)
        self.tableWidget_bin_file.clear()
        self.tableWidget_bin_file.setRowCount(len(self.filepath_bin_list))
        self.tableWidget_bin_file.setColumnCount(1)
        self.tableWidget_bin_file.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_bin_file.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget_bin_file.setHorizontalHeaderLabels(['文件'])
        for i in range(len(self.filepath_bin_list)):
            self.tableWidget_bin_file.setItem(i, 0, QTableWidgetItem(self.filepath_bin_list[i]))


    def flash_ex_checked(self):
        # row_size = self.tableWidget_pic_file.rowCount()
        # for i in range(row_size):
        #     if self.tableWidget_pic_file.item(i, 1).text().lower() == 'force_mcu'.lower():
        #         continue
        #
        #     if self.checkBox_flash.isChecked():
        #         self.tableWidget_pic_file.setItem(i, 1, QTableWidgetItem('spi'))
        #         # self.tableWidget_pic_file.item(i, 1).setText('spi')
        #     else:
        #         self.tableWidget_pic_file.setItem(i, 1, QTableWidgetItem('mcu'))
        #         # self.tableWidget_pic_file.item(i, 1).setText('mcu')
        dir = self.lineEdit_pic_dir.text()
        self.filename_list.clear()
        self.filepath_list.clear()
        self.scan_data(dir)
        self.tableWidget_pic_file.clear()
        self.tableWidget_pic_file.setRowCount(len(self.filename_list))
        self.tableWidget_pic_file.setColumnCount(3)
        self.tableWidget_pic_file.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_pic_file.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget_pic_file.setHorizontalHeaderLabels(['透明度', '内外flash', '文件'])
        for i in range(len(self.filepath_list)):
            file_element = self.filepath_list[i].split('.')
            if 'pAA' in file_element:
                self.tableWidget_pic_file.setItem(i, 0, QTableWidgetItem('pAA'))
            else:
                if self.checkBox_alpha.isChecked():
                    self.tableWidget_pic_file.setItem(i, 0, QTableWidgetItem('yes'))
                else:
                    if 'alpha' in file_element:
                        self.tableWidget_pic_file.setItem(i, 0, QTableWidgetItem('yes'))
                    elif 'point' in file_element:
                        self.tableWidget_pic_file.setItem(i, 0, QTableWidgetItem('point'))
                    else:
                        self.tableWidget_pic_file.setItem(i, 0, QTableWidgetItem('no'))

            if 'mcu' in file_element:
                self.tableWidget_pic_file.setItem(i, 1, QTableWidgetItem('force_mcu'))
            else:
                if self.checkBox_flash.isChecked():
                    self.tableWidget_pic_file.setItem(i, 1, QTableWidgetItem('spi'))
                else:
                    self.tableWidget_pic_file.setItem(i, 1, QTableWidgetItem('mcu'))
            self.tableWidget_pic_file.setItem(i, 2, QTableWidgetItem(self.filepath_list[i]))

    def alpha_checked(self):
        # row_size = self.tableWidget_pic_file.rowCount()
        # for i in range(row_size):
        #     if self.tableWidget_pic_file.item(i, 1).text().lower() == 'pAA'.lower():
        #         continue
        #
        #     if self.checkBox_alpha.isChecked():
        #         self.tableWidget_pic_file.setItem(i, 0, QTableWidgetItem('yes'))
        #         # self.tableWidget_pic_file.item(i, 0).setText('yes')
        #     else:
        #         self.tableWidget_pic_file.setItem(i, 0, QTableWidgetItem('no'))
        #         # self.tableWidget_pic_file.item(i, 0).setText('no')

        dir = self.lineEdit_pic_dir.text()
        self.filename_list.clear()
        self.filepath_list.clear()
        self.scan_data(dir)
        self.tableWidget_pic_file.clear()
        self.tableWidget_pic_file.setRowCount(len(self.filename_list))
        self.tableWidget_pic_file.setColumnCount(3)
        self.tableWidget_pic_file.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_pic_file.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget_pic_file.setHorizontalHeaderLabels(['透明度', '内外flash', '文件'])
        for i in range(len(self.filepath_list)):
            file_element = self.filepath_list[i].split('.')
            if 'pAA' in file_element:
                self.tableWidget_pic_file.setItem(i, 0, QTableWidgetItem('pAA'))
            else:
                if self.checkBox_alpha.isChecked():
                    self.tableWidget_pic_file.setItem(i, 0, QTableWidgetItem('yes'))
                else:
                    if 'alpha' in file_element:
                        self.tableWidget_pic_file.setItem(i, 0, QTableWidgetItem('yes'))
                    elif 'point' in file_element:
                        self.tableWidget_pic_file.setItem(i, 0, QTableWidgetItem('point'))
                    else:
                        self.tableWidget_pic_file.setItem(i, 0, QTableWidgetItem('no'))

            if 'mcu' in file_element:
                self.tableWidget_pic_file.setItem(i, 1, QTableWidgetItem('force_mcu'))
            else:
                if self.checkBox_flash.isChecked():
                    self.tableWidget_pic_file.setItem(i, 1, QTableWidgetItem('spi'))
                else:
                    self.tableWidget_pic_file.setItem(i, 1, QTableWidgetItem('mcu'))
            self.tableWidget_pic_file.setItem(i, 2, QTableWidgetItem(self.filepath_list[i]))

    def calculate_crc16(self, buf, len):
        gx = int(0x8005)
        crc16 = int(0)
        if len == 0:
            return 0

        if buf:
            for i in range(len):
                data = buf[i]
                # print(data, i, len)
                data = (data << 8) & 0xffff
                # data = (data * 256) & 0xffff
                crc16 = (crc16 ^ data) & 0xffff
                for j in range(8):
                    msb = crc16 & 0x8000
                    crc16 = (crc16 << 1) & 0xffff
                    # crc16 = (crc16 * 2) & 0xffff
                    if msb == 0x8000:
                        crc16 = (crc16 ^ gx) & 0xffff
        else:
            return 0

        return crc16

    pixel_byte = 2

    def pic_and_font_bin_file_create(self, FilePathList, FileNameList, FilePathList_bin, FileNameList_bin):
        # picture.bin and picture_font_merge.bin file create
        print("create picture_font_merge.bin file")
        color_buf = []
        picture_data = []

        pic_offset = 0
        fileLenList_bin = []
        color_buf.clear()

        for i in range(len(FilePathList)):
            image = QImage()
            image.load(FilePathList[i])
            image_pal_len = image.colorCount()
            # print(image.width(), image.height(), image.byteCount(), image.colorCount(), image.depth())
            # print(image.colorTable())
            # rgb = image.colorTable()
            # print(len(rgb))
            # image_palatte = []
            # for i in range(len(rgb)):
            #     r = qRed(rgb[i])
            #     g = qGreen(rgb[i])
            #     b = qBlue(rgb[i])
            #     alpha = qAlpha(rgb[i])
            #
            #     image_palatte += r, g, b
            # print(image_palatte)


            # print(checkFilePathList[i])
            img = Image.open(FilePathList[i])
            img_pix = img.load()
            # print("pic width %d, height %d, mode %s" %(img.size[0], img.size[1], img.mode))
            # print(img.width, img.height)
            color = 0
            alpha = 0
            if self.tableWidget_pic_file.item(i, 1).text() == 'spi':
                x_align_size = (img.size[0] + 3) / 4 * 4
                for y in range(img.size[1]):
                    for x in range(img.size[0]):
                        if img.mode == 'RGBA':
                            if self.tableWidget_pic_file.item(i, 0).text() == 'yes':
                                alpha = img_pix[x, y][3]
                                color = ((img_pix[x, y][2] >> 3) << 11) | \
                                        ((img_pix[x, y][1] >> 2) << 5) | \
                                        ((img_pix[x, y][0] >> 3) << 0)
                            else:
                                alpha = img_pix[x, y][3]
                                # color = (((img_pix[x, y][2]) >> 3) << 11) | \
                                #         (((img_pix[x, y][1]) >> 2) << 5) | \
                                #         (((img_pix[x, y][0]) >> 3) << 0)
                                color = (((img_pix[x, y][2] * alpha // 0xFF) >> 3) << 11) | \
                                        (((img_pix[x, y][1] * alpha // 0xFF) >> 2) << 5) | \
                                        (((img_pix[x, y][0] * alpha // 0xFF) >> 3) << 0)
                        elif img.mode == 'RGB':
                            color = ((img_pix[x, y][2] >> 3) << 11) | \
                                    ((img_pix[x, y][1] >> 2) << 5) | \
                                    ((img_pix[x, y][0] >> 3) << 0)
                        elif img.mode == 'LA':
                            color = ((img_pix[x, y][0] >> 0) << 8) | \
                                    ((img_pix[x, y][1] >> 0) << 0)
                        elif img.mode == 'L' or img.mode == 'P':
                            color = ((img_pix[x, y] >> 0) << 0)

                        if img.mode == 'RGBA':
                            if self.tableWidget_pic_file.item(i, 0).text() == 'yes':
                                color_buf.append(alpha)
                                color_buf.append((color >> 8) & 0xFF)
                                color_buf.append((color >> 0) & 0xFF)
                            elif self.tableWidget_pic_file.item(i, 0).text() == 'point':
                                if color <= 0:
                                    continue
                                color_buf.append(x)
                                color_buf.append(y)
                                color_buf.append(alpha)
                                color_buf.append((color >> 8) & 0xFF)
                                color_buf.append((color >> 0) & 0xFF)
                            elif self.tableWidget_pic_file.item(i, 0).text() == 'pAA':
                                if color <= 0:
                                    continue
                                color_buf.append(x)
                                color_buf.append(y)
                                color_buf.append(alpha)
                                color_buf.append((color >> 8) & 0xFF)
                                color_buf.append((color >> 0) & 0xFF)
                            else:
                                color_buf.append((color >> 8) & 0xFF)
                                color_buf.append((color >> 0) & 0xFF)
                        elif img.mode == 'RGB' or img.mode == 'LA':
                            color_buf.append((color >> 8) & 0xFF)
                            color_buf.append((color >> 0) & 0xFF)
                        elif img.mode == 'L' or img.mode == 'P':
                            color_buf.append((color >> 0) & 0xFF)

                        picture_data += color_buf
                        color_buf.clear()

                if img.mode == 'P':
                    img_pal = img.getpalette()
                    imgpal_len = image_pal_len # len(img_pal) // 3
                    # print(img_pal)
                    # print(imgpal_len)
                    color_buf.append((imgpal_len >> 0) & 0xFF)
                    color_buf.append((imgpal_len >> 8) & 0xFF)

                    for pal_index in range(imgpal_len):
                        r = img_pal[pal_index * 3 + 0] >> 3
                        g = img_pal[pal_index * 3 + 1] >> 2
                        b = img_pal[pal_index * 3 + 2] >> 3
                        table = (r << 0) | (g << 5) | (b << 11)
                        color_buf.append((table >> 8) & 0xFF)
                        color_buf.append((table >> 0) & 0xFF)
                        picture_data += color_buf
                        color_buf.clear()

        with open('picture.bin', 'wb') as f:
            # print(picture_data)
            f.seek(0)
            for data in picture_data:
                f.write(data.to_bytes(1, byteorder='little'))

        # picture_font_merge.bin create
        font_data = []

        for i in range(len(FilePathList_bin)):
            with open(FilePathList_bin[i], "rb") as f_bin:
                data = f_bin.readline()
                while data:
                    for bin_data in data:
                        font_data.append(bin_data)
                    data = f_bin.readline()
            fileLenList_bin.append('#define\t%s_OFFSET\t\t0x%08X\r\n' % (FileNameList_bin[i].split('.')[0].upper(), pic_offset))
            pic_offset = pic_offset + os.path.getsize(FilePathList_bin[i])

        if (len(FilePathList_bin)):
            remind_size = (len(font_data) + 16) % 4096

            if remind_size > 0:
                temp = [0xff for _ in range(4096 - remind_size)]
                pic_offset = len(font_data) + 16 + 4096 - remind_size
                font_data = font_data + temp
            else:
                pic_offset = len(font_data) + 16

            picture_data = font_data + picture_data
        else:
            pic_offset = 16
        # print(pic_offset)

        # crc_16 = 0
        crc_16 = self.calculate_crc16(picture_data, len(picture_data))
        buf = [0] * 16
        buf[0] = ((crc_16 >> 0) & 0xFF)
        buf[1] = ((crc_16 >> 8) & 0xFF)
        buf[2] = ((len(picture_data) >> 0) & 0xFF)
        buf[3] = ((len(picture_data) >> 8) & 0xFF)
        buf[4] = ((len(picture_data) >> 16) & 0xFF)
        buf[5] = ((len(picture_data) >> 24) & 0xFF)

        picture_data = buf + picture_data

        with open("picture_font_merge.bin", "wb") as f:
            f.seek(0)
            for data in picture_data:
                # print(data)
                f.write(data.to_bytes(1, byteorder='little'))

        return fileLenList_bin, pic_offset, crc_16

    def pic_all_data_c_file_create(self, FilePathList, FileNameList):
        # picture_data.c file create
        print("create picture_all_data.c file")
        picture_data = []
        pic_buf = []
        pic_buf.clear()
        picture_data.clear()
        pic_buf = "/*************************************************************\r\n"
        picture_data.append(pic_buf)
        pic_buf = "** this file is all picture data source file\r\n"
        picture_data.append(pic_buf)
        pic_buf = "** by chenlue\r\n"
        picture_data.append(pic_buf)
        pic_buf = "*************************************************************/\r\n"
        picture_data.append(pic_buf)
        pic_buf = "\r\n\r\n"
        picture_data.append(pic_buf)

        for i in range(len(FilePathList)):
            # if self.tableWidget_pic_file.item(i, 1).text() == 'spi':
            #     continue

            image = QImage()
            image.load(FilePathList[i])
            image_pal_len = image.colorCount()

            # print(FilePathList[i])
            img = Image.open(FilePathList[i])
            img_pix = img.load()
            # print("pic width %d, height %d, mode %s" %(img.size[0], img.size[1], img.mode))
            color = 0
            alpha = 0
            bit_point = 0
            pos = 0
            last_pos = 0
            if img.mode == 'RGBA':
                if self.tableWidget_pic_file.item(i, 0).text() == 'yes':
                    bit_point = self.pixel_byte+1
                elif self.tableWidget_pic_file.item(i, 0).text() == 'pAA':
                    bit_point = 4
                elif self.tableWidget_pic_file.item(i, 0).text() == 'point':
                    bit_point = 4
                else:
                    bit_point = self.pixel_byte
            elif img.mode == 'RGB':
                bit_point = self.pixel_byte
            elif img.mode == 'LA':
                bit_point = self.pixel_byte
            elif img.mode == 'P' or img.mode == 'L':
                bit_point = 1

            if bit_point == 1:
                pic_buf = "const unsigned char pic_%s_data[%d*%d*%d+2+%d*%d] = \r\n{\r\n\t" \
                          % (FileNameList[i].split('.')[0], img.size[0], img.size[1], bit_point, image_pal_len, self.pixel_byte)
            elif (bit_point == 2) or (bit_point == 3):
                pic_buf = "const unsigned char pic_%s_data[%d*%d*%d] = \r\n{\r\n\t" \
                          % (FileNameList[i].split('.')[0], img.width, img.height, bit_point)
            else:
                point_num = 0
                for y in range(img.size[1]):
                    for x in range(img.size[0]):
                        alpha = img_pix[x, y][3]
                        # color = (((img_pix[x, y][2]) >> 3) << 11) | \
                        #         (((img_pix[x, y][1]) >> 2) << 5) | \
                        #         (((img_pix[x, y][0]) >> 3) << 0)
                        color = (((img_pix[x, y][2] * alpha // 0xFF) >> 3) << 11) | \
                                (((img_pix[x, y][1] * alpha // 0xFF) >> 2) << 5) | \
                                (((img_pix[x, y][0] * alpha // 0xFF) >> 3) << 0)
                        if color > 0:
                            point_num += 1
                pic_buf = "const unsigned char pic_%s_data[%d*%d] = \r\n{\r\n\t" \
                          % (FileNameList[i].split('.')[0], point_num, 5)
            picture_data.append(pic_buf)

            x_align_size = (img.size[0] + 3) / 4 * 4
            for y in range(img.size[1]):
                for x in range(img.size[0]):
                    if img.mode == 'RGBA':
                        if bit_point == 3:
                            alpha = img_pix[x, y][3]
                            color = ((img_pix[x, y][2] >> 3) << 11) | \
                                    ((img_pix[x, y][1] >> 2) << 5) | \
                                    ((img_pix[x, y][0] >> 3) << 0)
                        else:
                            alpha = img_pix[x, y][3]
                            # color = (((img_pix[x, y][2]) >> 3) << 11) | \
                            #         (((img_pix[x, y][1]) >> 2) << 5) | \
                            #         (((img_pix[x, y][0]) >> 3) << 0)
                            color = (((img_pix[x, y][2] * alpha // 0xFF) >> 3) << 11) | \
                                    (((img_pix[x, y][1] * alpha // 0xFF) >> 2) << 5) | \
                                    (((img_pix[x, y][0] * alpha // 0xFF) >> 3) << 0)
                    elif img.mode == 'RGB':
                        color = ((img_pix[x, y][2] >> 3) << 11) | \
                                ((img_pix[x, y][1] >> 2) << 5) | \
                                ((img_pix[x, y][0] >> 3) << 0)
                    elif img.mode == 'LA':
                        color = ((img_pix[x, y][0] >> 0) << 8) | \
                                ((img_pix[x, y][1] >> 0) << 0)
                    elif img.mode == 'L' or img.mode == 'P':
                        color = ((img_pix[x, y] >> 0) << 0)

                    if (pos % 16 == 0) and (pos != last_pos):
                        last_pos = pos
                        pic_buf = "\r\n\t"
                        picture_data.append(pic_buf)

                    if img.mode == 'RGBA':
                        if bit_point == 3:
                            pic_buf = "0x%02X, 0x%02X, 0x%02X, " % (alpha, (color >> 8) & 0xff, (color >> 0) & 0xff)
                            pos += 3
                        elif bit_point == 4:
                            if color <= 0:
                                pic_buf = ""
                            else:
                                pic_buf = "0x%02X, 0x%02X, 0x%02X, 0x%02X, 0x%02X, " \
                                          % (x, y, alpha, (color >> 8) & 0xff, (color >> 0) & 0xff)
                                pos += 5
                        else:
                            pic_buf = "0x%02X, 0x%02X, " \
                                      % ((color >> 8) & 0xff, (color >> 0) & 0xff)
                            pos += 2
                    elif img.mode == 'RGB' or img.mode == 'LA':
                        pic_buf = "0x%02X, 0x%02X, " \
                                  % ((color >> 8) & 0xff, (color >> 0) & 0xff)
                        pos += 2
                    elif img.mode == 'L' or img.mode == 'P':
                        pic_buf = "0x%02X, " \
                                  % ((color >> 0) & 0xff)
                        pos += 1

                    picture_data.append(pic_buf)

            if img.mode == 'P':
                img_pal = list(img.getpalette())
                imgpal_len = image_pal_len # len(img_pal) // 3
                # print(img_pal)
                # print(imgpal_len)
                pic_buf = "\r\n\t0x%02X, 0x%02X,\r\n\t" % ((imgpal_len >> 0) & 0xff, (imgpal_len >> 8) & 0xff)
                picture_data.append(pic_buf)

                pos = 0
                last_pos = 0
                for pal_index in range(imgpal_len):
                    if (pos % 16) == 0 and (pos != last_pos):
                        last_pos = pos
                        pic_buf = "\r\n\t"
                        picture_data.append(pic_buf)
                    r = img_pal[pal_index*3 + 0] >> 3
                    g = img_pal[pal_index*3 + 1] >> 2
                    b = img_pal[pal_index*3 + 2] >> 3
                    table = (r << 0) | (g << 5) | (b << 11)
                    pic_buf = "0x%02X, 0x%02X, " % ((table >> 8) & 0xff, (table >> 0) & 0xff)
                    picture_data.append(pic_buf)
                    pos += 2

            pic_buf = "\r\n};\r\n\r\n"
            picture_data.append(pic_buf)

        with open("picture_all_data.c", 'w+') as pic_data:
            for data in picture_data:
                pic_data.write(data)

    def pic_all_data_h_file_create(self, FilePathList, FileNameList):
        # picture_all_data.h file create
        print("create picture_all_data.h file")
        picture_data = []
        pic_buf = []
        pic_buf.clear()
        picture_data.clear()
        pic_buf = "/*************************************************************\r\n"
        picture_data.append(pic_buf)
        pic_buf = "** this file is all picture data head file\r\n"
        picture_data.append(pic_buf)
        pic_buf = "** by chenlue\r\n"
        picture_data.append(pic_buf)
        pic_buf = "*************************************************************/\r\n"
        picture_data.append(pic_buf)
        pic_buf = "#ifndef _PICTURE_ALL_DATA_H\r\n"
        picture_data.append(pic_buf)
        pic_buf = "#define _PICTURE_ALL_DATA_H\r\n"
        picture_data.append(pic_buf)
        pic_buf = "\r\n\r\n"
        picture_data.append(pic_buf)

        for i in range(len(FilePathList)):
            # if self.tableWidget_pic_file.item(i, 1).text() == 'spi':
            #     continue

            image = QImage()
            image.load(FilePathList[i])
            image_pal_len = image.colorCount()

            # print(FilePathList[i])
            img = Image.open(FilePathList[i])
            img_pix = img.load()
            # print("pic width %d, height %d, mode %s" %(img.size[0], img.size[1], img.mode))
            bit_point = 0
            if img.mode == 'RGBA':
                if self.tableWidget_pic_file.item(i, 0).text() == 'yes':
                    bit_point = self.pixel_byte+1
                elif self.tableWidget_pic_file.item(i, 0).text() == 'pAA':
                    bit_point = 4
                elif self.tableWidget_pic_file.item(i, 0).text() == 'point':
                    bit_point = 4
                else:
                    bit_point = self.pixel_byte
            elif img.mode == 'RGB':
                bit_point = self.pixel_byte
            elif img.mode == 'LA':
                bit_point = self.pixel_byte
            elif img.mode == 'P' or img.mode == 'L':
                bit_point = 1

            if (bit_point == 1):
                pic_buf = "extern const unsigned char pic_%s_data[%d*%d*%d+2+%d*%d];\r\n" \
                          % (FileNameList[i].split('.')[0], img.size[0], img.size[1], bit_point, image_pal_len, self.pixel_byte)
            elif (bit_point == 2) or (bit_point == 3):
                pic_buf = "extern const unsigned char pic_%s_data[%d*%d*%d];\r\n" \
                          % (FileNameList[i].split('.')[0], img.width, img.height, bit_point)
            else:
                point_num = 0
                for y in range(img.size[1]):
                    for x in range(img.size[0]):
                        alpha = img_pix[x, y][3]
                        # color = (((img_pix[x, y][2]) >> 3) << 11) | \
                        #         (((img_pix[x, y][1]) >> 2) << 5) | \
                        #         (((img_pix[x, y][0]) >> 3) << 0)
                        color = (((img_pix[x, y][2] * alpha // 0xFF) >> 3) << 11) | \
                                (((img_pix[x, y][1] * alpha // 0xFF) >> 2) << 5) | \
                                (((img_pix[x, y][0] * alpha // 0xFF) >> 3) << 0)
                        if color > 0:
                            point_num += 1
                pic_buf = "extern const unsigned char pic_%s_data[%d*%d];\r\n" \
                          % (FileNameList[i].split('.')[0], point_num, 5)
            picture_data.append(pic_buf)

        pic_buf = "\r\n\r\n"
        picture_data.append(pic_buf)
        pic_buf = "#endif// _PICTURE_ALL_DATA_H\r\n"
        picture_data.append(pic_buf)
        pic_buf = "\r\n"
        picture_data.append(pic_buf)

        with open("picture_all_data.h", 'w+') as pic_data:
            for data in picture_data:
                pic_data.write(data)

    def pic_data_c_file_create(self, FilePathList, FileNameList):
        # picture_data.c file create
        print("create picture_data.c file")
        picture_data = []
        pic_buf = []
        pic_buf.clear()
        picture_data.clear()
        pic_buf = "/*************************************************************\r\n"
        picture_data.append(pic_buf)
        pic_buf = "** this file is all picture data source file\r\n"
        picture_data.append(pic_buf)
        pic_buf = "** by chenlue\r\n"
        picture_data.append(pic_buf)
        pic_buf = "*************************************************************/\r\n"
        picture_data.append(pic_buf)
        pic_buf = "\r\n\r\n"
        picture_data.append(pic_buf)

        for i in range(len(FilePathList)):
            if self.tableWidget_pic_file.item(i, 1).text() == 'spi':
                continue

            image = QImage()
            image.load(FilePathList[i])
            image_pal_len = image.colorCount()

            # print(FilePathList[i])
            img = Image.open(FilePathList[i])
            img_pix = img.load()
            # print("pic width %d, height %d, mode %s" %(img.size[0], img.size[1], img.mode))
            color = 0
            alpha = 0
            bit_point = 0
            pos = 0
            last_pos = 0
            if img.mode == 'RGBA':
                if self.tableWidget_pic_file.item(i, 0).text() == 'yes':
                    bit_point = self.pixel_byte+1
                elif self.tableWidget_pic_file.item(i, 0).text() == 'pAA':
                    bit_point = 4
                elif self.tableWidget_pic_file.item(i, 0).text() == 'point':
                    bit_point = 4
                else:
                    bit_point = self.pixel_byte
            elif img.mode == 'RGB':
                bit_point = self.pixel_byte
            elif img.mode == 'LA':
                bit_point = self.pixel_byte
            elif img.mode == 'P' or img.mode == 'L':
                bit_point = 1

            if (bit_point == 1):
                pic_buf = "const unsigned char pic_%s_data[%d*%d*%d+2+%d*%d] = \r\n{\r\n\t" \
                          % (FileNameList[i].split('.')[0], img.size[0], img.size[1], bit_point, image_pal_len, self.pixel_byte)
            elif (bit_point == 2) or (bit_point == 3):
                pic_buf = "const unsigned char pic_%s_data[%d*%d*%d] = \r\n{\r\n\t" \
                          % (FileNameList[i].split('.')[0], img.width, img.height, bit_point)
            else:
                point_num = 0
                for y in range(img.size[1]):
                    for x in range(img.size[0]):
                        alpha = img_pix[x, y][3]
                        # color = (((img_pix[x, y][2]) >> 3) << 11) | \
                        #         (((img_pix[x, y][1]) >> 2) << 5) | \
                        #         (((img_pix[x, y][0]) >> 3) << 0)
                        color = (((img_pix[x, y][2] * alpha // 0xFF) >> 3) << 11) | \
                                (((img_pix[x, y][1] * alpha // 0xFF) >> 2) << 5) | \
                                (((img_pix[x, y][0] * alpha // 0xFF) >> 3) << 0)
                        if color > 0:
                            point_num += 1
                pic_buf = "const unsigned char pic_%s_data[%d*%d] = \r\n{\r\n\t" \
                          % (FileNameList[i].split('.')[0], point_num, 5)
            picture_data.append(pic_buf)

            x_align_size = (img.size[0] + 3) / 4 * 4
            for y in range(img.size[1]):
                for x in range(img.size[0]):
                    if img.mode == 'RGBA':
                        if bit_point == 3:
                            alpha = img_pix[x, y][3]
                            color = ((img_pix[x, y][2] >> 3) << 11) | \
                                    ((img_pix[x, y][1] >> 2) << 5) | \
                                    ((img_pix[x, y][0] >> 3) << 0)
                        else:
                            alpha = img_pix[x, y][3]
                            # color = (((img_pix[x, y][2]) >> 3) << 11) | \
                            #         (((img_pix[x, y][1]) >> 2) << 5) | \
                            #         (((img_pix[x, y][0]) >> 3) << 0)
                            color = (((img_pix[x, y][2] * alpha // 0xFF) >> 3) << 11) | \
                                    (((img_pix[x, y][1] * alpha // 0xFF) >> 2) << 5) | \
                                    (((img_pix[x, y][0] * alpha // 0xFF) >> 3) << 0)
                    elif img.mode == 'RGB':
                        color = ((img_pix[x, y][2] >> 3) << 11) | \
                                ((img_pix[x, y][1] >> 2) << 5) | \
                                ((img_pix[x, y][0] >> 3) << 0)
                    elif img.mode == 'LA':
                        color = ((img_pix[x, y][0] >> 0) << 8) | \
                                ((img_pix[x, y][1] >> 0) << 0)
                    elif img.mode == 'L' or img.mode == 'P':
                        color = ((img_pix[x, y] >> 0) << 0)

                    if (pos % 16 == 0) and (pos != last_pos):
                        last_pos = pos
                        pic_buf = "\r\n\t"
                        picture_data.append(pic_buf)

                    if img.mode == 'RGBA':
                        if bit_point == 3:
                            pic_buf = "0x%02X, 0x%02X, 0x%02X, " % (alpha, (color >> 8) & 0xff, (color >> 0) & 0xff)
                            pos += 3
                        elif bit_point == 4:
                            if color <= 0:
                                pic_buf = ""
                            else:
                                pic_buf = "0x%02X, 0x%02X, 0x%02X, 0x%02X, 0x%02X, " \
                                          % (x, y, alpha, (color >> 8) & 0xff, (color >> 0) & 0xff)
                                pos += 5
                        else:
                            pic_buf = "0x%02X, 0x%02X, " \
                                      % ((color >> 8) & 0xff, (color >> 0) & 0xff)
                            pos += 2
                    elif img.mode == 'RGB' or img.mode == 'LA':
                        pic_buf = "0x%02X, 0x%02X, " \
                                  % ((color >> 8) & 0xff, (color >> 0) & 0xff)
                        pos += 2
                    elif img.mode == 'L' or img.mode == 'P':
                        pic_buf = "0x%02X, " \
                                  % ((color >> 0) & 0xff)
                        pos += 1

                    picture_data.append(pic_buf)

            if img.mode == 'P':
                img_pal = list(img.getpalette())
                imgpal_len = image_pal_len # len(img_pal) // 3
                # print(img_pal)
                # print(imgpal_len)
                pic_buf = "\r\n\t0x%02X, 0x%02X,\r\n\t" % ((imgpal_len >> 0) & 0xff, (imgpal_len >> 8) & 0xff)
                picture_data.append(pic_buf)

                pos = 0
                last_pos = 0
                for pal_index in range(imgpal_len):
                    if (pos % 16) == 0 and (pos != last_pos):
                        last_pos = pos
                        pic_buf = "\r\n\t"
                        picture_data.append(pic_buf)
                    r = img_pal[pal_index * 3 + 0] >> 3
                    g = img_pal[pal_index * 3 + 1] >> 2
                    b = img_pal[pal_index * 3 + 2] >> 3
                    table = (r << 0) | (g << 5) | (b << 11)
                    pic_buf = "0x%02X, 0x%02X, " % ((table >> 8) & 0xff, (table >> 0) & 0xff)
                    picture_data.append(pic_buf)
                    pos += 2

            pic_buf = "\r\n};\r\n\r\n"
            picture_data.append(pic_buf)

        with open("picture_data.c", 'w+') as pic_data:
            for data in picture_data:
                pic_data.write(data)

    def pic_data_h_file_create(self, FilePathList, FileNameList):
        # picture_data.h file create
        print("create picture_data.h file")
        picture_data = []
        pic_buf = []
        pic_buf.clear()
        picture_data.clear()
        pic_buf = "/*************************************************************\r\n"
        picture_data.append(pic_buf)
        pic_buf = "** this file is all picture data head file\r\n"
        picture_data.append(pic_buf)
        pic_buf = "** by chenlue\r\n"
        picture_data.append(pic_buf)
        pic_buf = "*************************************************************/\r\n"
        picture_data.append(pic_buf)
        pic_buf = "#ifndef _PICTURE_DATA_H\r\n"
        picture_data.append(pic_buf)
        pic_buf = "#define _PICTURE_DATA_H\r\n"
        picture_data.append(pic_buf)
        pic_buf = "\r\n\r\n"
        picture_data.append(pic_buf)

        for i in range(len(FilePathList)):
            if self.tableWidget_pic_file.item(i, 1).text() == 'spi':
                continue

            image = QImage()
            image.load(FilePathList[i])
            image_pal_len = image.colorCount()

            # print(FilePathList[i])
            img = Image.open(FilePathList[i])
            img_pix = img.load()
            # print("pic width %d, height %d, mode %s" %(img.size[0], img.size[1], img.mode))
            bit_point = 0
            if img.mode == 'RGBA':
                if self.tableWidget_pic_file.item(i, 0).text() == 'yes':
                    bit_point = self.pixel_byte+1
                elif self.tableWidget_pic_file.item(i, 0).text() == 'pAA':
                    bit_point = 4
                elif self.tableWidget_pic_file.item(i, 0).text() == 'point':
                    bit_point = 4
                else:
                    bit_point = self.pixel_byte
            elif img.mode == 'RGB':
                bit_point = self.pixel_byte
            elif img.mode == 'LA':
                bit_point = self.pixel_byte
            elif img.mode == 'P' or img.mode == 'L':
                bit_point = 1

            if (bit_point == 1):
                pic_buf = "extern const unsigned char pic_%s_data[%d*%d*%d+2+%d*%d];\r\n" \
                          % (FileNameList[i].split('.')[0], img.size[0], img.size[1], bit_point, image_pal_len, self.pixel_byte)
            elif (bit_point == 2) or (bit_point == 3):
                pic_buf = "extern const unsigned char pic_%s_data[%d*%d*%d];\r\n" \
                          % (FileNameList[i].split('.')[0], img.width, img.height, bit_point)
            else:
                point_num = 0
                for y in range(img.size[1]):
                    for x in range(img.size[0]):
                        alpha = img_pix[x, y][3]
                        # color = (((img_pix[x, y][2]) >> 3) << 11) | \
                        #         (((img_pix[x, y][1]) >> 2) << 5) | \
                        #         (((img_pix[x, y][0]) >> 3) << 0)
                        color = (((img_pix[x, y][2] * alpha // 0xFF) >> 3) << 11) | \
                                (((img_pix[x, y][1] * alpha // 0xFF) >> 2) << 5) | \
                                (((img_pix[x, y][0] * alpha // 0xFF) >> 3) << 0)
                        if color > 0:
                            point_num += 1
                pic_buf = "extern const unsigned char pic_%s_data[%d*%d];\r\n" \
                          % (FileNameList[i].split('.')[0], point_num, 5)
            picture_data.append(pic_buf)

        pic_buf = "\r\n\r\n"
        picture_data.append(pic_buf)
        pic_buf = "#endif// _PICTURE_DATA_H\r\n"
        picture_data.append(pic_buf)
        pic_buf = "\r\n"
        picture_data.append(pic_buf)

        with open("picture_data.h", 'w+') as pic_data:
            for data in picture_data:
                pic_data.write(data)

    def pic_c_file_create(self, FilePathList, FileNameList):
        # picture.c file create
        print("create picture.c file")
        picture_data = []
        pic_buf = []
        pic_buf.clear()
        picture_data.clear()
        pic_buf = "/*************************************************************\r\n"
        picture_data.append(pic_buf)
        pic_buf = "** this file is all picture struct information source file\r\n"
        picture_data.append(pic_buf)
        pic_buf = "** by chenlue\r\n"
        picture_data.append(pic_buf)
        pic_buf = "*************************************************************/\r\n"
        picture_data.append(pic_buf)
        pic_buf = "#include \"picture.h\"\r\n"
        picture_data.append(pic_buf)
        pic_buf = "#include \"picture_data.h\"\r\n"
        picture_data.append(pic_buf)
        pic_buf = "\r\n\r\n"
        picture_data.append(pic_buf)

        pos = 0
        point_num = 0
        for i in range(len(FilePathList)):

            image = QImage()
            image.load(FilePathList[i])
            image_pal_len = image.colorCount()

            # print(FilePathList[i])
            img = Image.open(FilePathList[i])
            img_pix = img.load()
            # print("pic width %d, height %d, mode %s" %(img.size[0], img.size[1], img.mode))
            alpha = 0
            bit_point = 0

            pic_buf = "const picture_info_struct pic_%s_info = {\r\n" \
                        %(FileNameList[i].split('.')[0])
            picture_data.append(pic_buf)

            if (self.tableWidget_pic_file.item(i, 1).text() == 'spi'):
                pic_buf = "\t.addr = (const unsigned char *)0x%08X,\r\n" %(pos)

                if img.mode == 'RGBA':
                    if self.tableWidget_pic_file.item(i, 0).text() == 'yes':
                        pos += img.width*img.height*(self.pixel_byte+1)
                    elif self.tableWidget_pic_file.item(i, 0).text() == 'pAA':
                        point_num = 0
                        for y in range(img.size[1]):
                            for x in range(img.size[0]):
                                alpha = img_pix[x, y][3]
                                # color = (((img_pix[x, y][2]) >> 3) << 11) | \
                                #         (((img_pix[x, y][1]) >> 2) << 5) | \
                                #         (((img_pix[x, y][0]) >> 3) << 0)
                                color = (((img_pix[x, y][2] * alpha // 0xFF) >> 3) << 11) | \
                                        (((img_pix[x, y][1] * alpha // 0xFF) >> 2) << 5) | \
                                        (((img_pix[x, y][0] * alpha // 0xFF) >> 3) << 0)
                                if color > 0:
                                    point_num += 1
                        pos += point_num*5
                    elif self.tableWidget_pic_file.item(i, 0).text() == 'point':
                        point_num = 0
                        for y in range(img.size[1]):
                            for x in range(img.size[0]):
                                alpha = img_pix[x, y][3]
                                # color = (((img_pix[x, y][2]) >> 3) << 11) | \
                                #         (((img_pix[x, y][1]) >> 2) << 5) | \
                                #         (((img_pix[x, y][0]) >> 3) << 0)
                                color = (((img_pix[x, y][2] * alpha // 0xFF) >> 3) << 11) | \
                                        (((img_pix[x, y][1] * alpha // 0xFF) >> 2) << 5) | \
                                        (((img_pix[x, y][0] * alpha // 0xFF) >> 3) << 0)
                                if color > 0:
                                    point_num += 1
                        pos += point_num * 5
                    else:
                        pos += img.width*img.height*self.pixel_byte
                elif img.mode == 'RGB':
                    pos += img.width*img.height*self.pixel_byte
                elif img.mode == 'LA':
                    pos += img.width*img.height*self.pixel_byte
                elif img.mode == 'P' or img.mode == 'L':
                    pos += img.width*img.height+2+(image_pal_len)*self.pixel_byte
            else:
                pic_buf = "\t.addr = (const unsigned char *)pic_%s_data,\r\n" %(FileNameList[i].split('.')[0])
            picture_data.append(pic_buf)

            if img.mode == 'RGBA':
                if self.tableWidget_pic_file.item(i, 0).text() == 'pAA':
                    pic_buf = "\t.width = (%d<<8)|%d,\r\n" % (img.width, img.height)
                    picture_data.append(pic_buf)

                    pic_buf = "\t.height = %d,\r\n" % (point_num*5)
                    picture_data.append(pic_buf)
                elif self.tableWidget_pic_file.item(i, 0).text() == 'point':
                    pic_buf = "\t.width = (%d<<8)|%d,\r\n" % (img.width, img.height)
                    picture_data.append(pic_buf)

                    pic_buf = "\t.height = %d,\r\n" % (point_num * 5)
                    picture_data.append(pic_buf)
                else:
                    pic_buf = "\t.width = %d,\r\n" % (img.width)
                    picture_data.append(pic_buf)

                    pic_buf = "\t.height = %d,\r\n" % (img.height)
                    picture_data.append(pic_buf)
            else:
                pic_buf = "\t.width = %d,\r\n" % (img.width)
                picture_data.append(pic_buf)

                pic_buf = "\t.height = %d,\r\n" % (img.height)
                picture_data.append(pic_buf)

            if img.mode == 'RGBA':
                if self.tableWidget_pic_file.item(i, 0).text() == 'yes':
                    pic_buf = "\t.alpha = 1,\r\n"
                elif self.tableWidget_pic_file.item(i, 0).text() == 'pAA':
                    pic_buf = "\t.alpha = 4,\r\n"
                elif self.tableWidget_pic_file.item(i, 0).text() == 'point':
                    pic_buf = "\t.alpha = 4,\r\n"
                else:
                    pic_buf = "\t.alpha = 0,\r\n"
            elif img.mode == 'RGB':
                pic_buf = "\t.alpha = 0,\r\n"
            elif img.mode == 'LA':
                pic_buf = "\t.alpha = 0,\r\n"
            elif img.mode == 'P' or img.mode == "L":
                pic_buf = "\t.alpha = 3,\r\n"
            picture_data.append(pic_buf)

            if self.tableWidget_pic_file.item(i, 1).text() == 'spi':
                pic_buf = "\t.external_flag = 1,\r\n"
            else:
                pic_buf = "\t.external_flag = 0,\r\n"
            picture_data.append(pic_buf)

            pic_buf = "\t};\r\n\r\n"
            picture_data.append(pic_buf)

        with open("picture.c", 'w+') as pic_data:
            for data in picture_data:
                pic_data.write(data)

    def pic_h_file_create(self, FilePathList, FileNameList, file_len_list, crc16, pic_offset):
        # picture.c file create
        print("create picture.h file")
        picture_data = []
        pic_buf = []
        pic_buf.clear()
        picture_data.clear()
        pic_buf = "/*************************************************************\r\n"
        picture_data.append(pic_buf)
        pic_buf = "** this file is all picture struct information head file\r\n"
        picture_data.append(pic_buf)
        pic_buf = "** by chenlue\r\n"
        picture_data.append(pic_buf)
        pic_buf = "*************************************************************/\r\n"
        picture_data.append(pic_buf)
        pic_buf = "#ifndef _PICTURE_H\r\n"
        picture_data.append(pic_buf)
        pic_buf = "#define _PICTURE_H\r\n"
        picture_data.append(pic_buf)
        pic_buf = "\r\n\r\n"
        picture_data.append(pic_buf)

        pic_buf = "#define PIC_CRC16\t\t0x%04X\r\n" %(crc16&0xffff)
        picture_data.append(pic_buf)
        pic_buf = "#define PIC_HEAD_SIZE\t16\r\n"
        picture_data.append(pic_buf)
        pic_buf = "#define PIC_OFFSET\t\t0x%08X\r\n" %(pic_offset)
        picture_data.append(pic_buf)

        pic_buf = "\r\n\r\n"
        picture_data.append(pic_buf)

        for i in range(len(file_len_list)):
            picture_data.append(file_len_list[i])

        pic_buf = "\r\n\r\n"
        picture_data.append(pic_buf)

        picture_data.append("typedef struct\r\n")
        picture_data.append("{\r\n")
        picture_data.append("\tconst unsigned char *addr;\r\n")
        picture_data.append("\tconst unsigned short width;\r\n")
        picture_data.append("\tconst unsigned short height;\r\n")
        picture_data.append("\tconst unsigned char alpha;//0: no alpha, 1: has alpha, 2:point display, 3:8bit(256 color.)\r\n")
        picture_data.append("\tconst unsigned char external_flag;//0: mcu flash, 1: external spi flash or emmc.\r\n")
        picture_data.append("}picture_info_struct;\r\n")
        picture_data.append("\r\n\r\n")

        for i in range(len(FileNameList)):
            pic_buf = "extern const picture_info_struct pic_%s_info;\r\n" \
                        %(FileNameList[i].split('.')[0])
            picture_data.append(pic_buf)

        pic_buf = "\r\n\r\n"
        picture_data.append(pic_buf)
        pic_buf = "#endif //_PICTURE_H\r\n"
        picture_data.append(pic_buf)
        pic_buf = "\r\n"
        picture_data.append(pic_buf)

        with open("picture.h", 'w+') as pic_data:
            for data in picture_data:
                pic_data.write(data)

    def start_btn_clicked(self):
        checkFilePathList = []
        checkFileNameList = []
        checkFilePathList_bin = []
        checkFileNameList_bin = []

        for i in range(len(self.filepath_list)):
            checkFilePathList.append(self.filepath_list[i])
            checkFileNameList.append(self.filename_list[i])
        for i in range(len(self.filepath_bin_list)):
            checkFilePathList_bin.append(self.filepath_bin_list[i])
            checkFileNameList_bin.append(self.filename_bin_list[i])

        fileLenList_bin, pic_offset, crc_16 = self.pic_and_font_bin_file_create(checkFilePathList, checkFileNameList, checkFilePathList_bin, checkFileNameList_bin)
        self.pic_all_data_c_file_create(checkFilePathList, checkFileNameList)
        self.pic_all_data_h_file_create(checkFilePathList, checkFileNameList)
        self.pic_data_c_file_create(checkFilePathList, checkFileNameList)
        self.pic_data_h_file_create(checkFilePathList, checkFileNameList)
        self.pic_c_file_create(checkFilePathList, checkFileNameList)
        self.pic_h_file_create(checkFilePathList, checkFileNameList, fileLenList_bin, crc_16, pic_offset)

        QMessageBox.about(self, '字库生成', '字库生成成功')


# 继承threading.Thread
'''
通过线程读取串口数据在速度比较慢的情况下可以完美工作，
但是在快速的接收数据时会出现卡死的情况，也许是线程读取部分的逻辑没有弄好，
所以我换成了2ms定时读取
'''
class ser_recvthread(threading.Thread):
    def __init__(self, func):
        super(ser_recvthread, self).__init__()
        self.func = func
        self.__flag = threading.Event()  # 用于暂停线程的标识
        self.__flag.set()  # 设置为True
        self.__running = threading.Event()  # 用于停止线程的标识
        self.__running.set()  # 将running设置为True

    def run(self):
        while self.__running.isSet():
            self.__flag.wait()  # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
            self.func()

    def pause(self):
        self.__flag.clear()  # 设置为False, 让线程阻塞

    def resume(self):
        self.__flag.set()  # 设置为True, 让线程停止阻塞

    def stop(self):
        self.__flag.clear()
        self.__running.clear()  # 设置为False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Little_tool()
    window.show()
    sys.exit(app.exec_())