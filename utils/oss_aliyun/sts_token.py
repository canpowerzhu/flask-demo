# @Author  : kane.zhu
# @Time    : 2022/11/12 10:38
# @Software: PyCharm
# @Description:
import json

from aliyunsdksts.request.v20150401 import AssumeRoleRequest
from aliyunsdkcore import client
from utils.oss_aliyun import *
from log_settings import logger

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


def gernate_sts_token(region_id: str)-> bool:
    """
    :param region_id:
    :param access_key_id:
    :param access_key_secret:
    :param role_arn:
    :return:
    """
    clt = client.AcsClient(access_key_id, access_key_secret, region_id)
    req = AssumeRoleRequest.AssumeRoleRequest()

    req.set_accept_format('json')
    req.set_RoleArn(sts_role_arn)
    req.set_RoleSessionName('oss-python-sdk-example')
    try:
        body = clt.do_action_with_exception(req)
        j = json.loads(oss2.to_unicode(body))
        token = StsToken()
        token.access_key_id = j['Credentials']['AccessKeyId']
        token.access_key_secret = j['Credentials']['AccessKeySecret']
        token.security_token = j['Credentials']['SecurityToken']
        token.request_id = j['RequestId']
        token.expiration = oss2.utils.to_unixtime(j['Credentials']['Expiration'], '%Y-%m-%dT%H:%M:%SZ')
        return True,token

    except  Exception as e:
        logger.error("生成sts token异常：{}".format(str(e)))
        return False,str(e)

