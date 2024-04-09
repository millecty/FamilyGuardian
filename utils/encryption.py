# 文件加解密
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

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