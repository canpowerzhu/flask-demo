# @Author  : kane.zhu
# @Time    : 2023/4/6 16:29
# @Software: PyCharm
# @Description:
import json

from flask import Blueprint, jsonify, request

from service.ali_mail_service import AliMailDepartment, AliMailAccount
from settings.conf import PrdConfig
from utils import get_ali_mail_token
from utils.mail.manage_ali_mail import ali_mail_token

mail_ali_bp = Blueprint('mail_ali_bp', __name__)


@mail_ali_bp.route("/init_mail_ali_token", methods=["GET", "POST"])
def get_mail_ali_token():
    data = ali_mail_token()
    return jsonify({"code": 200, "status": "success", "data": data})


# Department crud
@mail_ali_bp.route("/mail_department/<target_domain>", methods=["GET", "POST", "DELETE", "PUT"])
def mail_department_ops(target_domain):
    # 初始阿里企业邮箱管理的基本参数
    ali_mail_token_header = {'Content-Type': 'application/json',
                             'Authorization': get_ali_mail_token()}
    department_obj = AliMailDepartment(target_domain, ali_mail_token_header)

    if request.method == "GET":
        res = department_obj.query_department()
        return jsonify(res)

    elif request.method == "POST":
        data = json.loads(request.data)
        res = department_obj.add_department(data['department_name'], data['custom_department_id'])
        return jsonify(res)

    elif request.method == "DELETE":
        data = json.loads(request.data)
        res = department_obj.delete_department(data['department_id'])
        return jsonify(res)


    elif request.method == "PUT":
        data = json.loads(request.data)
        res = department_obj.update_department(data['department_id'], data['parent_id'], data['department_name'])
        return jsonify(res)

    else:
        return "禁止使用GET、POST、DELETE、PUT以外的请求方式"


# Account crud
@mail_ali_bp.route("/mail_account/<target_domain>", methods=["GET", "POST", "DELETE", "PUT"])
def mail_account_ops(target_domain):
    # 初始阿里企业邮箱管理的基本参数
    ali_mail_token_header = {'Content-Type': 'application/json',
                             'Authorization': get_ali_mail_token()}
    account_obj = AliMailAccount(target_domain, ali_mail_token_header)
    if request.method == "GET":
        pass

    elif request.method == "POST":
        data = json.loads(request.data)
        required_params = {'name', 'email', 'mobilePhone', 'departmentId'}
        for account_item in data['account_list']:
            is_miss_params = True if required_params & set(account_item.keys()) == required_params else False
            if not is_miss_params:
                return jsonify({"code": 400, "messsage": "misss reuqired params"})
            account_item['passwd'] = PrdConfig.ALI_MAIL_DEFAULT_PASSWD

        res = account_obj.add_mail_account(data['account_list'])
        return jsonify(res)

    elif request.method == "DELETE":
        pass


    elif request.method == "PUT":
        pass

    else:
        return "禁止使用GET、POST、DELETE、PUT以外的请求方式"
