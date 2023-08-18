# @Author  : kane.zhu
# @Time    : 2023/8/18 11:38
# @Software: PyCharm
# @Description:

from marshmallow import Schema, fields

class UserSchema(Schema):
    username = fields.String(required=True)
    email = fields.Email()
    password = fields.String(required=True)