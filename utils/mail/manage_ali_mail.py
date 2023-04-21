# @Author  : kane.zhu
# @Time    : 2023/4/6 16:57
# @Software: PyCharm
# @Description:
import json
from utils import get_redis_client
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

    logger.info("获得阿里云邮箱token:{}, 缓存名称：{}， 过期时间：{}秒".format(
        json.loads(bytes.decode(res.content))['access_token'],
        PrdConfig.ALI_CLOUD_MAIL_KEY_NAME,
        PrdConfig.ALI_CLOUD_MAIL_KEY_EXPIRE_SECOND))


    redis_con = get_redis_client()
    # 这里不在判断缓存是否过期，只要初始化token 即覆盖缓存
    # if not check_token_is_expire():
    redis_con.set(PrdConfig.ALI_CLOUD_MAIL_KEY_NAME,
                      json.loads(bytes.decode(res.content))['access_token'],
                      ex=PrdConfig.ALI_CLOUD_MAIL_KEY_EXPIRE_SECOND)

    return  json.loads(bytes.decode(res.content))



# 校验token是否过期，过期重新获取 初始化，反之放行
def check_token_is_expire():
    redis_con = get_redis_client()
    key_status = redis_con.exists(PrdConfig.ALI_CLOUD_MAIL_KEY_NAME)
    res = False if key_status == 0 else True
    logger.info("校验redis key的状态,结果是{}".format(res))
    return  res
