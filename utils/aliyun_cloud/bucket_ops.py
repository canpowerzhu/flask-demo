# @Author  : kane.zhu
# @Time    : 2023/5/11 20:27
# @Software: PyCharm
# @Description: 获取当前账号下的所有bucket
import oss2
from utils.aliyun_cloud import access_key_id,access_key_secret


def get_all_bucket() -> list:
    auth = oss2.Auth(access_key_id, access_key_secret)
    oss_list_client = oss2.Service(auth, 'https://oss-cn-hangzhou.aliyuncs.com')

    return [ {'bucket_name': oss_item.name,'region_id':oss_item.location[4::],'extranet_endpoint':oss_item.extranet_endpoint,'intranet_endpoint':oss_item.intranet_endpoint} for oss_item in oss2.BucketIterator(oss_list_client)]
    # for oss_item in oss2.BucketIterator(oss_list_client):
    #     single_bucket_info = {'bucket_name': oss_item.name,
    #                           'region_id':oss_item.location[4::],
    #                           'extranet_endpoint':oss_item.extranet_endpoint,
    #                           'intranet_endpoint':oss_item.intranet_endpoint}
    #     print(single_bucket_info)
