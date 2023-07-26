# @Author  : kane.zhu
# @Time    : 2023/3/21 17:57
# @Software: PyCharm
# @Description:
import json

from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkcore.client import AcsClient
from aliyunsdkdomain.request.v20180129.QueryDomainListRequest import QueryDomainListRequest
from flask import current_app

from dao.ops_db_domain import db_ops_root_domain_bulk, db_ops_sub_domain_bulk, db_ops_get_root_domain
from log_settings import logger
from settings.conf import PrdConfig


#### 阿里云域名相关同步


def ali_cloud_domain_sync():
    client = AcsClient(PrdConfig.ACCESS_KEY_ID, PrdConfig.ACCESS_SECRET, 'cn-hangzhou')
    request = QueryDomainListRequest()
    request.set_accept_format('json')
    request.set_PageNum(1)
    request.set_PageSize(50)

    response = client.do_action_with_exception(request)
    data = json.loads(response.decode('utf-8'))['Data']['Domain']
    domainlist = []
    for i in range(len(data)):
        # ali_cloud_domain_record(data[i]['DomainName'], client)
        single_domain_info_data = {
            "name_account": PrdConfig.ALI_USERNAME,
            "domain_name": data[i]['DomainName'],
            "locked": 0,
            "autorenew_enabled": 0,
            "expire_date": data[i]['ExpirationDate'].split(' ')[0],
            "create_date": data[i]['RegistrationDate'].split(' ')[0],
        }
        domainlist.append(single_domain_info_data)
    db_ops_root_domain_bulk(domainlist)
    logger.info("域名账号{}，总共同步{}".format(PrdConfig.ALI_USERNAME, len(data)))
    return True


def direct_async_ali_cloud_record():
    status_domain, root_domain = db_ops_get_root_domain(PrdConfig.ALI_USERNAME)
    if status_domain:
        for root_domain_item in root_domain:
            logger.info("开始同步{}域名的解析记录".format(root_domain_item.domain_name))
            ali_cloud_domain_record(root_domain_item.domain_name)


def ali_cloud_domain_record(domain):
    """
    阿里云万网域名接口 内部调用域名解析记录详情
    """
    client = AcsClient(PrdConfig.ACCESS_KEY_ID, PrdConfig.ACCESS_SECRET, 'cn-hangzhou')
    request = DescribeDomainRecordsRequest()
    request.set_accept_format('json')
    request.set_DomainName(domain)
    request.set_PageSize(PrdConfig.DOMAIN_RECORD_PAGE_SIZE)

    response = client.do_action_with_exception(request).decode('utf-8')
    records_list = json.loads(response)['DomainRecords']['Record']
    record_arr = []
    for record_info in records_list:
        record_info_data = {
            "register_website": "www.aliyun.com",
            "name_account": PrdConfig.ALI_USERNAME,
            "domain_name": record_info['DomainName'],
            "fqdn": record_info['RR'] + '.' + record_info['DomainName'],
            "type": record_info['Type'],
            "answer": record_info['Value']
        }
        record_arr.append(record_info_data)
    logger.info("阿里云域名{}的解析记录数量是{}".format(domain, len(records_list)))
    # 插入有记录的
    db_ops_sub_domain_bulk(current_app._get_current_object(), record_arr, domain, len(record_arr))
