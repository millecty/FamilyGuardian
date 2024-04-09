import sys
import os

# 文件加解密
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QMessageBox, QLineEdit
from PyQt5.QtCore import Qt
from untitled import Ui_Dialog
from newUser import Ui_Dialog as Ui_newUserDialog

QtCore.QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
key = b'mysecretpassword'  # 密钥（需要确保安全）


# 加密函数
def func_encrypt_config(_key, plain_text):
    cipher = AES.new(_key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(plain_text.encode(), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode()
    encrypted_text = base64.b64encode(ciphertext).decode()
    return iv + encrypted_text


# 解密函数
def func_decrypt_config(_key, encrypted_text):
    iv = base64.b64decode(encrypted_text[:24])
    ciphertext = base64.b64decode(encrypted_text[24:])
    cipher = AES.new(_key, AES.MODE_CBC, iv)
    decrypted_text = unpad(cipher.decrypt(ciphertext), AES.block_size).decode()
    return decrypted_text


class registerDialog(QDialog):
    ui = Ui_newUserDialog()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui.setupUi(self)


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
        else:
            self.show_login()

    def show_register(self):
        self.regisDialog = registerDialog()
        self.regisDialog.setFixedSize(378, 440)
        self.regisDialog.show()

    def show_login(self):
        self.logDialog = loginDialog()
        self.logDialog.setFixedSize(378, 440)
        self.logDialog.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = Controller()
    sys.exit(app.exec_())
