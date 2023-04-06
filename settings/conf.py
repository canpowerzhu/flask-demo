# @Author  : kane.zhu
# @Time    : 2022/11/7 21:43
# @Software: PyCharm
# @Description:


from starlette.config import Config as StarletConfig
import os
from collections import OrderedDict

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
config = StarletConfig(os.path.join(os.path.dirname(BASE_PATH), '.env'))


#######################################################################################

class BaseConfig(object):
    ######################################################################################
    # encrypt key & offset
    PASSKEY = config('PASSKEY', default='')
    PASSOFFSET = config('PASSOFFSET', default='')
    SECRET_KEY = config('SECRET_KEY', default='')
    ACCESS_SECRET_KEY = config('ACCESS_SECRET_KEY', default='')
    REFRESH_SECRET_KEY = config('REFRESH_SECRET_KEY', default='')

    #######################################################################################
    # server start param
    SERVER_HOST = config('SERVER_HOST', default='0.0.0.0')
    SERVER_PORT = config('SERVER_PORT', cast=int, default=5001)
    # Response Body struct
    GET_DATA = OrderedDict()
    POST_DATA = OrderedDict()
    GET_DATA = {
        'code': int,
        'show_size': int,
        'current_page': int,
        'count': int,
        'records': ''
    }
    POST_DATA = {
        'code': int,
        'message': str
    }

    #######################################################################################
    # INCLUDE_IN_SCHEMA = config('INCLUDE_IN_SCHEMA', cast=bool, default=True)
    #######################################################################################
    # ORM
    def _get_orm_base_conf(self, appd: dict) -> dict:
        return {
            'connections': {
                'default': {
                    'engine': 'tortoise.backends.mysql',
                    'credentials': {
                        'host': self.DB_HOST,
                        'port': self.DB_PORT,
                        'user': self.DB_USER,
                        'password': self.DB_PASSWD,
                        'database': self.DB_DATABASE,
                        'minsize': 1,
                        'maxsize': self.DB_MAX_SIZE,
                        'charset': 'utf8mb4'
                    }
                }
            },
            'apps': appd,
            'use_tz': False,
            'timezone': 'Asia/Shanghai'
        }

    @property
    def orm_link_conf(self) -> dict:
        orm_apps_settings = {
            'models': {
                'models': [
                    'app.dao.models'
                ],
                'default_connection': 'default',
            }
        }
        return self._get_orm_base_conf(orm_apps_settings)


class PrdConfig(BaseConfig):
    ###################################################################################################################
    # redis
    REDIS_HOST = config('REDIS_HOST', default='127.0.0.1')
    REDIS_PORT = config('REDIS_PORT', cast=int, default=6379)
    REDIS_PASSWD = config('REDIS_PASSWD', default='')
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    ###################################################################################################################
    # mysql database
    DB_USER = config('DB_USER', default='root')
    DB_PASSWD = config('DB_PASSWD', default='')
    DB_HOST = config('DB_HOST', default='127.0.0.1')
    DB_PORT = config('DB_PORT', cast=int, default=3306)
    DB_DATABASE = config('DB_DATABASE', default='')
    DB_MAX_SIZE = config('DB_MAX_SIZE', cast=int, default=5)
    # print("部分参数",DB_PASSWD,DB_HOST,DB_DATABASE)

    ALGORITHM = config('ALGORITHM', default="HS256")

    ###################################################################################################################
    # OSS
    OSS_ACCESS_KEY_ID = config('OSS_ACCESS_KEY_ID', default='')
    OSS_ACCESS_KEY_SECRET = config('OSS_ACCESS_KEY_SECRET', default='')
    OSS_BUCKET = config('OSS_BUCKET', default='')
    OSS_ENDPOINT = config('OSS_ENDPOINT',default='')
    OSS_STS_ARN = config('OSS_STS_ARN',default=None)

    #OSS分片上传参数
    OSS_PART_SIZE = config('OSS_PART_SIZE',default=100*1024*1024)  #分片上传默认的分片大小100MB 官方是100KB
    OSS_MULTI_THRESHOLD = config('OSS_MULTI_THRESHOLD',default=100*1024) #文件长度阈值 大于后启用分片
    OSS_NUM_THREADS = config('OSS_NUM_THREADS',default=8) #设置并发上传线程数

    BROKER_URL = config('BROKER_URL',default="redis://192.168.1.4:6369/1")
    CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND',default="redis://192.168.1.4:6369/1")
    CELRY_TIMEZONE = 'Asia/Shanghai'

    TEMPLATE_PATH=os.path.join(os.path.dirname(BASE_PATH),'templates')
    STATIC_PATH=os.path.join(os.path.dirname(BASE_PATH),'static')


    #Email config
    ## Email
    EMAIL_FROM_ACCOUNT = config('EMAIL_FROM_ACCOUNT', default='')
    EMAIL_FROM_ACCOUNT_PASS = config('EMAIL_FROM_ACCOUNT_PASS', default='')
    EMAIL_HOST = config('EMAIL_HOST', default='smtp.mxhichina.com')
    EMAIL_SMTP_PORT = config('EMAIL_SMTP_PORT', default=465)

    # NAME Domain config
    NAME_API_URL = config('NAME_API_URL',default='')

    # ALI Domain config
    ACCESS_KEY_ID = config('ACCESS_KEY_ID',default='')
    ACCESS_SECRET = config('ACCESS_SECRET',default='')
    ALI_USERNAME = config('ALI_USERNAME',default='')
    DOMAIN_RECORD_PAGE_SIZE = config('DOMAIN_RECORD_PAGE_SIZE',default='') #设置获取域名解析记录的单页数量

    #JENKINS Config
    JENKINS_HOST = config('JENKINS_HOST', default='')
    JENKINS_API_USER = config('JENKINS_API_USER', default='')
    JENKINS_API_TOKEN = config('JENKINS_API_TOKEN', default='')


    #ali cloud mail
    ALI_MAIL_URL = config('ALI_MAIL_URL', default='')
    ALI_MAIL_CLIENT_ID = config('ALI_MAIL_CLIENT_ID', default='')
    ALI_MAIL_CLIENT_SECRET = config('ALI_MAIL_CLIENT_SECRET', default='')

Config = PrdConfig
ORM_LINK_CONF = Config().orm_link_conf