# @Author  : kane.zhu
# @Time    : 2023/3/21 19:33
# @Software: PyCharm
# @Description:
from flask import Blueprint, jsonify

from utils.domain.domain_ali import ali_cloud_domain_sync, direct_async_ali_cloud_record

domain_ali_bp = Blueprint('domain_ali_bp', __name__)


@domain_ali_bp.route("/sync_root_domain", methods=["GET", "POST"])
def domain_root_sync():
    ali_cloud_domain_sync()

    return jsonify({"code": 200, "status": "success", "data": "data"})


@domain_ali_bp.route("/sync_domain_record", methods=["GET", "POST"])
def domain_record_sync():
    direct_async_ali_cloud_record()

    return jsonify({"code": 200, "status": "success", "data": "data"})
