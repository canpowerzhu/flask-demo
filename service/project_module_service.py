import json

# @Author  : kane.zhu
# @Time    : 2023/8/10 17:06
# @Software: PyCharm
# @Description:
from dao.models import ProjectInfoSchema
from dao.ops_db_project_module import add_project_info_db
from log_settings import logger
from flask import request


def add_project_info_service(project_data):
    print("数据是{}，类型{}".format(project_data,type(project_data)))
    project_schema = ProjectInfoSchema()
    before_db_data = project_schema.load(project_data)
    logger.info("来自请求：{}, 检验参数成功进入，入库前-数据处理后: {}".format(request.trace_id,before_db_data))

    return True if add_project_info_db(before_db_data) else False