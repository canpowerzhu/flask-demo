# @Author  : kane.zhu
# @Time    : 2022/11/8 14:48
# @Software: PyCharm
# @Description:


from flask import Blueprint, jsonify

user_crud_bp = Blueprint('user_crud', __name__,url_prefix="/v1/user")


@user_crud_bp.route('/demo_data', methods=['GET'])
def get_user():
    resp = {'status': 200, 'msg': 'success', 'data': 'this is v1 data'}
    return jsonify(resp)
