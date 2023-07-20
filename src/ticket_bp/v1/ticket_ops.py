# @Author  : kane.zhu
# @Time    : 2023/7/7 16:25
# @Software: PyCharm
# @Description: 这是工单模块
from flask import Blueprint, jsonify,request
from log_settings import logger
from settings.schema_models import AddWorkFlowCategory
from service.ticket_service import TicketService


ticket_bp = Blueprint('ticket_bp', __name__)



@ticket_bp.route("/ticket_category",methods=["GET"])
def get_ticket_category():
    # 管理工单创建时的分类选项

    get_param = request.args.get("parent_name")
    category_obj = TicketService()
    if get_param is None:
        res_list = [ item[0] for item in category_obj.get_ticket_list()]
        logger.info("来自请求：{}；获取父级分类信息:{}".format(request.trace_id,res_list))

    else:
        print(category_obj.get_ticket_list(category_parent_name=get_param))
        res_list = [item[0]  for item in category_obj.get_ticket_list(category_parent_name=get_param) ]
        logger.info("来自请求：{}；获取{}的子级分类信息{}".format(request.trace_id,get_param,res_list))

    return jsonify({"code": 200, "status": "success", "data": res_list})

@ticket_bp.route("/ticket_category", methods=["POST"])
def manage_ticket_category():
    request_data = request.json
    try:
        AddWorkFlowCategory(**request_data)
    except Exception as e:
        # 校验失败
        return jsonify({"error": str(e)}), 400

    print("request_data:{},type:{}".format(request_data,type(request_data)))
    ticket_obj = TicketService()
    res,status =ticket_obj.add_ticket_category(request_data)
    final_dict = {"code":200,"status":"success"} if status else {"code":500,"status":"failed","data":res}
    return  jsonify(final_dict)


@ticket_bp.route("/ticket_category", methods=["PUT","DELETE"])
def update_ticket_category():
    if request.method == "DELETE":
        logger.info("来自请求：{}；增加工单系统的分类信息：{}".format(request.trace_id, 'dd'))

    if request.method == "PUT":
        logger.info("来自请求：{}；更新工单系统的分类信息：{}".format(request.trace_id, 'dd'))


    return  jsonify({"code":200,"status":"success","data":"data"})