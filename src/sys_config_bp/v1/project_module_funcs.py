# @Author  : kane.zhu
# @Time    : 2023/8/10 17:43
# @Software: PyCharm
# @Description:


from flask import Blueprint, request, jsonify
from log_settings import logger
from dao.models import ProjectInfoSchema
from marshmallow import ValidationError
from service.project_module_service import add_project_info_service
from utils.custom_status_code_message import generate_response,CustomStatusCode


project_module_bp = Blueprint("project_module_bp", __name__)
project_schema = ProjectInfoSchema()
@project_module_bp.route("/item", methods=["POST"])
def create_project_info():
    """
    校验参数统一在路由层进行，数据处理放在service
    :return:
    """
    request_data = request.json

    try:
        project_schema.validate(request_data)
    except ValidationError as e:
        logger.error("来自请求：{}, 检验参数失败: {}".format(request.trace_id,str(e)))
        return generate_response(CustomStatusCode.BAD_REQUEST,str(e))
    logger.info("来自请求：{}, 请求体是: {}".format(request.trace_id, request_data))
    status =  add_project_info_service(request_data)

    return generate_response(CustomStatusCode.CREATED,request_data) if status else generate_response(CustomStatusCode.INTERNAL_SERVER_ERROR,request_data)