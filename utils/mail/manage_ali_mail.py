# @Author  : kane.zhu
# @Time    : 2023/4/6 16:57
# @Software: PyCharm
# @Description:
import json
import os.path
from log_settings import logger
import requests
from settings.conf import PrdConfig


def ali_mail_token():
    ali_header = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    uri = 'oauth2/v2.0/token'
    payload = {
        'grant_type': 'client_credentials',
        'client_id': PrdConfig.ALI_MAIL_CLIENT_ID,
        'client_secret': PrdConfig.ALI_MAIL_CLIENT_SECRET
    }
    url = "{}/{}".format(PrdConfig.ALI_MAIL_URL,uri)
    try:
        res = requests.post(url,headers=ali_header,data=payload)
    except Exception as e:
        logger.error("初始化阿里云企业邮箱token异常：{}".format(e))
        return  e
    return  json.loads(bytes.decode(res.content))



