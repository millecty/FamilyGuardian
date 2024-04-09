import sys
import os
import re
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QMessageBox, QLineEdit
from PyQt5.QtCore import Qt
from untitled import Ui_Dialog
from newUser import Ui_Dialog as Ui_newUserDialog

from utils.encryption import func_encrypt_config, func_decrypt_config
from utils.lineEditValidator import LineEditValidator

QtCore.QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
key = b'mysecretpassword'  # 密钥（需要确保安全）

class registerDialog(QDialog):
    ui = Ui_newUserDialog()
    userNameValidator = LineEditValidator(
        fullPatterns=r'^[a-zA-Z0-9]{6,12}$',
        partialPatterns=r'^[\u4e00-\u9fa5a-zA-Z0-9]{1,12}$',
        fixupString='请输入英文字母和数字组成的6-12位用户名'
    )
    userPasswordValidator = LineEditValidator(
        fullPatterns=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[^]{8,16}$',
        partialPatterns=r'^[^]{1,16}$',
        fixupString=None
    )

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.ui.regisMiniButton.clicked.connect(self.showMinimized)
        self.ui.regisCloseButton.clicked.connect(self.close)
        self.ui.passwordEdit.setEchoMode(QLineEdit.Password)
        self.ui.passwordConfirmEdit.setEchoMode(QLineEdit.Password)
        self.ui.registerButton.clicked.connect(self.register)

    def register(self):
        msgBox = QMessageBox()
        msgBox.setText('注册成功!\n即将转到登陆界面...')
        timer = QTimer()
        timer.timeout.connect(msgBox.close)
        timer.start(3000)
        msgBox.exec_()
        self.close()

class loginDialog(QDialog):
    ui = Ui_Dialog()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.ui.loginButton.clicked.connect(self.check)
        self.ui.loginMiniButton.clicked.connect(self.showMinimized)
        self.ui.loginCloseButton.clicked.connect(self.close)
        self.ui.passwordEdit.setEchoMode(QLineEdit.Password)

    def check(self):
        filepath = 'data/userInfo'
        filepath += '/users.dat'
        userInput_Name = self.ui.userNameEdit.text()
        userInput_Password = self.ui.passwordEdit.text()
        userFile = open(filepath, 'rb')
        userInfo = userFile.read().decode('utf-8')
        userFile.close()
        userInfo = func_decrypt_config(key, userInfo)
        if self.check_credentials(userInfo, userInput_Name, userInput_Password):
            print('登录成功!')
            QMessageBox.information(self, 'Congratulation!', '登陆成功!')
        else:
            print('登录失败!')
            QMessageBox.information(self, 'Pity!', '登陆失败!')

    def check_credentials(self, userinfo, userinput_name, userinput_password):
        lines = userinfo.splitlines()
        userNum = [x for x in range(0, len(lines) - 1) if x % 2 == 0]
        if len(lines) % 2 != 0:
            raise SystemExit('UserFileError!')
        for i in userNum:
            if lines[i] == userinput_name and lines[i + 1] == userinput_password:
                return True
        return False


class Controller:
    # 放在
    def __init__(self):
        if not os.path.exists('data'):
            os.mkdir('data')
            os.mkdir('data/userInfo')
        filepath = 'data/userInfo/users.dat'
        # 如果没有用户账户文件，打开注册界面
        if not os.path.isfile(filepath):
            self.show_register()
        self.show_login()

    def show_register(self):
        self.regisDialog = registerDialog()
        self.regisDialog.setFixedSize(378, 440)
        self.regisDialog.exec_()

    def show_login(self):
        self.logDialog = loginDialog()
        self.logDialog.setFixedSize(378, 440)
        self.logDialog.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = Controller()
    # controller.show_login()
    sys.exit(app.exec_())
