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


class loginDialog(QDialog):
    ui = Ui_Dialog()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui.setupUi(self)
        self.newUserUi.setupUi(self)
        
        if not os.path.exists('data'):
            os.mkdir('data')
        # self.clearFocus()
        # self.ui.userNameEdit.setFocus()
        self.ui.loginButton.clicked.connect(self.check)
        self.ui.loginMiniButton.clicked.connect(self.showMinimized)
        self.ui.loginCloseButton.clicked.connect(self.close)
        self.ui.passwordEdit.setEchoMode(QLineEdit.Password)

    def check(self):
        filepath = 'data/userInfo'
        # if not os.path.exists(filepath):
        #     os.mkdir(filepath)
        filepath += '/users.dat'
        # if not os.path.isfile(filepath):
        #     userName = 'admin'
        #     userPassword = '123456'
        #     userFile = open(filepath, 'wb')
        #     infoToWrite = userName + '\n' + userPassword + '\n'
        #     infoToWrite = func_encrypt_config(key, infoToWrite)
        #     userFile.write(infoToWrite.encode('utf-8'))
        #     userFile.flush()
        #     userFile.close()
        # else:
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = loginDialog()
    login.setWindowFlag(Qt.FramelessWindowHint)
    login.show()
    # dialog = QDialog()
    # dialog.setWindowFlag(Qt.FramelessWindowHint)      # 去除标题栏
    # ui = Ui_Dialog()
    # ui.setupUi(dialog)
    # dialog.show()
    sys.exit(app.exec_())
