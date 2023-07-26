# @Author  : kane.zhu
# @Time    : 2023/3/20 16:31
# @Software: PyCharm
# @Description:


from flask import Blueprint, jsonify

from utils.domain.domain_name import sync_name_root_domain, sync_sub_domain_info

domain_name_bp = Blueprint('domain_name_bp', __name__)


@domain_name_bp.route("/sync_root_domain", methods=["GET", "POST"])
def domain_root_sync():
    data = sync_name_root_domain() if sync_name_root_domain() is not None else None
    print(data, type(data))
    return jsonify({"code": 200, "status": "success", "data": data})


@domain_name_bp.route("/sync_domain_records/<account_username>", methods=["GET", "POST"])
def domain_record_sync(account_username):
    data = sync_sub_domain_info(account_username) if sync_sub_domain_info(account_username) is not None else None
    return jsonify({"code": 200, "status": "success", "data": data})
