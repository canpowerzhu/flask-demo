# @Author  : kane.zhu
# @Time    : 2022/11/14 10:54
# @Software: PyCharm
# @Description:
from flask import Blueprint, request, jsonify
from utils.oss_aliyun.sts_token import gernate_sts_token

sts_api_bp = Blueprint('aliyun_oss_sts', __name__)


@sts_api_bp.route('/oss_sts_token', methods=['GET'])
def get_sts_token():
    region_id = request.args.get('region_id')
    sts_token = gernate_sts_token(region_id)
    return jsonify({'access_key_id': sts_token.access_key_id,
                    'access_key_secret': sts_token.access_key_secret,
                    'security_token': sts_token.security_token,
                    'expiration_time': sts_token.expiration})
