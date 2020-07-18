import sys
from PyQt5.QtWidgets import (QWidget, QApplication, QGridLayout, QRadioButton, QVBoxLayout, QTabWidget, QFormLayout,
    QLabel, QLineEdit, QPushButton, QFileDialog, QMainWindow, QAction)

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class Tab(QTabWidget):
    def __init__(self):
        super().__init__()
        self.tab1 = QWidget()

        self.addTab(self.tab1, 'Excel deal')

        self.tab1UI()

    def tab1UI(self):
        tab1_lay = QGridLayout()
        self.tab1.setLayout(tab1_lay)

        self.output_title = QLabel('dest')
        tab1_lay.addWidget(self.output_title, 0, 0)

        self.output_file = QLineEdit()
        self.output_file.setGeometry(20, 20, 100, 20)
        tab1_lay.addWidget(self.output_file, 0, 1)

        self.DirButton = QPushButton(self)
        self.DirButton.setGeometry(self.output_file.width() + 5, 20, 20, 20)
        self.DirButton.setObjectName('queryButton')
        self.DirButton.setText('...')
        self.DirButton.setStatusTip('Click to select file')
        self.DirButton.clicked.connect(self.file_select)
        tab1_lay.addWidget(self.DirButton, 0, 2)

        self.statusTip()

    def file_select(self):
        files, ok1 = QFileDialog.getOpenFileNames(self,
                                                  "多文件选择",
                                                  "./",
                                                  "All Files (*);;Text Files (*.txt)")
        self.output_file.setText(files[0])
        print(files, ok1)



class TabWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.TabWidgetUI()

    def TabWidgetUI(self):
        # 表单布局
        layout = QFormLayout()
        self.setLayout(layout)

        tabwidget = Tab()
        layout.addRow(tabwidget)

class Little_tool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Little Tool')
        self.setGeometry(500, 500, 500, 400)

        table = TabWidget()

        excelAction = QAction('&Excel', self)
        excelAction.setShortcut('Ctrl+E')
        excelAction.setStatusTip('Excel handle')
        excelAction.triggered.connect(table.TabWidgetUI)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&功能')
        fileMenu.addAction(excelAction)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Little_tool()
    demo.show()
    sys.exit(app.exec_())