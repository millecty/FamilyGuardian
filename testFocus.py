# 导入相关模块和包
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import sys

# 创建一个app应用
app = QApplication(sys.argv)
# 创建一个窗口
window = QWidget()
# 设置窗口标题
window.setWindowTitle('焦点控制')
# 设置窗口大小
window.resize(500, 500)
# 创建文本框Text_box 并作为window的子类
Text_box = QLineEdit(window)
# 创建文本框Text_box1并作为window的子类
Text_box1 = QLineEdit(window)
# 设置文本框所在位置
Text_box1.move(50, 50)
# 创建文本框Text_box3，并作为window的子类
Text_box2 = QLineEdit(window)
# 设置文本框所在位置
Text_box2.move(100, 100)
# 设置Text_box2作为获得焦点的文本框
Text_box2.setFocus()
# 设置通过Tab键过得焦点
Text_box2.setFocusPolicy(Qt.TabFocus)
# 展示窗口
window.show()
# 进入事件循环
sys.exit(app.exec_())