# @Author  : kane.zhu
# @Time    : 2023/2/2 19:19
# @Software: PyCharm
# @Description:
import base64
import os
from log_settings import logger
import pyotp
from qrcode import QRCode,constants
from settings.conf import PrdConfig
def get_qrcode(secret_key, username):

    filepath = PrdConfig.STATIC_PATH  + os.sep + 'img' + os.sep + secret_key + '.png'
    data = pyotp.totp.TOTP(secret_key).provisioning_uri(username, issuer_name="MFA Code")
    print(data)
    qr = QRCode(
        version=1,
        error_correction=constants.ERROR_CORRECT_L,
        box_size=6,
        border=4, )
    try:
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image()
        img.save(filepath)  # 保存条形码图片

        return True, filepath
    except Exception as e:
        # logger.error("生成二维码图片异常：{}".format(str(e)))
        print(e)
        return False, None




def return_img_stream(img_local_path):
    """
    工具函数:
    获取本地图片流
    :param img_local_path:文件单张图片的本地绝对路径
    :return: 图片流
    """
    img_stream = ''
    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream) #Base64是一种用64个字符来表示任意二进制数据的方法。
        img_stream=img_stream.decode()  ##bytes转成字符串
    return img_stream

def google_verify_result(secret_key, verifycode):
    t = pyotp.TOTP(secret_key)
    result = t.verify(verifycode)  # 对输入验证码进行校验，正确返回True
    if result:
        msg = True
    else:
        msg = False
    return msg