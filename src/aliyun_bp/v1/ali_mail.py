# @Author  : kane.zhu
# @Time    : 2023/4/6 16:29
# @Software: PyCharm
# @Description:
import json

from flask import Blueprint, jsonify
from utils.mail.manage_ali_mail import ali_mail_token


mail_ali_bp = Blueprint('mail_ali_bp', __name__)

@mail_ali_bp.route("/init_mail_ali_token",methods=["GET","POST"])
def get_mail_ali_token():
    data= ali_mail_token()
    return  jsonify({"code":200,"status":"success","data":data})

# Department crud
# Account crud