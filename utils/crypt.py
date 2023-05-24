# @Author  : kane.zhu
# @Time    : 2023/4/20 19:47
# @Software: PyCharm
# @Description:

from Crypto.Cipher import AES
from Crypto import Random
from binascii import b2a_hex, a2b_hex
from settings.conf import PrdConfig

class KaneCrypto(object):
    def __init__(self, key: bytes, iv: str):
        """
        :param key: 是密钥key
        :param iv: 是偏移量
        """
        self.mode = AES.MODE_CBC
        # 因为在python3中AES传入参数的参数类型存在问题，需要更换为 bytearray , 所以使用encode编码格式将其转为字节格式（linux系统可不用指定编码）
        self.key = key
        self.iv = iv.encode('utf-8')

    def __pkcs5padding(self, data):
        return self.pkcs7padding(data, 8)

    def __pkcs7padding(self, data, block_size=16):
        if type(data) != bytearray and type(data) != bytes:
            raise TypeError("仅支持 bytearray/bytes 类型!")
        pl = block_size - (len(data) % block_size)
        return data + bytearray([pl for i in range(pl)])


    def __pre_check_length(self, msg):
        # 这里密钥key 长度必须为16（AES-128）,
        # 24（AES-192）,或者32 （AES-256）Bytes 长度
        # 目前AES-128 足够目前使用
        if len(msg.encode('utf-8')) % 16:
            add = 16 - len(msg.encode('utf-8'))
        else:
            add = 0
        msg = msg + ('\0' * add)
        return msg.encode('utf-8')

    def encrypt(self, msg: bytes):
        """
        :param msg: 需要加密的信息
        :return: 返回密文
        """
        msg = self.__pkcs7padding(msg)
        cryptos = AES.new(self.key, self.mode, self.iv)
        cipher_text = cryptos.encrypt(msg)
        return bytes.decode(b2a_hex(cipher_text))


    def decrypt(self, msg: str) -> str:
        crypto = AES.new(self.key, self.mode, self.iv)
        plain_text = crypto.decrypt(a2b_hex(msg))
        return bytes.decode(plain_text).rstrip('\0')


