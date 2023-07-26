# @Author  : kane.zhu
# @Time    : 2022/11/8 21:48
# @Software: PyCharm
# @Description:

from alibabacloud_tea_openapi import models as open_api_models

from settings.conf import PrdConfig

access_key_id = PrdConfig.OSS_ACCESS_KEY_ID
access_key_secret = PrdConfig.OSS_ACCESS_KEY_SECRET
bucket_name = PrdConfig.OSS_BUCKET
endpoint = PrdConfig.OSS_ENDPOINT

if not PrdConfig.OSS_STS_ARN is None:
    sts_role_arn = PrdConfig.OSS_STS_ARN

# 初始化短信服务请求config object

config = open_api_models.Config(
    # 必填，您的 AccessKey ID,
    access_key_id=access_key_id,
    # 必填，您的 AccessKey Secret,
    access_key_secret=access_key_secret
)
# 访问的域名
