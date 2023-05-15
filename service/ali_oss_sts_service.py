# @Author  : kane.zhu
# @Time    : 2023/5/12 16:01
# @Software: PyCharm
# @Description:
import json

from utils.oss_aliyun.sts_token import gernate_sts_token


def gernate_sts_token_service(region_id: str,from_app_name:str) -> dict:
    sts_token_status, sts_token_obj = gernate_sts_token(region_id,from_app_name)
    if sts_token_status:
        sts_token_data = json.loads(sts_token_obj)['body']
        message = "success"
    else:
        message = "failed"
        sts_token_data = sts_token_obj

    return {'code': 200, 'message': message, 'data': sts_token_data}


