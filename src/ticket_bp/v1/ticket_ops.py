# @Author  : kane.zhu
# @Time    : 2023/7/7 16:25
# @Software: PyCharm
# @Description: 这是工单模块

from flask import Blueprint, jsonify, request

from log_settings import logger
from service.ticket_service import TicketService,WorkOrderService
from settings.schema_models import AddWorkFlowCategory,CreateWorkFlow,CreateWorkOrder

ticket_bp = Blueprint('ticket_bp', __name__)


@ticket_bp.route("/ticket_category", methods=["GET"])
def get_ticket_category():
    # 管理工单创建时的分类选项

    get_param = request.args.get("parent_name")
    category_obj = TicketService()
    if get_param is None:
        res_list = [item[0] for item in category_obj.get_ticket_list()]
        logger.info("来自请求：{}；获取父级分类信息:{}".format(request.trace_id, res_list))

    else:
        res_list = [item[0] for item in category_obj.get_ticket_list(category_parent_name=get_param)]
        logger.info("来自请求：{}；获取{}的子级分类信息{}".format(request.trace_id, get_param, res_list))

    return jsonify({"code": 200, "status": "success", "data": res_list})


@ticket_bp.route("/ticket_category", methods=["POST"])
def manage_ticket_category():
    request_data = request.json
    try:
        AddWorkFlowCategory(**request_data)
    except Exception as e:
        # 校验失败
        return jsonify({"error": str(e)}), 400

    ticket_obj = TicketService()
    res, status = ticket_obj.add_ticket_category(request_data)
    logger.info("来自请求：{}----添加工单分类信息:父级-{} 子级-{}".format(request.trace_id,
                                                                         request_data['work_order_category_name'],
                                                                         request_data[
                                                                             'work_order_second_category_name']))

    final_dict = {"code": 200, "status": "success"} if status else {"code": 500, "status": "failed", "data": res}
    return jsonify(final_dict)


@ticket_bp.route("/ticket_category/<item_id>", methods=["PUT", "DELETE"])
def update_ticket_category(item_id):
    ticket_obj = TicketService()
    if request.method == "PUT":
        # 若请求体不为空，则是PUT更新请求
        logger.info(
            "来自请求：{}；更新工单系统的分类信息：{},请求体是:{}".format(request.trace_id, str(item_id), request.json))
    else:
        # 逻辑删除
        ticket_obj.update_ticket(item_id)
        logger.info("来自请求：{}；删除工单系统的分类信息：{}".format(request.trace_id, str(item_id)))

    return jsonify({"code": 200, "status": "success", "data": "data"})





@ticket_bp.route("/ticket_work_order",methods=["POST"])
def create_work_order():
    # 创建工单之前，工单类目必须不能为空 并且工单流程也不能为空
    work_order_obj = WorkOrderService()
    if work_order_obj.check_work_flow_count() or work_order_obj.check_category_count():
        logger.error("来自请求：{}, 工单类目或者工单流程为空".format(request.trace_id))
        return jsonify({"code": 5001, "status": "failed", "data": "工单类目或者工单流程为空,请先去创建"})

        # pydantic校验数据字段
    request_data = request.json
    try:
        CreateWorkOrder(**request_data)
    except Exception as e:
        # 校验失败
        return jsonify({"error": str(e)}), 400

    # 下面进行工单流程的创建
    res, status = work_order_obj.create_work_order(request_data)

    final_dict = {"code": 200, "status": "success"} if status else {"code": 500, "status": "failed", "data": res}
    return jsonify(final_dict)


@ticket_bp.route("/ticket_work_order_flow",methods=["POST"])
def create_work_order_flow():
    #创建工单流程之前，工单类目必须不能为空
    work_order_obj = WorkOrderService()
    if  work_order_obj.check_category_count():
        logger.error("来自请求：{}, 工单类目为空".format(request.trace_id))
        return jsonify({"code": 5011, "status": "failed", "data": "工单类目为空"})

    # pydantic校验数据字段
    request_data = request.json
    try:
        CreateWorkFlow(**request_data)
    except Exception as e:
        # 校验失败
        return jsonify({"error": str(e)}), 400

    # 下面进行工单流程的创建
    res, status =    work_order_obj.create_work_flow(request_data)

    final_dict = {"code": 200, "status": "success"} if status else {"code": 500, "status": "failed", "data": res}
    return jsonify(final_dict)