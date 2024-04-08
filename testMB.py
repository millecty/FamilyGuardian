from PyQt5.QtWidgets import QPushButton, QApplication, QWidget, QDialog
from PyQt5.QtWidgets import QMessageBox
import sys

app = QApplication([])
widget = QDialog()


def showMsg():
    QMessageBox.information(widget, "信息提示框", "ok,弹出测试信息")


btn = QPushButton("测试点击按钮", widget)
btn.clicked.connect(showMsg)
widget.show()
sys.exit(app.exec_())
