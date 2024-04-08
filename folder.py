import os

# 文件加解密
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
key = b'mysecretpassword'  # 密钥（需要确保安全）

# 加密函数
def func_encrypt_config(_key, plain_text):
    cipher = AES.new(_key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(plain_text.encode(), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode()
    encrypted_text = base64.b64encode(ciphertext).decode()
    return iv + encrypted_text

content = 'admin\n123456\n'

content = func_encrypt_config(key, content)


filepath = 'data/userInfo'
if not os.path.exists(filepath):
    os.mkdir(filepath)

filepath += '/user.dat'
if not os.path.isfile(filepath):
    userFile = open(filepath, 'wb')
    # userFile.write('admin\n'.encode('utf-8'))
    # userFile.write('123456\n'.encode('utf-8'))
    userFile.write(content.encode('utf-8'))
    userFile.flush()
    userFile.close()

userFile = open(filepath, 'rb')
data = userFile.read().decode('utf-8')
userFile.close()
print(data)
