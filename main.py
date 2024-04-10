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
filepath = 'data/userInfo/users.dat'


class registerDialog(QDialog):
    abnormalExit = False        # 用于给程序知道是非正常退出，可以不用展示后面的界面
    ui = Ui_newUserDialog()
    userNameValidator = LineEditValidator(
        fullPatterns=['', r'^[a-zA-Z0-9]{6,12}$'],
        partialPatterns=['', r'^[a-zA-Z0-9]{1,12}$'],
        fixupString=''
    )
    userPasswordValidator = LineEditValidator(
        fullPatterns=['', r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z0-9]{8,16}$'],
        partialPatterns=['', r'^[a-zA-Z0-9]{1,16}$'],
        fixupString=''
    )

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.ui.regisMiniButton.clicked.connect(self.showMinimized)
        # self.ui.regisCloseButton.clicked.connect(QApplication.instance().quit)  # 这里要设置让后面的东西别出来了
        self.ui.regisCloseButton.clicked.connect(self.reject)  # 这里要设置让后面的东西别出来了
        self.ui.userNameEdit.setValidator(self.userNameValidator)
        self.ui.userNameEdit.installEventFilter(self.userNameValidator)
        self.ui.userNameEdit.setPlaceholderText('6-12个英文/数字组合')
        self.ui.passwordEdit.setEchoMode(QLineEdit.Password)
        self.ui.passwordEdit.setValidator(self.userPasswordValidator)
        self.ui.passwordEdit.installEventFilter(self.userPasswordValidator)
        self.ui.passwordEdit.setPlaceholderText('8-16个英文/数字组合(至少一个英文大小写加数字)')
        self.ui.passwordConfirmEdit.setValidator(self.userPasswordValidator)
        self.ui.passwordConfirmEdit.installEventFilter(self.userPasswordValidator)
        self.ui.passwordConfirmEdit.setEchoMode(QLineEdit.Password)
        self.ui.passwordConfirmEdit.setPlaceholderText('与第一次的输入保持一致')
        self.ui.registerButton.clicked.connect(self.register)
        QMessageBox.information(self, '', '首次登录，请先创建用户!')

    def register(self):
        userInput_Name = self.ui.userNameEdit.text()
        userInput_Password = self.ui.passwordEdit.text()
        userInput_PasswordConfirm = self.ui.passwordConfirmEdit.text()
        if len(userInput_Name) == 0 or len(userInput_Password) == 0 or len(userInput_PasswordConfirm) == 0:
            QMessageBox.information(self, '', '用户名/密码不能为空!')
            self.ui.userNameEdit.setFocus()
            return
        if userInput_Password != userInput_PasswordConfirm:
            QMessageBox.information(self, '', '两次输入的密码不一致!')
            self.ui.passwordEdit.clear()
            self.ui.passwordConfirmEdit.clear()
            self.ui.passwordEdit.setFocus()
            return
        userFile = open(filepath, 'wb')
        userInfo = userInput_Name + '\n' + userInput_Password
        userInfo = func_encrypt_config(key, userInfo)
        userFile.write(userInfo.encode('utf-8'))
        userFile.flush()
        userFile.close()
        # 注册成功
        msgBox = QMessageBox()
        msgBox.setText('注册成功!\n即将转到登陆界面...')
        timer = QTimer()
        timer.timeout.connect(msgBox.close)
        timer.start(3000)
        msgBox.exec_()
        self.accept()

    # def closeAct(self):
    #     self.abnormalExit = True
    #     self.close()

class loginDialog(QDialog):
    ui = Ui_Dialog()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.ui.loginButton.clicked.connect(self.check)
        self.ui.loginMiniButton.clicked.connect(self.showMinimized)
        self.ui.loginCloseButton.clicked.connect(self.reject)
        # self.ui.loginCloseButton.clicked.connect(self.close)
        self.ui.passwordEdit.setEchoMode(QLineEdit.Password)

    def check(self):
        userInput_Name = self.ui.userNameEdit.text()
        userInput_Password = self.ui.passwordEdit.text()
        userFile = open(filepath, 'rb')
        userInfo = userFile.read().decode('utf-8')
        userFile.close()
        userInfo = func_decrypt_config(key, userInfo)
        if self.check_credentials(userInfo, userInput_Name, userInput_Password) == 1:
            print('登录成功!')
            QMessageBox.information(self, 'Congratulation!', '登陆成功!')
        elif self.check_credentials(userInfo, userInput_Name, userInput_Password) == 2:
            print('密码错误!')
            self.ui.passwordEdit.clear()
            QMessageBox.information(self, '', '密码错误!')
        elif self.check_credentials(userInfo, userInput_Name, userInput_Password) == 3:
            print('账号错误!')
            self.ui.userNameEdit.clear()
            self.ui.passwordEdit.clear()
            self.ui.userNameEdit.setFocus()
            QMessageBox.information(self, '', '账号错误!')

    def check_credentials(self, userinfo, userinput_name, userinput_password):
        lines = userinfo.splitlines()
        userNum = [x for x in range(0, len(lines) - 1) if x % 2 == 0]
        if len(lines) % 2 != 0:
            raise SystemExit('UserFileError!')
        for i in userNum:
            if lines[i] == userinput_name and lines[i + 1] == userinput_password:  # 匹配成功
                return 1
            elif lines[i] == userinput_name and lines[i + 1] != userinput_password:  # 密码错误
                return 2
            else:  # 账号错误
                return 3
        return 0


class Controller:
    # 放在
    def __init__(self):
        if not os.path.exists('data'):
            os.mkdir('data')
        if not os.path.exists('data/userInfo'):
            os.mkdir('data/userInfo')
        filepath = 'data/userInfo/users.dat'
        # 如果没有用户账户文件，打开注册界面
        if not os.path.isfile(filepath):
            if self.show_register() == QDialog.Rejected:
                sys.exit(0)
        if self.show_login() == QDialog.Accepted:
            sys.exit(0)
        else:
            sys.exit(0)

    def show_register(self):
        self.regisDialog = registerDialog()
        self.regisDialog.setFixedSize(378, 440)
        return self.regisDialog.exec_()

    def show_login(self):
        self.logDialog = loginDialog()
        self.logDialog.setFixedSize(378, 440)
        return self.logDialog.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = Controller()
    print('等待结束')
    sys.exit(app.exec_())
