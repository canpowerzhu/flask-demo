# @Author  : kane.zhu
# @Time    : 2023/8/9 11:09
# @Software: PyCharm
# @Description: 系统配置处理服务
from flask import request

from dao.ops_db_config_info import add_sys_config_info, get_sys_config_list
from log_settings import logger


def add_config_item(add_item_dict: dict) -> bool:
    """
    :param add_item_dict:
    :return: boolean
    """
    return True if add_sys_config_info(add_item_dict) else False


def update_config_item(update_item_dict: dict) -> bool:
    """
    :param update_item_dict:
    :return: boolean
    """
    return True if update_item_dict(update_item_dict) else False


def get_config_list(config_key=None,config_name=None,config_group=None):
    """
    :return:
    """
    query_sql_express = get_sys_config_list(config_key=config_key,config_name=config_name,config_group=config_group)


    status, result = query_sql_express
    if status:
        logger.info("来自请求：{}, 查询语句是： {}，查询结果: {}".format(request.trace_id,str(query_sql_express), result))
        return status, result
