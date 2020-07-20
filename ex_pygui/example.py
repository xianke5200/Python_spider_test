from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QButtonGroup, QFrame, QToolButton, QStackedLayout, \
    QWidget, QStatusBar, QBoxLayout, QLabel, QDesktopWidget, QMessageBox, QMenu, QAction
from PyQt5.QtGui import QDesktopServices, QFont, QIcon
from PyQt5.QtCore import Qt

import sys


class Demo(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("测试")
        # 窗口大小
        self.resize(1400, 800)
        # self.setFixedSize(1500, 600)  # 设置窗口为固定尺寸， 此时窗口不可调整大小
        # self.setMinimumSize(1800， 1000)  # 设置窗口最大尺寸
        # self.setMaximumSize(900， 300)  # 设置窗口最小尺寸
        # self.setWindowFlag(Qt.WindowStaysOnTopHint)   # 设置窗口顶层显示
        # self.setWindowFlags(Qt.FramelessWindowHint)  # 设置无边框窗口样式，不显示最上面的标题栏

        self.content_font = QFont("微软雅黑", 12, QFont.Medium)  # 定义字体样式

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

        # 第一个布局
        self.main_frame1 = QMainWindow()
        self.frame1_bar = QStatusBar()
        self.frame1_bar.setObjectName("frame1_bar")
        self.main_frame1.setStatusBar(self.frame1_bar)
        self.frame1_bar.showMessage("欢迎进入frame1")

        rom_frame = QFrame(self.main_frame1)
        rom_frame.setGeometry(0, 0, self.width(), self.main_frame.height() - 25)
        rom_frame.setFrameShape(QFrame.Panel)
        rom_frame.setFrameShadow(QFrame.Raised)

        # 超链接
        self.super_link = QLabel(rom_frame)
        self.super_link.setText("""
            超链接: <a href="https://blog.csdn.net/s_daqing">点击打开查看</a>
            """)
        self.super_link.setGeometry(20, 30, 300, 25)
        self.super_link.setFont(self.content_font)  # 使用字体样式
        self.super_link.setOpenExternalLinks(True)  # 使其成为超链接
        self.super_link.setTextInteractionFlags(Qt.TextBrowserInteraction)  # 双击可以复制文本

        self.start_btn = QPushButton("开 始", rom_frame)
        self.start_btn.setGeometry(self.width() * 0.7, self.height() * 0.8, 100, 40)
        # self.start_btn.clicked.connect(self.start_btn_click)
        self.quit_btn = QPushButton("退 出", rom_frame)
        self.quit_btn.setGeometry(self.width() * 0.85, self.height() * 0.8, 100, 40)
        self.quit_btn.setStatusTip("点击关闭程序")
        # self.quit_btn.clicked.connect(QCoreApplication.instance().quit)  # 点击退出可以直接退出
        self.quit_btn.clicked.connect(self.close)  # 点击退出按钮的退出槽函数

        #rom_frame1 = QFrame()
        #rom_frame1.setFrameShape(QFrame.Panel)
        #rom_frame1.setFrameShadow(QFrame.Raised)

        #rom_frame2 = QFrame()
        #rom_frame2.setFrameShape(QFrame.Panel)
        #rom_frame2.setFrameShadow(QFrame.Raised)

        # 创建布局管理器
        self.layout1 = QBoxLayout(QBoxLayout.TopToBottom)

        # 给管理器对象设置父控件
        rom_frame.setLayout(self.layout1)
        self.main_frame1.setCentralWidget(rom_frame)

        # 把子控件添加到布局管理器中
        #self.layout1.addWidget(rom_frame1, 1)
        #self.layout1.addWidget(rom_frame2, 1)

        self.layout1.setContentsMargins(0, 0, 0, 0)  # 设置布局的左上右下外边距
        self.layout1.setSpacing(0)  # 设置子控件的内边距

        frame1_bar_frame = QFrame(self.main_frame1)
        frame1_bar_frame.setGeometry(0, self.main_frame.height(), self.width(), 25)

        # 第二个布局
        self.main_frame2 = QMainWindow()
        self.frame2_bar = QStatusBar()
        self.frame2_bar.setObjectName("frame2_bar")
        self.main_frame2.setStatusBar(self.frame2_bar)
        self.frame2_bar.showMessage("欢迎进入frame2")

        custom_frame = QFrame(self.main_frame2)
        custom_frame.setGeometry(0, 0, self.width(), self.main_frame.height() - 25)
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
        self.layout2 = QBoxLayout(QBoxLayout.TopToBottom)

        # 给管理器对象设置父控件
        custom_frame.setLayout(self.layout2)
        """
        使用了父类为QMainWindow的话，在里面使用布局类，QGridLayout， QHBoxLayout ，QVBoxLayout 等等时，发现不好用，
        加上下面这句代码就可以了，QMainWindow对象.setCentralWidget(这里填布局管理器的父控件对象)
        """
        self.main_frame2.setCentralWidget(custom_frame)

        # 把子控件添加到布局管理器中
        self.layout2.addWidget(custom_frame1, 1)
        self.layout2.addWidget(custom_frame2, 1)
        self.layout2.addWidget(custom_frame3, 1)

        self.layout2.setContentsMargins(0, 0, 0, 0)  # 设置布局的左上右下外边距
        self.layout2.setSpacing(0)  # 设置子控件的内边距

        frame2_bar_frame = QFrame(self.main_frame2)
        frame2_bar_frame.setGeometry(0, self.main_frame.height(), self.width(), 25)

        # 把两个布局放进去
        self.stacked_layout.addWidget(self.main_frame1)
        self.stacked_layout.addWidget(self.main_frame2)


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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Demo()
    window.show()
    sys.exit(app.exec_())
