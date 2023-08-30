# @Author  : kane.zhu
# @Time    : 2023/8/10 17:15
# @Software: PyCharm
# @Description:
import json

from dao.models import ProjectInfo, ModuleInfo, ProjectModulePlaybook,ProjectModulePlaybookRelation
from dao.models import db

from dto.project_info_schema import ProjectInfoSchema
from dto.project_module_playbook_schema import ProjectModuleCombineSchema
from log_settings import logger


def add_project_info_db(project_info_dict) -> bool:
    """
    :param project_info_dict:
    :return:
    """
    try:
        db.session.execute(ProjectInfo.__table__.insert(), [project_info_dict])
        db.session.commit()
    except Exception as e:
        logger.error(e)
        return False

    return True




def update_project_info_db(id: int, project_info_data: dict) -> bool:
    """
    :param id:
    :param project_info_data:
    :return:
    """
    try:

        ProjectInfo.query.filter(ProjectInfo.id == id).update(project_info_data)
        db.session.commit()
        logger.info("更新数据库，请求体是{}".format(json.dumps(project_info_data)))
    except Exception as e:
        logger.error(e)
        return False, e
    return True, None


def get_project_list_db(project_name=None, project_code=None) -> object:
    """
    获取项目信息，可以根据project_name,project_code进行单独或者联合查询 模糊查询
    :param project_name:
    :param project_code:
    :return:
    """
    query = db.session.query(ProjectInfo)

    if project_name:
        query = query.filter(ProjectInfo.project_name.like(f'%{project_name}%'))

    if project_code:
        query = query.filter(ProjectInfo.project_code.like(f'%{project_code}%'))

    try:
        result = query.all()

        # 借助marshmallow 格式化数据
        result_list_dict = ProjectInfoSchema().dump(result, many=True)
        logger.info("查询的参数是project_name:{},project_code:{}---响应体是{}".format(project_name, project_code,
                                                                                      result_list_dict))
        return True, result_list_dict
    except Exception as e:
        logger.error(e)
        return False, e

def get_project_name_by_id_db(project_id:int) -> object:
    """
    依据id 获取项目名称，用于创建模块时候的目录挂在路径命名
    :param id:
    :return:
    """
    try:
        project_code = db.session.query(ProjectInfo.project_code).filter(ProjectInfo.id == project_id).first()[0]
        return True, project_code
    except Exception as e:
        logger.error(e)
        return False, e


def add_module_info_db(module_info_dict) -> bool:
    """
    :param module_info_dict:
    :return:
    """
    try:
        db.session.execute(ModuleInfo.__table__.insert(), [module_info_dict])
        db.session.commit()
    except Exception as e:
        logger.error(e)
        return False

    return True


def get_project_module_info(module_id: int):
    """
    :param module_id: 获取模块的 相关信息
    :return:
    """
    try:
        result = db.session.query(
        ModuleInfo.id,
        ModuleInfo.project_id,
        ModuleInfo.module_name,
        ModuleInfo.module_package_name,
        ModuleInfo.module_rel_path,
        ModuleInfo.module_env_pairs,
        ModuleInfo.module_port_pairs,
        ModuleInfo.module_host_pairs,
        ModuleInfo.module_volumes_pairs,
        ModuleInfo.dump_oom_status,
        ModuleInfo.dump_oom_path,
        ModuleInfo.debug_status,
        ModuleInfo.debug_status_port,
        ModuleInfo.start_define_params,
        ModuleInfo.module_memory,
        ModuleInfo.project_cloud_platform,
        # Add ProjectInfo fields...
        ProjectInfo.project_name,
        ProjectInfo.project_code,
        ProjectInfo.base_image_name,
        ProjectInfo.health_check_interval,
        ProjectInfo.health_check_timeout,
        ProjectInfo.health_check_retries,
        ProjectInfo.health_check_start_period
        # Add other fields...
    ).join(ProjectInfo, ModuleInfo.project_id == ProjectInfo.id).filter(ModuleInfo.id == module_id).first()

        # 借助marshmallow 格式化数据
        result_list_dict = ProjectModuleCombineSchema().dump(result)
        logger.info("查询的参数是module_id:{},查询的结果是{}".format(module_id,result_list_dict))
        return True, result_list_dict
    except Exception as e:
        logger.error(e)
        return False, e



def add_project_module_playbook_db(module_id:int,project_module_playbook_dict) -> bool:
    """
    :param project_module_playbook_dict:
    :return:
    """
    try:
        # 新增playbook完成后，去更新模块和playbook表
        db.session.execute(ProjectModulePlaybook.__table__.insert(), [project_module_playbook_dict])
        db.session.commit()


        md5_str =  project_module_playbook_dict['md5']
        add_playbook_obj = ProjectModulePlaybookRelation(playbook_md5=md5_str,project_module_id=module_id)
        db.session.add(add_playbook_obj)
        db.session.commit()
        logger.info("更新tbl_playbook_relation表. module_id is {}, md5_str is {}".format(module_id, md5_str))
        return True
    except Exception as e:
        logger.error(e)
        return False




