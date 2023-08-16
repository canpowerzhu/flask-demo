# @Author  : kane.zhu
# @Time    : 2023/8/10 17:15
# @Software: PyCharm
# @Description:
import json

from sqlalchemy import or_

from dao.models import ProjectInfo
from dao.models import db
from log_settings import logger


def add_project_info_db(project_info_dict)-> bool:
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
