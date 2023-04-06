# @Author  : kane.zhu
# @Time    : 2022/11/8 16:12
# @Software: PyCharm
# @Description:

import redis
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
