#!usr/bin/python3
#-*- coding: utf-8 -*-

from PyQt5.QtCore import QUrl, QRect
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QButtonGroup, QFrame, QToolButton, QStackedLayout, \
    QWidget, QStatusBar, QBoxLayout, QLabel, QDesktopWidget, QMessageBox, QMenu, QAction, QFileDialog, QLineEdit, \
    QGridLayout, QComboBox
from PyQt5.QtGui import QDesktopServices, QFont, QIcon
from PyQt5.QtCore import Qt

import sys

combox_dict = {'combo1':1, 'combo1':2, 'combo3':3,
               'combo4':4, 'combo5':5, 'combo6':6 }

class Little_tool(QWidget):
    def __init__(self, n = 1):
        super().__init__()

        self.setWindowTitle("测试")
        # 窗口大小
        self.resize(600, 800)
        # self.setFixedSize(1500, 600)  # 设置窗口为固定尺寸， 此时窗口不可调整大小
        # self.setMinimumSize(1800， 1000)  # 设置窗口最大尺寸
        # self.setMaximumSize(900， 300)  # 设置窗口最小尺寸
        # self.setWindowFlag(Qt.WindowStaysOnTopHint)   # 设置窗口顶层显示
        # self.setWindowFlags(Qt.FramelessWindowHint)  # 设置无边框窗口样式，不显示最上面的标题栏

        self.content_font = QFont("微软雅黑", 12, QFont.Medium)  # 定义字体样式

        self.language_dict = {}
        self.layout_count = n
        self.layout_list = []

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
                                     "确定退出xxxx程序吗？",  # 消息对话框中显示的文本
                                     QMessageBox.Yes | QMessageBox.No,  # 指定按钮的组合 Yes和No
                                     QMessageBox.No  # 默认的按钮焦点,这里默认是No按钮
                                     )
        # 判断按钮的选择
        if reply == QMessageBox.Yes:
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
        self.window1_btn.setText("window1")
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

        main_frame1 = self.window1_UI(self.main_frame)
        main_frame2 = self.window2_UI(self.main_frame)

        # 把两个布局放进去
        self.stacked_layout.addWidget(main_frame1)
        self.stacked_layout.addWidget(main_frame2)

    def window1_UI(self, frame):
        # 第一个布局
        main_frame1 = QMainWindow()
        frame1_bar = QStatusBar()
        frame1_bar.setObjectName("frame1_bar")
        main_frame1.setStatusBar(frame1_bar)
        frame1_bar.showMessage("欢迎进入frame1")

        self.rom_frame = QFrame(main_frame1)
        self.rom_frame.setGeometry(0, 0, self.width(), frame.height() - 25)
        self.rom_frame.setFrameShape(QFrame.Panel)
        self.rom_frame.setFrameShadow(QFrame.Raised)

        # 创建布局管理器
        self.layout1 = QBoxLayout(QBoxLayout.TopToBottom)
        tab_lay = QBoxLayout(QBoxLayout.LeftToRight)
        tab_lay1 = QBoxLayout(QBoxLayout.LeftToRight)

        output_title = QLabel('dest', self.rom_frame)
        output_title.setGeometry(self.width() * 0.1, self.height() * 0.1, 10, 4)
        self.output_file = QLineEdit(self.rom_frame)
        DirButton = QPushButton(self.rom_frame)
        DirButton.setObjectName('query Button')
        DirButton.setText('...')
        DirButton.setStatusTip('Click to select file')
        DirButton.clicked.connect(self.file_select)
        addButton = QPushButton(self.rom_frame)
        addButton.resize(5, 2)
        addButton.setObjectName('add Button')
        addButton.setText('+')
        addButton.setStatusTip('Click to add source select')
        addButton.clicked.connect(self.add_file_select)

        output_title1 = QLabel('src1', self.rom_frame)
        self.output_file1 = QLineEdit(self.rom_frame)
        DirButton1 = QPushButton(self.rom_frame)
        DirButton1.setObjectName('query Button')
        DirButton1.setText('...')
        DirButton1.setStatusTip('Click to select source file')
        DirButton1.clicked.connect(self.file_select)
        combo1 = QComboBox(self.rom_frame)

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
        # self.start_btn.clicked.connect(self.start_btn_click)
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
        tab_lay1.addWidget(combo1, 1)

        # 给管理器对象设置父控件
        self.rom_frame.setLayout(self.layout1)
        main_frame1.setCentralWidget(self.rom_frame)

        self.layout1.setContentsMargins(0, 0, 0, 0)  # 设置布局的左上右下外边距
        self.layout1.setSpacing(0)  # 设置子控件的内边距

        self.layout_list.append(tab_lay)
        self.layout_list.append(tab_lay1)

        #self.layout1.addLayout(tab_lay)
        #self.layout1.addStretch(1)  # 设置空间之间的上下间距
        #self.layout1.addWidget(QLabel('please select the source file'))
        #self.layout1.addLayout(tab_lay1)
        #self.layout1.addStretch(1)  # 设置空间之间的上下间距

        for i in range(len(self.layout_list)):
            self.layout1.addLayout(self.layout_list[i])
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

        custom_frame1 = QFrame()
        custom_frame1.setFrameShape(QFrame.Panel)
        custom_frame1.setFrameShadow(QFrame.Raised)

        custom_frame2 = QFrame()
        custom_frame2.setFrameShape(QFrame.Panel)
        custom_frame2.setFrameShadow(QFrame.Raised)

        custom_frame3 = QFrame()
        custom_frame3.setFrameShape(QFrame.Panel)
        custom_frame3.setFrameShadow(QFrame.Raised)

        # 创建布局管理器
        layout2 = QBoxLayout(QBoxLayout.TopToBottom)

        # 给管理器对象设置父控件
        custom_frame.setLayout(layout2)
        """
        使用了父类为QMainWindow的话，在里面使用布局类，QGridLayout， QHBoxLayout ，QVBoxLayout 等等时，发现不好用，
        加上下面这句代码就可以了，QMainWindow对象.setCentralWidget(这里填布局管理器的父控件对象)
        """
        main_frame2.setCentralWidget(custom_frame)

        # 把子控件添加到布局管理器中
        layout2.addWidget(custom_frame1, 1)
        layout2.addWidget(custom_frame2, 1)
        layout2.addWidget(custom_frame3, 1)

        layout2.setContentsMargins(0, 0, 0, 0)  # 设置布局的左上右下外边距
        layout2.setSpacing(0)  # 设置子控件的内边距

        frame2_bar_frame = QFrame(main_frame2)
        frame2_bar_frame.setGeometry(0, frame.height(), self.width(), 25)

        return main_frame2

    def click_window1(self):
        if self.stacked_layout.currentIndex() != 0:
            self.stacked_layout.setCurrentIndex(0)
            self.frame1_bar.showMessage("欢迎进入frame1")


    def click_window2(self):
        if self.stacked_layout.currentIndex() != 1:
            self.stacked_layout.setCurrentIndex(1)
            self.frame2_bar.showMessage("欢迎进入frame2")
            QDesktopServices.openUrl(QUrl("https://www.csdn.net/"))  # 点击window2按钮后，执行这个槽函数的时候，会在浏览器自动打开这个网址

    def click_feedback(self, event):
        QMessageBox.about(self, "反馈", "使用过程中如有疑问，请联系：xxxx.163.com\r\n\r\n版本：V1.0.1")


    def click_about(self, event):
        QMessageBox.about(self, "关于", "使用文档，请参考：xxxxxx")

    def add_file_select(self):
        self.layout_count += 1
        if(self.layout_count > 8):
            return
        tab_lay_add = QBoxLayout(QBoxLayout.LeftToRight)

        text = 'src%d' %(self.layout_count)
        output_title_add = QLabel(text, self.rom_frame)
        output_file_add = QLineEdit(self.rom_frame)
        DirButton_add = QPushButton(self.rom_frame)
        DirButton_add.setObjectName('query Button')
        DirButton_add.setText('...')
        DirButton_add.setStatusTip('Click to select source file')
        DirButton_add.clicked.connect(self.file_select)
        combo_add = QComboBox(self.rom_frame)

        tab_lay_add.addWidget(output_title_add, 1)
        tab_lay_add.addWidget(output_file_add, 20)
        tab_lay_add.addWidget(DirButton_add, 1)
        tab_lay_add.addWidget(combo_add, 1)

        tab_lay_add.widgetEvent()

        #self.layout1.addWidget(QLabel('please select the source file'))
        #self.layout1.addLayout(tab_lay_add)
        #self.layout1.addStretch(1)#设置空间之间的上下间距

        self.layout_list.append(tab_lay_add)

        for i in range(len(self.layout_list)):
            self.layout1.addLayout(self.layout_list[i])
            self.layout1.setStretch(2*i, 0)
        self.layout1.addStretch(1)  # 设置空间之间的上下间距

        self.rom_frame.update()

    def file_select(self):
        file, ok1 = QFileDialog.getOpenFileName(self,
                                                  "多文件选择",
                                                  "./",
                                                  "All Files (*);;Text Files (*.txt)")
        if ok1:
            #self.output_file.setText(file)
            print(file, ok1, self.layout1.count())
            # 读取excel 文件语言列表

    def read_excel_file(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Little_tool()
    window.show()
    sys.exit(app.exec_())