# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PySide6-Pkg.ui'
##
## Created by: Qt User Interface Compiler version 6.4.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
                           QCursor, QFont, QFontDatabase, QGradient,
                           QIcon, QImage, QKeySequence, QLinearGradient,
                           QPainter, QPalette, QPixmap, QRadialGradient,
                           QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QHBoxLayout,
                               QHeaderView, QLabel, QMainWindow, QMenu,
                               QMenuBar, QSizePolicy, QSlider, QSpinBox,
                               QStatusBar, QTabWidget, QTableWidget, QTableWidgetItem,
                               QTextBrowser, QTextEdit, QToolButton, QVBoxLayout,
                               QWidget)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.action = QAction(MainWindow)
        self.action.setObjectName(u"action")
        icon = QIcon()
        iconThemeName = u"document-open"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.action.setIcon(icon)
        self.action_Input = QAction(MainWindow)
        self.action_Input.setObjectName(u"action_Input")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 951, 611))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.tabO = QTabWidget(self.verticalLayoutWidget)
        self.tabO.setObjectName(u"tabO")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayoutWidget_2 = QWidget(self.tab)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(0, 0, 881, 591))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.tableWidget = QTableWidget(self.verticalLayoutWidget_2)
        self.tableWidget.setObjectName(u"tableWidget")

        self.verticalLayout_2.addWidget(self.tableWidget)

        self.tabO.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.label = QLabel(self.tab_2)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 71, 16))
        self.widget = QWidget(self.tab_2)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(0, 30, 281, 131))
        self.verticalLayoutWidget_3 = QWidget(self.widget)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(10, 0, 271, 131))
        self.verticalLayout_3 = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.verticalLayoutWidget_3)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_3.addWidget(self.label_2)

        self.label_4 = QLabel(self.verticalLayoutWidget_3)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_3.addWidget(self.label_4)

        self.label_5 = QLabel(self.verticalLayoutWidget_3)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_3.addWidget(self.label_5)

        self.label_7 = QLabel(self.verticalLayoutWidget_3)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_3.addWidget(self.label_7)

        self.label_6 = QLabel(self.verticalLayoutWidget_3)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_3.addWidget(self.label_6)

        self.label_3 = QLabel(self.verticalLayoutWidget_3)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_3.addWidget(self.label_3)

        self.widget_2 = QWidget(self.tab_2)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setGeometry(QRect(280, 30, 281, 131))
        self.verticalLayoutWidget_4 = QWidget(self.widget_2)
        self.verticalLayoutWidget_4.setObjectName(u"verticalLayoutWidget_4")
        self.verticalLayoutWidget_4.setGeometry(QRect(10, 0, 271, 131))
        self.verticalLayout_4 = QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_9 = QLabel(self.verticalLayoutWidget_4)
        self.label_9.setObjectName(u"label_9")

        self.verticalLayout_4.addWidget(self.label_9)

        self.label_8 = QLabel(self.verticalLayoutWidget_4)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout_4.addWidget(self.label_8)

        self.label_10 = QLabel(self.verticalLayoutWidget_4)
        self.label_10.setObjectName(u"label_10")

        self.verticalLayout_4.addWidget(self.label_10)

        self.label_12 = QLabel(self.verticalLayoutWidget_4)
        self.label_12.setObjectName(u"label_12")

        self.verticalLayout_4.addWidget(self.label_12)

        self.label_13 = QLabel(self.verticalLayoutWidget_4)
        self.label_13.setObjectName(u"label_13")

        self.verticalLayout_4.addWidget(self.label_13)

        self.label_11 = QLabel(self.verticalLayoutWidget_4)
        self.label_11.setObjectName(u"label_11")

        self.verticalLayout_4.addWidget(self.label_11)

        self.widget_3 = QWidget(self.tab_2)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setGeometry(QRect(10, 160, 781, 171))
        self.horizontalLayoutWidget = QWidget(self.widget_3)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(0, 0, 621, 24))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_14 = QLabel(self.horizontalLayoutWidget)
        self.label_14.setObjectName(u"label_14")

        self.horizontalLayout.addWidget(self.label_14)

        self.comboBox = QComboBox(self.horizontalLayoutWidget)
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout.addWidget(self.comboBox)

        self.toolButton = QToolButton(self.horizontalLayoutWidget)
        self.toolButton.setObjectName(u"toolButton")

        self.horizontalLayout.addWidget(self.toolButton)

        self.horizontalLayoutWidget_2 = QWidget(self.widget_3)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(0, 20, 241, 31))
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_15 = QLabel(self.horizontalLayoutWidget_2)
        self.label_15.setObjectName(u"label_15")

        self.horizontalLayout_2.addWidget(self.label_15)

        self.horizontalSlider = QSlider(self.horizontalLayoutWidget_2)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_2.addWidget(self.horizontalSlider)

        self.horizontalLayoutWidget_3 = QWidget(self.widget_3)
        self.horizontalLayoutWidget_3.setObjectName(u"horizontalLayoutWidget_3")
        self.horizontalLayoutWidget_3.setGeometry(QRect(260, 20, 241, 31))
        self.horizontalLayout_4 = QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_17 = QLabel(self.horizontalLayoutWidget_3)
        self.label_17.setObjectName(u"label_17")

        self.horizontalLayout_4.addWidget(self.label_17)

        self.horizontalSlider_3 = QSlider(self.horizontalLayoutWidget_3)
        self.horizontalSlider_3.setObjectName(u"horizontalSlider_3")
        self.horizontalSlider_3.setOrientation(Qt.Horizontal)

        self.horizontalLayout_4.addWidget(self.horizontalSlider_3)

        self.horizontalLayoutWidget_4 = QWidget(self.widget_3)
        self.horizontalLayoutWidget_4.setObjectName(u"horizontalLayoutWidget_4")
        self.horizontalLayoutWidget_4.setGeometry(QRect(260, 50, 241, 31))
        self.horizontalLayout_6 = QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.label_18 = QLabel(self.horizontalLayoutWidget_4)
        self.label_18.setObjectName(u"label_18")

        self.horizontalLayout_6.addWidget(self.label_18)

        self.textEdit = QTextEdit(self.horizontalLayoutWidget_4)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setMaximumSize(QSize(16777215, 78))

        self.horizontalLayout_6.addWidget(self.textEdit)

        self.horizontalLayoutWidget_7 = QWidget(self.widget_3)
        self.horizontalLayoutWidget_7.setObjectName(u"horizontalLayoutWidget_7")
        self.horizontalLayoutWidget_7.setGeometry(QRect(510, 20, 241, 31))
        self.horizontalLayout_9 = QHBoxLayout(self.horizontalLayoutWidget_7)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.label_21 = QLabel(self.horizontalLayoutWidget_7)
        self.label_21.setObjectName(u"label_21")

        self.horizontalLayout_9.addWidget(self.label_21)

        self.spinBox = QSpinBox(self.horizontalLayoutWidget_7)
        self.spinBox.setObjectName(u"spinBox")

        self.horizontalLayout_9.addWidget(self.spinBox)

        self.horizontalLayoutWidget_6 = QWidget(self.widget_3)
        self.horizontalLayoutWidget_6.setObjectName(u"horizontalLayoutWidget_6")
        self.horizontalLayoutWidget_6.setGeometry(QRect(510, 50, 241, 31))
        self.horizontalLayout_8 = QHBoxLayout(self.horizontalLayoutWidget_6)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.label_20 = QLabel(self.horizontalLayoutWidget_6)
        self.label_20.setObjectName(u"label_20")

        self.horizontalLayout_8.addWidget(self.label_20)

        self.textBrowser_2 = QTextBrowser(self.horizontalLayoutWidget_6)
        self.textBrowser_2.setObjectName(u"textBrowser_2")

        self.horizontalLayout_8.addWidget(self.textBrowser_2)

        self.horizontalLayoutWidget_10 = QWidget(self.widget_3)
        self.horizontalLayoutWidget_10.setObjectName(u"horizontalLayoutWidget_10")
        self.horizontalLayoutWidget_10.setGeometry(QRect(0, 50, 251, 31))
        self.horizontalLayout_13 = QHBoxLayout(self.horizontalLayoutWidget_10)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.label_24 = QLabel(self.horizontalLayoutWidget_10)
        self.label_24.setObjectName(u"label_24")

        self.horizontalLayout_13.addWidget(self.label_24)

        self.comboBox_3 = QComboBox(self.horizontalLayoutWidget_10)
        self.comboBox_3.setObjectName(u"comboBox_3")

        self.horizontalLayout_13.addWidget(self.comboBox_3)

        self.horizontalLayoutWidget_5 = QWidget(self.widget_3)
        self.horizontalLayoutWidget_5.setObjectName(u"horizontalLayoutWidget_5")
        self.horizontalLayoutWidget_5.setGeometry(QRect(0, 80, 241, 31))
        self.horizontalLayout_7 = QHBoxLayout(self.horizontalLayoutWidget_5)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.label_19 = QLabel(self.horizontalLayoutWidget_5)
        self.label_19.setObjectName(u"label_19")

        self.horizontalLayout_7.addWidget(self.label_19)

        self.textBrowser = QTextBrowser(self.horizontalLayoutWidget_5)
        self.textBrowser.setObjectName(u"textBrowser")

        self.horizontalLayout_7.addWidget(self.textBrowser)

        self.horizontalLayoutWidget_9 = QWidget(self.widget_3)
        self.horizontalLayoutWidget_9.setObjectName(u"horizontalLayoutWidget_9")
        self.horizontalLayoutWidget_9.setGeometry(QRect(0, 110, 371, 31))
        self.horizontalLayout_12 = QHBoxLayout(self.horizontalLayoutWidget_9)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.label_23 = QLabel(self.horizontalLayoutWidget_9)
        self.label_23.setObjectName(u"label_23")

        self.horizontalLayout_12.addWidget(self.label_23)

        self.comboBox_2 = QComboBox(self.horizontalLayoutWidget_9)
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.horizontalLayout_12.addWidget(self.comboBox_2)

        self.horizontalLayoutWidget_8 = QWidget(self.widget_3)
        self.horizontalLayoutWidget_8.setObjectName(u"horizontalLayoutWidget_8")
        self.horizontalLayoutWidget_8.setGeometry(QRect(260, 80, 511, 31))
        self.horizontalLayout_11 = QHBoxLayout(self.horizontalLayoutWidget_8)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.checkBox_2 = QCheckBox(self.horizontalLayoutWidget_8)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.horizontalLayout_11.addWidget(self.checkBox_2)

        self.checkBox = QCheckBox(self.horizontalLayoutWidget_8)
        self.checkBox.setObjectName(u"checkBox")

        self.horizontalLayout_11.addWidget(self.checkBox)

        self.label_22 = QLabel(self.horizontalLayoutWidget_8)
        self.label_22.setObjectName(u"label_22")

        self.horizontalLayout_11.addWidget(self.label_22)

        self.textBrowser_3 = QTextBrowser(self.horizontalLayoutWidget_8)
        self.textBrowser_3.setObjectName(u"textBrowser_3")

        self.horizontalLayout_11.addWidget(self.textBrowser_3)

        self.horizontalLayoutWidget_11 = QWidget(self.widget_3)
        self.horizontalLayoutWidget_11.setObjectName(u"horizontalLayoutWidget_11")
        self.horizontalLayoutWidget_11.setGeometry(QRect(390, 110, 291, 31))
        self.horizontalLayout_14 = QHBoxLayout(self.horizontalLayoutWidget_11)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.label_25 = QLabel(self.horizontalLayoutWidget_11)
        self.label_25.setObjectName(u"label_25")

        self.horizontalLayout_14.addWidget(self.label_25)

        self.comboBox_4 = QComboBox(self.horizontalLayoutWidget_11)
        self.comboBox_4.setObjectName(u"comboBox_4")

        self.horizontalLayout_14.addWidget(self.comboBox_4)

        self.horizontalLayoutWidget_12 = QWidget(self.widget_3)
        self.horizontalLayoutWidget_12.setObjectName(u"horizontalLayoutWidget_12")
        self.horizontalLayoutWidget_12.setGeometry(QRect(0, 140, 301, 31))
        self.horizontalLayout_15 = QHBoxLayout(self.horizontalLayoutWidget_12)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.label_26 = QLabel(self.horizontalLayoutWidget_12)
        self.label_26.setObjectName(u"label_26")

        self.horizontalLayout_15.addWidget(self.label_26)

        self.comboBox_5 = QComboBox(self.horizontalLayoutWidget_12)
        self.comboBox_5.setObjectName(u"comboBox_5")

        self.horizontalLayout_15.addWidget(self.comboBox_5)

        self.tabO.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.tabO.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.tabO.addTab(self.tab_4, "")

        self.verticalLayout.addWidget(self.tabO)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 26))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menu.addAction(self.action)
        self.menu.addAction(self.action_Input)

        self.retranslateUi(MainWindow)

        self.tabO.setCurrentIndex(1)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.action.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00 Open", None))
        self.action_Input.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u5165 Input", None))
        self.tabO.setTabText(self.tabO.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Tab 1", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_14.setText(
            QCoreApplication.translate("MainWindow", u"\u9ed8\u8ba4\u4fdd\u5b58\u8def\u5f84\uff1a", None))
        self.toolButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"\u901f\u5ea6\u500d\u7387", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"\u97f3\u91cf\u500d\u7387", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"\u8ba1\u5206\u677f\u540d\u79f0", None))
        self.label_21.setText(
            QCoreApplication.translate("MainWindow", u"\u6700\u5927\u6307\u4ee4\u751f\u6210\u9ad8\u5ea6", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"\u73a9\u5bb6\u9009\u62e9\u5668", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u5668\u6a21\u5f0f", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"bdx\u4f5c\u8005\u540d\u79f0", None))
        self.label_23.setText(
            QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u547d\u4ee4\u683c\u5f0f\u7248\u672c", None))
        self.checkBox_2.setText(
            QCoreApplication.translate("MainWindow", u"\u662f\u5426\u542f\u7528\u8fdb\u5ea6\u6761", None))
        self.checkBox.setText(
            QCoreApplication.translate("MainWindow", u"\u662f\u5426\u81ea\u5b9a\u4e49\u8fdb\u5ea6\u6761", None))
        self.label_22.setText(
            QCoreApplication.translate("MainWindow", u"\u81ea\u5b9a\u4e49\u8fdb\u5ea6\u6761\u5185\u5bb9\uff1a", None))
        self.label_25.setText(
            QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u8f6c\u6362\u7b97\u6cd5\u7248\u672c", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u5bfc\u51fa\u6a21\u5f0f", None))
        self.tabO.setTabText(self.tabO.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Tab 2", None))
        self.tabO.setTabText(self.tabO.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"\u9875", None))
        self.tabO.setTabText(self.tabO.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"\u9875", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6", None))
    # retranslateUi


if __name__ == "__main__":
    import sys
    from PySide6 import QtWidgets

    app = QtWidgets.QApplication(sys.argv)  # 创建一个QApplication，也就是你要开发的软件app
    MainWindow = QtWidgets.QMainWindow()  # 创建一个QMainWindow，用来装载你需要的各种组件、控件
    # MainWindow = QtWidgets.QWidget()        # 创建一个QMainWindow，用来装载你需要的各种组件、控件
    ui = Ui_MainWindow()  # ui是你创建的ui类的实例化对象
    ui.setupUi(MainWindow)  # 执行类中的setupUi方法，方法的参数是第二步中创建的QMainWindow
    MainWindow.show()  # 执行QMainWindow的show()方法，显示这个QMainWindow
    sys.exit(app.exec_())  # 使用exit()或者点击关闭按钮退出QApplication
