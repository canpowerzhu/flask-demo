# @Author  : kane.zhu
# @Time    : 2023/3/20 17:12
# @Software: PyCharm
# @Description:
import json
from concurrent.futures import ThreadPoolExecutor
import requests
from flask import current_app

from dao.ops_db_domain import get_domain_name_user_token, db_ops_root_domain_bulk, db_ops_get_token, \
    db_ops_get_root_domain, db_ops_sub_domain_bulk
from settings.conf import PrdConfig
from log_settings import logger

#### 域名接口
name_headers = {
    'Content-Type': 'application/json'
}


def sync_name_root_domain():
    status, res = get_domain_name_user_token()
    if status:
        res_from_db = res if len(res) >= 1 else None

    for account_info in res_from_db:
        res = requests.get(PrdConfig.NAME_API_URL,
                           headers=name_headers,
                           auth=(account_info[0], account_info[1]))

        if res.status_code != 200:
            logger.error("获取用户{}的域名，出现异常---{}".format(account_info[0], res.content))

        domainresult = json.loads(res.content.decode('utf-8'))['domains']
        logger.info("获取用户{}的域名，总数是{},详细结果----{}".format(account_info[0], len(domainresult), domainresult))

        # 组装批量插入数据[{}]

        insert_domain_arr = []
        for single_domain_info in domainresult:
            single_domain_info_data = {
                "name_account": account_info[0],
                "domain_name": single_domain_info['domainName'],
                "locked": 1 if 'locked' in single_domain_info and single_domain_info['locked'] == "True" else 0,
                "autorenew_enabled": 1 if 'autorenewEnabled' in single_domain_info else 0,
                "expire_date": single_domain_info['expireDate'].split('T')[0].split('T')[0],
                "create_date": single_domain_info['createDate'].split('T')[0],
            }
            insert_domain_arr.append(single_domain_info_data)
        db_ops_root_domain_bulk(insert_domain_arr)


def sync_sub_domain_info(account_username):
    pool_arr = []
    pool = ThreadPoolExecutor()
    status_token,account_token=db_ops_get_token(account_username)
    status_domain,root_domain=db_ops_get_root_domain(account_username)


    if status_domain and status_token:
        for root_domain_item in root_domain:
            pool_arr.append(pool.submit(async_sub_domain_record,current_app._get_current_object(), account_username,account_token.token,root_domain_item.domain_name))
            result = [i.result() for i in pool_arr]
            print("result:{}".format(result))


def async_sub_domain_record(self_app,account_username,account_token,root_domain):
    logger.info("进入异步线程去处理用户{},token是{},{}域名的记录信息".format(account_username,account_token,root_domain))
    submain_url = "{}/{}/records".format(PrdConfig.NAME_API_URL,root_domain)

    res = requests.get(submain_url,headers=name_headers,auth=(account_username, account_token))

    if res.status_code != 200:
        logger.error("获取用户{}的域名，出现异常---{}".format(account_username, res.content))

    # 字典为空判断，为空意味着没有解析
    recordresult = json.loads(res.content.decode('utf-8'))['records'] if  bool(json.loads(res.content.decode('utf-8'))) else []
        # 组装批量插入数据[{}]
    logger.info("获取用户{},域名{}，总数是{},详细结果----{}".format(account_username, root_domain, len(recordresult),
                                                                   recordresult))
    record_arr = []
    for record_info in recordresult:
        print(record_info)
        record_info_data = {
            "register_website": "www.name.com",
            "name_account": account_username,
            "domain_name": root_domain,
            "fqdn": record_info['fqdn'],
            "type": record_info['type'],
            "answer": record_info['answer']
        }
        record_arr.append(record_info_data)
    db_ops_sub_domain_bulk(self_app,record_arr,root_domain,len(recordresult))
