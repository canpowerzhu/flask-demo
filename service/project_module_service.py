import json

# @Author  : kane.zhu
# @Time    : 2023/8/10 17:06
# @Software: PyCharm
# @Description:
from dao.models import ProjectInfoSchema
from marshmallow import ValidationError
from dao.ops_db_project_module import add_project_info_db
from log_settings import logger
from flask import request


def add_project_info_service(project_data)->bool:
    """
    :param project_data:
    :return:
    service层 衔接DO数据层
    """
    return True if add_project_info_db(project_data) else False



