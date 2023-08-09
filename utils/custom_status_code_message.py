# @Author  : kane.zhu
# @Time    : 2023/8/9 14:12
# @Software: PyCharm
# @Description:
from flask import jsonify


class CustomStatusCode:
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500
    NO_DATA = 1400


status_message = {
    CustomStatusCode.OK: 'OK',
    CustomStatusCode.CREATED: 'Created Successfully',
    CustomStatusCode.BAD_REQUEST: 'Bad Request,please check it',
    CustomStatusCode.NOT_FOUND: 'Not Found',
    CustomStatusCode.INTERNAL_SERVER_ERROR: 'Server Internal Error,please contact administrator'
}


def generate_response(status_code,data=None,message=None):
    response = {
        'status': status_code,
        'message': message if message else status_message.get(status_code,''),
        'data': data
    }
    return  jsonify(response),status_code