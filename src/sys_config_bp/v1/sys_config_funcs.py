# @Author  : kane.zhu
# @Time    : 2023/8/9 11:26
# @Software: PyCharm
# @Description:


from flask import Blueprint, request, jsonify
from service.sys_config_info_service import add_config_item, get_config_list
from log_settings import logger
from settings.schema_models import CreateConfigItem
from utils.custom_status_code_message import generate_response,CustomStatusCode


sysconfig_bp = Blueprint("sysconfig_bp", __name__)


@sysconfig_bp.route("/item/list", methods=["GET"])
def get_config_info():
    status,result = get_config_list()
    return generate_response(CustomStatusCode.OK,result) if status else generate_response(CustomStatusCode.INTERNAL_SERVER_ERROR)


@sysconfig_bp.route("/item", methods=["POST"])
def create_config_info():
    request_data = request.json
    try:
        CreateConfigItem(**request_data)
    except Exception as e:
        # 校验失败
        logger.error("来自请求：{}, 检验参数失败: {}".format(request.trace_id,str(e)))
        return jsonify({"error": str(e)}), 400

    status =  add_config_item(request_data)

    return generate_response(CustomStatusCode.CREATED,request_data) if status else generate_response(CustomStatusCode.INTERNAL_SERVER_ERROR,request_data)
