# @Author  : kane.zhu
# @Time    : 2023/4/19 11:47
# @Software: PyCharm
# @Description:
import json

from flask import Blueprint, request, jsonify
from src.gitlab_bp.v1 import gitlab_obj
from log_settings import logger

gitlab_bp = Blueprint("gitlab_bp", __name__)


# 这里可以不用delete, put 进行逻辑删除
@gitlab_bp.route("/user", methods=["GET"])
def gitlab_user_ops():
    if request.method == 'GET':
        res = gitlab_obj.users.list(get_all=True, iterator=True)
        record = []
        for list_item in res:
            if list_item.__dict__['_attrs']['state'] == 'active':
                record.append(list_item.__dict__['_attrs'])
        return jsonify({"code": 200, "message": "success", "count": len(record), "data": record})


@gitlab_bp.route("/user", methods=["POST"])

def create_user_ops():
    req_body = request.json
    required_params = {'email', 'password', 'username', 'name'}
    """
       可选参数      
        "public_email": "john@example.com",
        "commit_email": "john-codes@example.com",
        "is_admin": false|0,    
        "projects_limit": 100,
        "can_create_group": true|1,
        "can_create_project": true|1 #这个参数不用管 所有用户均可以创建工程
   """
    #  如果是普通用户，设置属性工程限制10，不可创建group
    if 'is_admin' not in req_body.keys() or req_body['is_admin'] == 0:
        req_body['projects_limit'] = 10
        req_body['can_create_group'] = False

    is_miss_params = True if required_params & set(req_body.keys()) == required_params else False
    if not is_miss_params:
        return jsonify({"code": 400, "message": "misses required params"})
    try:
        # 这里默认使用填写的邮箱
        req_body['public_email'] = req_body['email']
        req_body['commit_email'] = req_body['email']
        gitlab_obj.users.create(req_body)
        logger.info("gitlab创建用户,用户参数：{}".format(req_body))
    except Exception as e:
        logger.error("gitlab创建用户异常：{}".format(str(e)))
        return jsonify({"code": 500, "message": "failed", "data": "gitlab创建用户异常：{}".format(str(e))})
    return jsonify({"code": 200, "message": "success"})


# 这里可以不用delete, put 进行逻辑删除
@gitlab_bp.route("/user/<user_id>", methods=["PUT"])
def update_user_info(user_id):
    req_body = request.get_json()
    user_obj = gitlab_obj.users.get(user_id).__dict__['_attrs']
    is_can_block = True if user_obj['state'] == "active" else False
    # 这里可以放心，前端筛选出来的都是is_delete ==0 即没有被删除的
    if not is_can_block:
        return jsonify({"code": 400, "message": "is_block error, the {}'s state had block".format(user_obj['name'])})
    if 'is_block' in req_body.keys() and req_body['is_block'] == 1:
        user_obj.block()
        return jsonify({"code": 200, "message": "the {} had block successfully".format(user_obj['name'])})


@gitlab_bp.route("/user/<user_id>/reset_password", methods=["PUT"])
def update_user_password(user_id):
    req_body = request.get_json()
    user_obj = gitlab_obj.users.get(user_id).__dict__['_attrs']
    is_can_block = True if user_obj['state'] == "active" else False
    # 这里可以放心，前端筛选出来的都是is_delete ==0 即没有被删除的
    if not is_can_block:
        return jsonify({"code": 400, "message": "is_block error, the {}'s state had block".format(user_obj['name'])})
    if 'is_block' in req_body.keys() and req_body['is_block'] == 1:
        user_obj.block()
        return jsonify({"code": 200, "message": "the {} had block successfully".format(user_obj['name'])})
