# @Author  : kane.zhu
# @Time    : 2022/11/8 14:48
# @Software: PyCharm
# @Description:


from flask import Blueprint, jsonify

user_crud_bp = Blueprint('user_crud', __name__)


@user_crud_bp.route('/v1/user', methods=['GET'])
def get_user():
    resp = {'status': 200, 'msg': 'success', 'data': 'this is v1 data'}
    return jsonify(resp)
