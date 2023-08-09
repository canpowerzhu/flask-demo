# @Author  : kane.zhu
# @Time    : 2023/8/9 11:09
# @Software: PyCharm
# @Description: 系统配置处理服务
from dao.ops_db_config_info import add_sys_config_info, get_sys_config_list
from log_settings import logger
from flask import request

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


def get_config_list(config_name=None,config_key=None,config_group=None):
    """
    :return:
    """
    status,result = get_sys_config_list()
    if status:
        print(result,type(result))
        logger.info("来自请求：{}, 查询结构: {}".format(request.trace_id,result))
        return status,result
    # get_sys_config_list() if  config_name else get_sys_config_list(config_name)
    # get_sys_config_list() if  config_key else get_sys_config_list(config_key)
    # get_sys_config_list() if  config_group else get_sys_config_list(config_group)

