# @Author  : kane.zhu
# @Time    : 2023/7/11 14:35
# @Software: PyCharm
# @Description:

# @Author  : kane.zhu
# @Time    : 2023/2/24 16:58
# @Software: PyCharm
# @Description:

from sqlalchemy import distinct

from dao.models import WorkOrderCategory, db
from log_settings import logger


def db_ops_add_ticket_category(category_data_dict):
    try:
        db.session.execute(WorkOrderCategory.__table__.insert(), category_data_dict)
        db.session.commit()
    except Exception as e:
        logger.error(e)
        return False, e

    return True


def db_ops_get_ticket_parent_category():
    """
    获取工单分类的父级目录名称
    :return:
    """
    try:
        parent_category_list = db.session.query(distinct(WorkOrderCategory.work_order_category_name)).all()
    except Exception as e:
        logger.error(e)
        return False, e
    return True, parent_category_list


def db_ops_get_ticket_child_category(parent_category_name):
    """
    获取父级工单分类的子级
    :return:
    """
    try:
        child_category_list = db.session.query(WorkOrderCategory.work_order_second_category_name).filter(
            WorkOrderCategory.work_order_category_name == parent_category_name).distinct(
            WorkOrderCategory.work_order_second_category_name).all()
    except Exception as e:
        logger.error(e)
        return False, e
    return True, child_category_list
