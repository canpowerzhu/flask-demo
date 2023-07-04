# @Author  : kane.zhu
# @Time    : 2022/11/8 16:12
# @Software: PyCharm
# @Description:
import datetime
import jwt
import redis
from flask import g

from settings.conf import PrdConfig
from log_settings import logger


def get_redis_client():
    try:
        pool = redis.ConnectionPool(host=PrdConfig.REDIS_HOST,
                                    port=PrdConfig.REDIS_PORT,
                                    password=PrdConfig.REDIS_PASSWD)
    except Exception as e:
        logger.error("connect redis error:{}".format(e))

    redis_conn = redis.Redis(connection_pool=pool)

    return redis_conn


def get_ali_mail_token():
    redis_con = get_redis_client()
    res = redis_con.get(PrdConfig.ALI_CLOUD_MAIL_KEY_NAME)

    ali_mail_token_from_redis = "bearer {}".format(bytes.decode(res))

    return ali_mail_token_from_redis



