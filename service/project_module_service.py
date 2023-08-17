# @Author  : kane.zhu
# @Time    : 2023/8/10 17:06
# @Software: PyCharm
# @Description:

from flask import request

from dao.ops_db_project_module import add_project_info_db, get_project_list_db,update_project_info_db
from log_settings import logger


def add_project_info_service(project_data) -> bool:
    """
    :param project_data:
    :return:
    service层 衔接DO数据层
    """
    return True if add_project_info_db(project_data) else False


def get_project_list_service(project_name=None, project_code=None):
    """
    :return:
    """
    query_sql_express = get_project_list_db(project_name=project_name, project_code=project_code)

    status, result = query_sql_express
    if status:
        logger.info("来自请求：{}, 查询语句是： {}，查询结果: {}".format(request.trace_id, str(query_sql_express), result))
        return status, result


def update_project_info_service(id: int,update_project_data:dict):
    status, result = update_project_info_db(id,update_project_data)
    if status:
        logger.info("来自请求：{}, 更新项目信息{}".format(request.trace_id, result))
        return status, result
