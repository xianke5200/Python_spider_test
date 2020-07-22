
import xlrd
import xlwt
from PyQt5 import QtWidgets
from PyQt5.QtCore import QUrl, QRect, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QButtonGroup, QFrame, QToolButton, QStackedLayout, \
    QWidget, QStatusBar, QBoxLayout, QLabel, QDesktopWidget, QMessageBox, QMenu, QAction, QFileDialog, QLineEdit, \
    QGridLayout, QComboBox, QDialog
from PyQt5.QtGui import QDesktopServices, QFont, QIcon
from PyQt5.QtCore import Qt
import time

import sys
from ex_pygui.excel_db import excel_db

class Little_tool(QWidget):
    def __init__(self, n = 1):
        super().__init__()

        self.setWindowTitle("测试")
        # 窗口大小
        #self.resize(800, 600)
        self.setFixedSize(800, 600)  # 设置窗口为固定尺寸， 此时窗口不可调整大小
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
            self.ed.dbClose()#关闭数据库
            self.ed.dbRemove()#删除数据库文件
            event.accept()
        else:
            event.ignore()


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
        self.window2_btn.setText("window2")
        self.window2_btn.setObjectName("menu_btn")
        self.window2_btn.resize(100, 25)
        self.window2_btn.move(self.window1_btn.width(), 0)
        self.window2_btn.clicked.connect(self.click_window2)
        self.window2_btn.setAutoRaise(True)

        self.btn_group = QButtonGroup(self.frame_tool)
        self.btn_group.addButton(self.window1_btn, 1)
        self.btn_group.addButton(self.window2_btn, 2)

        # 1.3 帮助下拉菜单栏
        # 创建帮助工具按钮
        help_btn = QToolButton(self.frame_tool)
        help_btn.setText("帮助")
        help_btn.setObjectName("menu_btn")
        help_btn.resize(100, 25)
        help_btn.move(self.window2_btn.x() + self.window2_btn.width(), 0)
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

        # 把两个布局放进去
        self.stacked_layout.addWidget(main_frame1)
        self.stacked_layout.addWidget(main_frame2)

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



    def window1_UI(self, frame):
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
        self.layout1 = QBoxLayout(QBoxLayout.TopToBottom)
        tab_lay = QBoxLayout(QBoxLayout.LeftToRight)
        tab_lay1 = QBoxLayout(QBoxLayout.LeftToRight)
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
        start_btn = QPushButton("开 始", self.rom_frame)
        start_btn.setGeometry(self.width() * 0.3, self.height() * 0.85, 100, 40)
        start_btn.clicked.connect(self.write_excel_file)
        quit_btn = QPushButton("退 出", self.rom_frame)
        quit_btn.setGeometry(self.width() * 0.6, self.height() * 0.85, 100, 40)
        quit_btn.setStatusTip("点击关闭程序")
        # self.quit_btn.clicked.connect(QCoreApplication.instance().quit)  # 点击退出可以直接退出
        quit_btn.clicked.connect(self.close)  # 点击退出按钮的退出槽函数

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

    def window2_UI(self, frame):
        # 第二个布局
        main_frame2 = QMainWindow()
        frame2_bar = QStatusBar()
        frame2_bar.setObjectName("frame2_bar")
        main_frame2.setStatusBar(frame2_bar)
        frame2_bar.showMessage("欢迎进入frame2")

        custom_frame = QFrame(main_frame2)
        custom_frame.setGeometry(0, 0, self.width(), frame.height() - 25)
        custom_frame.setFrameShape(QFrame.Panel)
        custom_frame.setFrameShadow(QFrame.Raised)

        self.gridLayout = QGridLayout(custom_frame)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.ser_databit = QtWidgets.QComboBox(custom_frame)
        self.ser_databit.setObjectName("ser_databit")
        self.gridLayout.addWidget(self.ser_databit, 5, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(custom_frame)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 6, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(custom_frame)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 7, 0, 1, 1)
        self.ser_display_lineedit = QtWidgets.QLineEdit(custom_frame)
        self.ser_display_lineedit.setObjectName("ser_display")
        self.gridLayout.addWidget(self.ser_display_lineedit, 6, 2, 1, 4)
        self.ser_refresh = QtWidgets.QPushButton(custom_frame)
        self.ser_refresh.setObjectName("ser_refresh")
        self.gridLayout.addWidget(self.ser_refresh, 1, 3, 1, 1)
        self.ser_stopbit = QtWidgets.QComboBox(custom_frame)
        self.ser_stopbit.setObjectName("ser_stopbit")
        self.gridLayout.addWidget(self.ser_stopbit, 6, 1, 1, 1)
        self.ser_sendtimer = QtWidgets.QCheckBox(custom_frame)
        self.ser_sendtimer.setObjectName("ser_sendtimer")
        self.gridLayout.addWidget(self.ser_sendtimer, 4, 2, 1, 1)
        self.ser_checkbit = QtWidgets.QComboBox(custom_frame)
        self.ser_checkbit.setObjectName("ser_checkbit")
        self.gridLayout.addWidget(self.ser_checkbit, 7, 1, 1, 1)
        self.ser_hex_display = QtWidgets.QCheckBox(custom_frame)
        self.ser_hex_display.setObjectName("ser_hex_display")
        self.gridLayout.addWidget(self.ser_hex_display, 1, 4, 1, 2)
        self.label_7 = QtWidgets.QLabel(custom_frame)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 5, 2, 1, 4)
        self.ser_num = QtWidgets.QComboBox(custom_frame)
        self.ser_num.setObjectName("ser_num")
        self.gridLayout.addWidget(self.ser_num, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(custom_frame)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(custom_frame)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 4, 4, 1, 1)
        self.ser_clearbtn = QtWidgets.QPushButton(custom_frame)
        self.ser_clearbtn.setObjectName("ser_clearbtn")
        self.gridLayout.addWidget(self.ser_clearbtn, 1, 6, 1, 1)
        self.textEdit = QtWidgets.QTextEdit(custom_frame)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 7)
        self.label = QtWidgets.QLabel(custom_frame)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.ser_file_select = QtWidgets.QLineEdit(custom_frame)
        self.ser_file_select.setObjectName("ser_file_select")
        self.gridLayout.addWidget(self.ser_file_select, 11, 0, 1, 6)
        self.set_openbtn = QtWidgets.QPushButton(custom_frame)
        self.set_openbtn.setObjectName("set_openbtn")
        self.gridLayout.addWidget(self.set_openbtn, 1, 2, 1, 1)
        self.ser_sendbtn = QtWidgets.QPushButton(custom_frame)
        self.ser_sendbtn.setObjectName("ser_sendbtn")
        self.gridLayout.addWidget(self.ser_sendbtn, 5, 6, 1, 1)
        self.ser_sendtmr_time = QtWidgets.QLineEdit(custom_frame)
        self.ser_sendtmr_time.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ser_sendtmr_time.sizePolicy().hasHeightForWidth())
        self.ser_sendtmr_time.setSizePolicy(sizePolicy)
        self.ser_sendtmr_time.setObjectName("ser_sendtmr_time")
        self.gridLayout.addWidget(self.ser_sendtmr_time, 4, 3, 1, 1)
        self.ser_bdrate = QtWidgets.QComboBox(custom_frame)
        self.ser_bdrate.setObjectName("ser_bdrate")
        self.gridLayout.addWidget(self.ser_bdrate, 4, 1, 1, 1)
        self.checkBox_3 = QtWidgets.QCheckBox(custom_frame)
        self.checkBox_3.setObjectName("checkBox_3")
        self.gridLayout.addWidget(self.checkBox_3, 7, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(custom_frame)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 5, 0, 1, 1)
        self.ser_send_filebtn = QtWidgets.QPushButton(custom_frame)
        self.ser_send_filebtn.setObjectName("ser_send_filebtn")
        self.gridLayout.addWidget(self.ser_send_filebtn, 10, 6, 1, 1)
        self.ser_rw_combo = QtWidgets.QComboBox(custom_frame)
        self.ser_rw_combo.setObjectName("ser_rw_combo")
        self.gridLayout.addWidget(self.ser_rw_combo, 10, 5, 1, 1)
        self.ser_rw_checkbox = QtWidgets.QCheckBox(custom_frame)
        self.ser_rw_checkbox.setObjectName("ser_rw_checkbox")
        self.gridLayout.addWidget(self.ser_rw_checkbox, 10, 0, 1, 1)
        self.ser_file_select_btn = QtWidgets.QPushButton(custom_frame)
        self.ser_file_select_btn.setObjectName("ser_file_select_btn")
        self.gridLayout.addWidget(self.ser_file_select_btn, 11, 6, 1, 1)

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
        self.checkBox_3.setText("Hex发送")
        self.label_3.setText("数据位")
        self.ser_send_filebtn.setText("发送文件")
        self.ser_rw_checkbox.setText("选中读写文件")
        self.ser_file_select_btn.setText("...")

        frame2_bar_frame = QFrame(main_frame2)
        frame2_bar_frame.setGeometry(0, frame.height(), self.width(), 25)

        return main_frame2

    def click_window1(self):
        if self.stacked_layout.currentIndex() != 0:
            self.stacked_layout.setCurrentIndex(0)
            #self.frame1_bar.showMessage("欢迎使用")

    def click_window2(self):
        if self.stacked_layout.currentIndex() != 1:
            self.stacked_layout.setCurrentIndex(1)
            #self.frame2_bar.showMessage("欢迎进入frame2")
            #QDesktopServices.openUrl(QUrl("https://www.csdn.net/"))  # 点击window2按钮后，执行这个槽函数的时候，会在浏览器自动打开这个网址

    def click_feedback(self, event):
        QMessageBox.about(self, "反馈", "抱歉无法反馈")

    def click_about(self, event):
        #QMessageBox.about(self, "关于", "抱歉，没有文档")
        from ex_pygui.time_display import Ui_Dialog  # 显示自定义的弹出窗口
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

    def add_file_select(self):
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
            self.combo_list[index-1].addItems(read_data[1:])
            self.combo_list[index-1].activated[str].connect(lambda str, param = index : self.write_sqlite(str, param))

    def read_excel_file(self, filename, start_row, end_row, start_col, end_col):
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

            for dest_all_data_row in range(len(dest_all_data)):
                for j in range(len(dest_all_data)):
                    if j == mySheet_dest_col:
                        print(dest_all_data_row, j, dest_col_data[dest_all_data_row])
                        mySheet.write(dest_all_data_row, j, dest_col_data[dest_all_data_row])
                    else:
                        if(j < len(dest_data[0]) and mySheet_dest_col < len(dest_data[0])):
                            print(dest_all_data_row, j, dest_data[dest_all_data_row][j])
                            mySheet.write(dest_all_data_row, j, dest_data[dest_all_data_row][j])
        now = time.localtime()
        QMessageBox.about(self, "结束", "文件已复制完成")
        workbook.save('SN_设备侧_固件标题语言'+'%s%s%s%s%s%s' %(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)+'.xls')

    def write_sqlite(self, str, param):
        self.ed.delete(param)
        self.ed.insert(self.lineedit_list[param].text(), str, param)
        self.ed.dbDump()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Little_tool()
    window.show()
    sys.exit(app.exec_())