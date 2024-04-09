# coding:utf-8
# Python 3.8.x

from MainWindow_ui import Ui_MainWindow
from LineEditRegExpValidator import *

# PyQt5 - QLineEdit正则表达式输入验证器
# -- by 鱼子酱




class NewClassName(QtWidgets.QMainWindow, Ui_MainWindow):

    '''

    '''

    def __init__(self, parent=None):
        super(NewClassName, self).__init__(parent) #
        self.setupUi(self) #


        self.setFixedSize(self.width(), self.height())
        self.setFocus(True)



        # 创建输入验证器(默认为科学表达式输入验证器)
        SciNotValidator = LineEditRegExpValidator()
        self.lineEdit_2.setValidator(SciNotValidator)
        # 当输入不合法或未完成时，游标移除编辑框时，编辑框返回上一次内容。
        self.lineEdit_2.installEventFilter(SciNotValidator)


        # 创建整数输入(六位)验证器
        SciNotValidator = LineEditRegExpValidator(
            fullPatterns=[
                r'[0-9]{6}',
                ],

            partialPatterns=[
            '',
            r'[0-9]{1,6}'
            ],

            fixupString='123456'
        )
        self.lineEdit_3.setValidator(SciNotValidator)
        self.lineEdit_3.installEventFilter(SciNotValidator)


        # 创建字母(包含大小写，六位)输入验证器
        SciNotValidator = LineEditRegExpValidator(
            fullPatterns=[
                r'[a-zA-Z]{6}',
                ],

            partialPatterns=[
            '',
            r'[a-zA-Z]{1,6}'
            ],

            fixupString='aBcDeF'
        )
        self.lineEdit_4.setValidator(SciNotValidator)
        self.lineEdit_4.installEventFilter(SciNotValidator)




if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = NewClassName()
    MainWindow.show()
    app.exec_()