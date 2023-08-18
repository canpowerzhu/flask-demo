# @Author  : kane.zhu
# @Time    : 2023/2/24 16:49
# @Software: PyCharm
# @Description:
from flask import request
from marshmallow import ValidationError, pprint
from werkzeug.security import generate_password_hash, check_password_hash


from dao.ops_db_users import db_ops_reg_user, db_ops_get_user
from dto.user_schema import UserSchema
from log_settings import logger


def user_reg(username, passwd, email, gtoken):
    """
    :param username: 注册用户名
    :param passwd: 注册用户原始密码
    :param email: 注册用户邮箱
    :param gtoken: 用户otp_secret_key
    :return: boolen
    """
    hashed_passwd = generate_password_hash(passwd)
    user_reg_data = {"username": username,
                     "email": email,
                     "password": hashed_passwd,
                     "is_mfa": True,
                     "otp_secret_key": gtoken
                     }
    try:
        UserSchema(many=True).load(user_reg_data)
    except ValidationError as err:
        logger.error("来自请求：{}, 校验字段异常: {}".format(request.trace_id, err.messages))
        pprint(err.messages)

    if not db_ops_reg_user(user_reg_data):
        return False


def login_user_verify(email, passwd):
    hashed_passwd, get_otp_secret_key = db_ops_get_user(email)
    if check_password_hash(hashed_passwd, passwd):
        return True, get_otp_secret_key
