# @Author  : kane.zhu
# @Time    : 2023/8/10 17:06
# @Software: PyCharm
# @Description:

from flask import request

from dao.ops_db_project_module import add_project_info_db, get_project_list_db, update_project_info_db, \
    add_module_info_db, get_project_module_info, add_project_module_playbook_db, get_project_name_by_id_db
from log_settings import logger
from utils.generate_result_yaml import MakeModuleYaml
from utils.make_md5 import calculate_md5


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


def update_project_info_service(id: int, update_project_data: dict):
    status, result = update_project_info_db(id, update_project_data)
    if status:
        logger.info("来自请求：{}, 更新项目信息{}".format(request.trace_id, result))
        return status, result


def add_module_info_service(module_data) -> bool:
    """
    :param project_data:
    :return:
    service层 衔接DO数据层
    """
    # 这里需要将module_data进行整合，将volumes的挂载信息处理
    print(module_data, type(module_data))
    status, project_code = get_project_name_by_id_db(module_data['project_id'])
    if not status:
       return False

    module_volumes_pairs = {'/application/logs/{}'.format(module_data['module_name']): '/mnt/logs',
                            '/applicaiton/jar_package/{}/{}/{}'.format(project_code, module_data['module_name'],
                                                                       module_data[
                                                                           'module_package_name']): '/mnt/{}'.format(
                                module_data['module_package_name'])}

    module_data['module_volumes_pairs'] = module_volumes_pairs
    return True if add_module_info_db(module_data) else False


def generate_project_module_playbook_service(module_id: int) -> bool:
    status, res = get_project_module_info(module_id)
    if not status:
        return False
    mk_yaml_obj = MakeModuleYaml(res)
    playbook_str = mk_yaml_obj.make_yaml()
    project_module_playbook_dict = {
        'md5': calculate_md5(playbook_str),
        'content': playbook_str,
        'src_ip': request.remote_addr,
        'type': 'YAML'
    }
    add_playbook_content_status = add_project_module_playbook_db(project_module_playbook_dict)
    if not add_playbook_content_status:
        return False, None
    logger.info("service层的结果是{}".format(res))
    return True, res
