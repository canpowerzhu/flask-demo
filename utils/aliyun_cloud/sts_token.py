# @Author  : kane.zhu
# @Time    : 2022/11/12 10:38
# @Software: PyCharm
# @Description:
from alibabacloud_sts20150401 import models as sts_20150401_models
from alibabacloud_sts20150401.client import Client as Sts20150401Client
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient

from log_settings import logger
from utils.aliyun_cloud import *

for param in (access_key_id, access_key_secret, bucket_name, endpoint, sts_role_arn):
    assert '<' not in param, 'please setup param:' + param


class StsToken(object):
    """
    :param access_key_id: 临时凭证的访问key_id
    :param access_key_secret: 临时凭证的访问key_secret
    :param expiration: 临时凭证的过期时间
    :param security_token: 临时凭证的安全token
    :param request_id: 请求id
    """

    def __init__(self):
        self.access_key_id = ''
        self.access_key_secret = ''
        self.expiration = 0
        self.security_token = ''
        self.request_id = ''

    @staticmethod
    def create_client(region_id: str) -> Sts20150401Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config.endpoint = 'sts.{}.aliyuncs.com'.format(region_id)
        return Sts20150401Client(config)


def gernate_sts_token(region_id: str, from_app_name: str) -> bool:
    """
    :return:
    """
    clt = StsToken.create_client(region_id)
    assume_role_request = sts_20150401_models.AssumeRoleRequest(
        duration_seconds=3600,
        role_arn=sts_role_arn,
        role_session_name=from_app_name
    )
    runtime = util_models.RuntimeOptions()
    try:
        resp = clt.assume_role_with_options(assume_role_request, runtime)
        return True, UtilClient.to_jsonstring(resp)


    except Exception as error:
        UtilClient.assert_as_string(error.message)
        logger.error("生成sts token异常：{}".format(str(error.message)))
        return False, str(error.message)
