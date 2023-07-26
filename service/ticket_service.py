# @Author  : kane.zhu
# @Time    : 2023/7/7 16:35
# @Software: PyCharm
# @Description:
import json

from flask import request

from dao.ops_ticket import db_ops_add_ticket_category, db_ops_get_ticket_child_category, \
    db_ops_get_ticket_parent_category, db_ops_update_ticket_category, check_work_order_category, check_work_order_flow
from log_settings import logger


class TicketService(object):
    def __init__(self):
        pass

    @staticmethod
    def get_ticket_list(**kwargs):
        if not kwargs:
            status, res = db_ops_get_ticket_parent_category()
            if status:
                logger.info("来自请求：{}；获取父级分类信息:{}".format(request.trace_id, res))
        else:
            status, res = db_ops_get_ticket_child_category(kwargs['category_parent_name'])
            if status:
                print("查询 {} 父级目录下的二级的结果是：{}".format(kwargs['category_parent_name'], res))

        return res

    @staticmethod
    def add_ticket_category(req_data):
        try:
            db_ops_add_ticket_category(req_data)
            res = "success"
            status = True
        except Exception as e:
            logger.error("增加流程工单类别异常:{}".format(e))
            res = e
            status = True
        return res, status

    @staticmethod
    def update_ticket(item_id: int, **kwargs):
        if not kwargs:
            delete_body = {'blocked': 1}
            db_ops_update_ticket_category(item_id, delete_body)
            logger.info("禁用了工单类目，编号是{}，禁用的字段体是{}".format(str(item_id), json.dumps(kwargs)))

        else:
            logger.info("进入更新,更新的请求体是{}".format(json.dumps(kwargs)))
            # db_ops_update_ticket_category(item_id, delete_body)

        return "OK"


class WorkOrderService(object):
    def __init__(self):
        pass

    def check_category_count(self) -> bool:
        """
        校验工单类目是否为空
        :return: bool
        """
        return check_work_order_category()

    def check_work_flow_count(self) -> bool:
        """
        校验工作流是否为空
        :return: bool
        """
        return check_work_order_flow()
