# @Author  : kane.zhu
# @Time    : 2023/7/11 14:35
# @Software: PyCharm
# @Description:
import json

from sqlalchemy import and_

from dao.models import WorkOrderCategory, db, WorkOrderFlow, WorkOrder
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
        parent_category_list = db.session.query(WorkOrderCategory).filter(WorkOrderCategory.blocked == '0').distinct(
            WorkOrderCategory.work_order_category_name).all()
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
        child_category_list = db.session.query(WorkOrderCategory.work_order_second_category_name).filter(and_(
            WorkOrderCategory.work_order_category_name == parent_category_name, WorkOrderCategory.blocked == "0")).all()
    except Exception as e:
        logger.error(e)
        return False, e
    return True, child_category_list


def db_ops_update_ticket_category(id: int, update_data: dict):
    """
    更新目录信息，其中包含删除（逻辑删除）
    :param id: 更新的索引id
    :param update_data: 新的数据对象
    :return:
    """
    try:

        WorkOrderCategory.query.filter(WorkOrderCategory.id == id).update(update_data)
        db.session.commit()
        logger.info("更新数据库，请求体是{}".format(json.dumps(update_data)))
    except Exception as e:
        logger.error(e)
        return False, e
    return True, None


# 查询工单目录和工单流程数据
def check_work_order_category():
    """
    校验工单类目是否为空的判断
    :return:
    """
    category_count = WorkOrderCategory.query.count()
    print("工单类目数量:{}".format(category_count))
    return True if category_count == 0 else False


def check_work_order_flow():
    """
    校验工单使用的流程是否为空的判断
    :return:
    """
    flow_count = WorkOrderFlow.query.count()
    print("工单流程数量:{}".format(flow_count))
    return True if flow_count == 0 else False


def db_ops_add_ticket_flow(work_order_flow_dict):
    """
    工单流程的新建，插入落库
    :param work_order_flow_dict: 工单流程新建请求体
    :return:
    """
    try:
        db.session.execute(WorkOrderFlow.__table__.insert(), work_order_flow_dict)
        db.session.commit()
    except Exception as e:
        logger.error(e)
        return False, e

    return True


def db_ops_add_work_order(work_order_dict):
    """
    工单入库，sql插入操作
    :param work_order_dict: 请求体
    :return:
    """
    try:
        db.session.execute(WorkOrder.__table__.insert(), work_order_dict)
        db.session.commit()
    except Exception as e:
        logger.error(e)
        return False, e

    return True
