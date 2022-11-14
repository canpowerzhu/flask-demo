# @Author  : kane.zhu
# @Time    : 2022/11/8 21:48
# @Software: PyCharm
# @Description:
import oss2

from settings.conf import PrdConfig

access_key_id = PrdConfig.OSS_ACCESS_KEY_ID
access_key_secret = PrdConfig.OSS_ACCESS_KEY_SECRET
bucket_name = PrdConfig.OSS_BUCKET
endpoint = PrdConfig.OSS_ENDPOINT


if not PrdConfig.OSS_STS_ARN is None:
    sts_role_arn = PrdConfig.OSS_STS_ARN