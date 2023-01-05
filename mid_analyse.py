# -*- coding: utf-8 -*-

##########################################################################
# Form generated from reading UI file 'mid_analyse.ui'
##
# Created by: Qt User Interface Compiler version 6.4.1
##
# WARNING! All changes made in this file will be lost when recompiling UI file!
##########################################################################

# from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
#                             QMetaObject, QObject, QPoint, QRect,
#                             QSize, QTime, QUrl, Qt)
# from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
#                            QFont, QFontDatabase, QGradient, QIcon,
#                            QImage, QKeySequence, QLinearGradient, QPainter,
#                            QPalette, QPixmap, QRadialGradient, QTransform)
# from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QLabel,
# QLineEdit, QPushButton, QSizePolicy, QWidget)

import sys
from PySide6.QtWidgets import QApplication, QWidget, QGroupBox, QPushButton, \
    QLabel, QLineEdit, QHBoxLayout, QFileDialog
from PySide6.QtCore import QRect, QMetaObject, Slot


class Ui_Form(QWidget):
    def __init__(self):
        super().__init__()
        self.groupBox = None
        self.horizontalLayout = None
        self.horizontalLayoutWidget = None
        self.close_button = None
        self.fileChoseButton = None
        self.input_button = None
        self.note_count_label = None
        self.note_count_shower = None
        self.output_button = None

    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(582, 355)
        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 0, 561, 311))
        self.fileChoseButton = QPushButton(self.groupBox)
        self.fileChoseButton.setObjectName(u"file_chose_button")
        self.fileChoseButton.setGeometry(QRect(10, 20, 75, 24))
        self.note_count_label = QLabel(self.groupBox)
        self.note_count_label.setObjectName(u"note_count_label")
        self.note_count_label.setGeometry(QRect(20, 50, 54, 16))
        self.note_count_shower = QLineEdit(self.groupBox)
        self.note_count_shower.setObjectName(u"note_count_shower")
        self.note_count_shower.setGeometry(QRect(70, 50, 113, 20))
        self.horizontalLayoutWidget = QWidget(Form)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 310, 561, 41))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.input_button = QPushButton(self.horizontalLayoutWidget)
        self.input_button.setObjectName(u"input_button")

        self.horizontalLayout.addWidget(self.input_button)

        self.output_button = QPushButton(self.horizontalLayoutWidget)
        self.output_button.setObjectName(u"output_button")

        self.horizontalLayout.addWidget(self.output_button)

        self.close_button = QPushButton(self.horizontalLayoutWidget)
        self.close_button.setObjectName(u"close_button")

        self.horizontalLayout.addWidget(self.close_button)

        Form.setWindowTitle("Mid解析器")

        self.groupBox.setTitle("mid信息")
        self.fileChoseButton.setText("选择文件")
        self.note_count_label.setText("音符数")
        self.input_button.setText("导入")
        self.output_button.setText("导出分析")
        self.close_button.setText("关闭")

        QMetaObject.connectSlotsByName(Form)

        # self.ui.btnCalculate.clicked.connect(self.fileLoading)

    def fileLoading(self):
        filePath, _ = QFileDialog.getOpenFileName(
            self.groupBox,  # 父窗口对象
            "选择文件",  # 标题
            r"./",  # 起始目录
            "mid类型 (*.mid *.midi)"  # 选择类型过滤项，过滤内容在括号中
        )
        print(filePath)

    @Slot()
    def on_fileChoseButton_clicked(self):
        filePath, _ = QFileDialog.getOpenFileName(
            self.groupBox,  # 父窗口对象
            "选择文件",  # 标题
            r"./",  # 起始目录
            "mid类型 (*.mid *.midi)"  # 选择类型过滤项，过滤内容在括号中
        )
        print(filePath)


class MidAnalyseGui(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.fileChoseButton.clicked.connect(self.fileLoading)

    def fileLoading(self):
        filePath, _ = QFileDialog.getOpenFileName(
            self.ui.groupBox,  # 父窗口对象
            "选择文件",  # 标题
            r"./",  # 起始目录
            "mid类型 (*.mid *.midi)"  # 选择类型过滤项，过滤内容在括号中
        )
        print(filePath)

    @Slot()
    def on_fileChoseButton_clicked(self):
        filePath, _ = QFileDialog.getOpenFileName(
            self.ui.groupBox,  # 父窗口对象
            "选择文件",  # 标题
            r"./",  # 起始目录
            "mid类型 (*.mid *.midi)"  # 选择类型过滤项，过滤内容在括号中
        )
        print(filePath)


if __name__ == "__main__":
    app = QApplication(sys.argv)  # 创建一个QApplication，也就是你要开发的软件app
    # MainWindow = QMainWindow()  # 创建一个QMainWindow，用来装载你需要的各种组件、控件
    # MainWindow = QWidget()  # 创建一个QMainWindow，用来装载你需要的各种组件、控件
    ui = MidAnalyseGui()  # ui是你创建的ui类的实例化对象
    # ui.setupUi(MainWindow)  # 执行类中的setupUi方法，方法的参数是第二步中创建的QMainWindow
    ui.show()  # 执行QMainWindow的show()方法，显示这个QMainWindow
    sys.exit(app.exec())  # 使用exit()或者点击关闭按钮退出QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QWidget()
    ui = Ui_Form()
    ui.setupUi(MainWindow)
    ui.show()
    sys.exit(app.exec())
