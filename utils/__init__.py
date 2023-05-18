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


# 构造header
headers = {
    'typ': 'jwt',
    'alg': 'HS256'
}


def create_token(username, password):
    # 构造payload
    payload = {
        'username': username,
        'password': password,  # 自定义用户ID
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)  # 超时时间
    }
    result = jwt.encode(payload=payload, key=PrdConfig.SALT, algorithm="HS256", headers=headers)
    return result


def login_required(f):
    '让装饰器装饰的函数属性不会变 -- name属性'
    '第1种方法,使用functools模块的wraps装饰内部函数'

    # @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            if g.username == 1:
                return {'code': 4001, 'message': 'token已失效'}, 401
            elif g.username == 2:
                return {'code': 4001, 'message': 'token认证失败'}, 401
            elif g.username == 2:
                return {'code': 4001, 'message': '非法的token'}, 401
            else:
                return f(*args, **kwargs)
        except BaseException as e:
            return {'code': 4001, 'message': '请先登录认证.'}, 401

    '第2种方法,在返回内部函数之前,先修改wrapper的name属性'
    wrapper.__name__ = f.__name__
    return wrapper
