# @Author  : kane.zhu
# @Time    : 2023/8/10 17:15
# @Software: PyCharm
# @Description:
import json

from dao.models import ProjectInfo
from dao.models import db
from dto.project_info_schema import ProjectInfoSchema
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
