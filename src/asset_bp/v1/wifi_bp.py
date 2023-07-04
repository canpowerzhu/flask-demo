# @Author  : kane.zhu
# @Time    : 2023/5/19 17:22
# @Software: PyCharm
# @Description:


from flask import Blueprint, jsonify, request, render_template
from log_settings import logger
from service.ali_sms_wifi_service import wifi_info_crypt_service,get_wifi_pass_decrypt_service
from settings.schema_models import BulkWifiBody,SendWifiPass

wifi_info_bp = Blueprint('wifi_info_bp', __name__)


@wifi_info_bp.route("/add_wifi",methods=["POST"])
def add_wifi_info():
    request_data = request.json
    try:
        BulkWifiBody(wifi_list=request_data)
    except Exception as e:
        # 校验失败
        return jsonify({"error": str(e)}), 400

    if not wifi_info_crypt_service(request_data):
        return jsonify({"error": str("添加失败，请联系管理员"),"TraceId":request.trace_id}), 500
    return jsonify({"status": str("添加成功"), "TraceId": request.trace_id})

# @wifi_info_bp.route("/send_wifi_pass",methods=["POST"])
@wifi_info_bp.route("/get_wifi_pass",methods=["POST","GET"])
def get_wifi_password():
    if request.method == "POST":

        wifi_name = request.referrer.split("=")[1]
        phone_number = request.json["phone_number"]
        print("here",wifi_name,phone_number)
        #TODO 这里增加手机号码校验，是否在规则的手机号列表里面
        get_wifi_pass_decrypt_service(wifi_name,phone_number)
        logger.info("TraceID is {},手机号码{}获取{}的wifi的密码成功".format(request.trace_id,phone_number,wifi_name))
        return jsonify({"code":200,"message":"发送成功，请留意手机短信"})
    if request.method == 'GET':
        wifi_name = request.args.get("wifi_name")
        return render_template('get_wifi_pass.html', wifi_name=wifi_name)

