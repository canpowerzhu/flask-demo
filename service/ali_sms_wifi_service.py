# @Author  : kane.zhu
# @Time    : 2023/5/19 18:03
# @Software: PyCharm
# @Description:

from flask import request

from dao.ops_db_wifi import db_ops_bulk_create, db_ops_get_password
from log_settings import logger
from settings.conf import PrdConfig
from utils import crypt
from utils.aliyun_cloud import ali_sms


def wifi_info_crypt_service(bulk_wifi_data) -> bool:
    crypt_obj = crypt.KaneCrypto(PrdConfig.AES_KEY.encode('UTF-8'), PrdConfig.AES_IV)
    data_info_arr = []
    for item in bulk_wifi_data:
        item['wifi_manage_pass'] = crypt_obj.encrypt(item['wifi_manage_pass'].encode())
        item['wifi_connect_pass'] = crypt_obj.encrypt(item['wifi_connect_pass'].encode())
        data_info_arr.append(item)
    status = db_ops_bulk_create(data_info_arr)
    return status


def get_wifi_pass_decrypt_service(wifi_name: str, phone_number: str) -> str:
    crypt_obj = crypt.KaneCrypto(PrdConfig.AES_KEY.encode('UTF-8'), PrdConfig.AES_IV)
    crypt_passord = db_ops_get_password(wifi_name)
    logger.info("TraceId:{},获取的密文密码是{}".format(request.trace_id, crypt_passord))
    # 这里要获取到请求的手机号 以及明文密码
    plain_password = crypt_obj.decrypt(crypt_passord)

    # print("明文是{},长度是{}，类型是{}".format(plain_password[0:16],len(plain_password),type(plain_password)))

    ali_sms.AliSms.SendPassWord(phone_number, plain_password[0:16])
