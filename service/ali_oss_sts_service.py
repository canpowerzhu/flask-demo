# @Author  : kane.zhu
# @Time    : 2023/5/12 16:01
# @Software: PyCharm
# @Description:
from utils.oss_aliyun.sts_token import gernate_sts_token


def gernate_sts_token_service(region_id: str) -> dict:
    sts_token_status, sts_token_obj = gernate_sts_token(region_id)

    if sts_token_status:
        sts_token_data = {'access_key_id': sts_token_obj.access_key_id,
                          'access_key_secret': sts_token_obj.access_key_secret,
                          'security_token': sts_token_obj.security_token,
                          'expiration_time': sts_token_obj.expiration}
        message = "success"
    else:
        message = "failed"
        sts_token_data = sts_token_obj

    return {'code': 200, 'message': message, 'data': sts_token_data}
