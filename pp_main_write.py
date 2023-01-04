import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtWidgets import QLabel, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


class MusicreaterGUI:
    def __init__(self):
        self.button, self.label = None, None

    def setupUi(self, window):
        window.setWindowTitle("音·创")  # 窗口标题
        window.resize(300, 150)  # 重置大小

        self.label = QLabel(window)  # 在窗口上创建实例化label
        string = "welcome to musicreater"
        self.label.setText(string)
        self.label.setGeometry(80, 50, 150, 20)

        self.button = QPushButton(window)
        self.button.setText("close")
        self.button.setGeometry(120, 100, 50, 20)
        self.button.clicked.connect(window.close)


class MusicreaterWidget(QWidget, MusicreaterGUI):  # 很棒的继承，请 体会
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)  # 创建应用程序实例对象
    app.setApplicationDisplayName("Musicreater-pp")
    app.setApplicationVersion("v0.0.1")
    app.setEffectEnabled(Qt.UI_AnimateCombo)
    app.setWindowIcon(QPixmap(r"logo_done_c_Finish_C_Done_CCC_1024px.ico"))

    window_ = MusicreaterWidget()  # 窗口实例化
    window_.show()
    n = app.exec()
    print(n)
    try:
        sys.exit(n)
    except SystemExit:
        print("hi, error")
