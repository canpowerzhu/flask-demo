# @Author  : kane.zhu
# @Time    : 2022/11/14 10:54
# @Software: PyCharm
# @Description:
from flask import Blueprint, request, jsonify

from log_settings import logger
from service.ali_oss_sts_service import gernate_sts_token_service
from utils.aliyun_cloud.bucket_ops import get_all_bucket

sts_api_bp = Blueprint('aliyun_oss_sts', __name__)


@sts_api_bp.route('/oss_sts_token', methods=['GET'])
def get_sts_token():
    # todo 这里需要校验Region_id 的合理存在问题
    region_id = request.args.get('region_id')
    from_app_name = request.args.get('from_app_name')
    gernate_sts_token_res = gernate_sts_token_service(request.trace_id, region_id, from_app_name)
    logger.info("来自请求：{}；获取临时身份认证信息：{}".format(request.trace_id, gernate_sts_token_res))
    return jsonify(gernate_sts_token_res)


@sts_api_bp.route('/oss_bukect_infos', methods=['GET'])
def get_bucket_info_list():
    bucket_list = get_all_bucket()
    return jsonify({'buckets': bucket_list})


@sts_api_bp.route('/object_upload', methods=['POST'])
def upload_object():
    return jsonify({"code": 200, "message": "success", "data": {"access_url": "https://ww.so.om/t.txt"}})
