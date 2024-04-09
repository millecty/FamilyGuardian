import os
# 文件加解密
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
key = b'mysecretpassword'  # 密钥（需要确保安全）
#
# # 解密函数
# def func_decrypt_config(_key, encrypted_text):
#     iv = base64.b64decode(encrypted_text[:24])
#     ciphertext = base64.b64decode(encrypted_text[24:])
#     cipher = AES.new(_key, AES.MODE_CBC, iv)
#     decrypted_text = unpad(cipher.decrypt(ciphertext), AES.block_size).decode()
#     return decrypted_text
#
# filepath = 'data/userInfo/user.dat'
# userFile = open(filepath, 'rb')
# userInfo = userFile.read().decode('utf-8')
# userInfo = func_decrypt_config(key, userInfo)
#
# # print(userInfo)
# n = userInfo.splitlines()
# print(len(n))
#
# userFile.close()

n = 10  # 指定的数字上限

# 使用列表推导式生成正奇数列表
odd_numbers = [x for x in range(0, n - 1) if x % 2 == 0]

print(odd_numbers)
