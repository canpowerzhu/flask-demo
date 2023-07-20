# @Author  : kane.zhu
# @Time    : 2023/7/7 16:35
# @Software: PyCharm
# @Description:
from flask import request

from dao.ops_ticket import db_ops_add_ticket_category,db_ops_get_ticket_child_category,db_ops_get_ticket_parent_category
from log_settings import logger



class TicketService(object):
    def __init__(self):
        pass

    @staticmethod
    def get_ticket_list(**kwargs):
        if not kwargs:
            status,res = db_ops_get_ticket_parent_category()
            if status:
                logger.info("来自请求：{}；获取父级分类信息:{}".format(request.trace_id,res))
        else:
            status, res = db_ops_get_ticket_child_category(kwargs['category_parent_name'])
            if status:
                print("查询 {} 父级目录下的二级的结果是：{}".format(kwargs['category_parent_name'],res))

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

    # @staticmethod
    # def get_parent_category():
    #     pass

    def update_ticket(self):
        pass
