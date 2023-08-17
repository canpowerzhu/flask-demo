# @Author  : kane.zhu
# @Time    : 2023/8/10 17:43
# @Software: PyCharm
# @Description:


from flask import Blueprint, request
from marshmallow import ValidationError

from dao.models import ProjectInfoSchema
from log_settings import logger
from service.project_module_service import add_project_info_service, get_project_list_service,update_project_info_service
from utils.custom_status_code_message import generate_response, CustomStatusCode

project_module_bp = Blueprint("project_module_bp", __name__)


@project_module_bp.route("/item", methods=["POST"])
def create_project_info():
    """
    校验参数统一在路由层进行，数据处理放在service
    :return:
    """
    request_data = request.json
    try:
        res_data = ProjectInfoSchema().load(request_data)
    except ValidationError as error:
        logger.error("来自请求：{}, 检验参数失败: {}".format(request.trace_id, str(error.messages)))
        return generate_response(CustomStatusCode.BAD_REQUEST, str(error.messages))

    logger.info("来自请求：{}, 请求体是: {}".format(request.trace_id, res_data))
    status = add_project_info_service(res_data)
    return generate_response(CustomStatusCode.CREATED, res_data) if status else generate_response(
        CustomStatusCode.INTERNAL_SERVER_ERROR, res_data)


@project_module_bp.route("/item/list", methods=["GET"])
def get_project_list():
    """
    校验参数统一在路由层进行，数据处理放在service
    :return:
    """
    if request.args:
        allowed_params = {'project_name', 'project_code'}
        disablled_params = set(request.args.keys()) - allowed_params
        if disablled_params:
            return generate_response(CustomStatusCode.BAD_REQUEST, 'Invalid params ')
    project_name_v = request.args.get('project_name') if request.args.get('project_name') else None
    project_code_v = request.args.get('project_code') if request.args.get('project_code') else None

    status, result = get_project_list_service(project_name=project_name_v, project_code=project_code_v)
    return generate_response(CustomStatusCode.OK, result) if status else generate_response(
        CustomStatusCode.INTERNAL_SERVER_ERROR)

@project_module_bp.route("/item/<id>", methods=["PUT"])
def update_project_item(id):
    """
    校验参数统一在路由层进行，数据处理放在service
    :return:
    """
    if id is None and not isinstance(id,int):
        return generate_response(CustomStatusCode.BAD_REQUEST, 'please check id ')
    request_update_data = request.json
    try:
        res_data = ProjectInfoSchema().load(request_update_data)
    except ValidationError as error:
        logger.error("来自请求：{}, 检验参数失败: {}".format(request.trace_id, str(error.messages)))
        return generate_response(CustomStatusCode.BAD_REQUEST, str(error.messages))

    status, result = update_project_info_service(id,res_data)
    return generate_response(CustomStatusCode.OK, result) if status else generate_response(
        CustomStatusCode.INTERNAL_SERVER_ERROR)
