# @Author  : kane.zhu
# @Time    : 2022/11/8 14:39
# @Software: PyCharm
# @Description:

from flask_login import UserMixin
import datetime

from dao import db

"""
如果你将模型类定义在单独的模块中，那么必须在调用db.create_all()之前导入相应的模块，
以便让SQLAlchemy获取模型类被创建时生成的表信息
创建类 需继承UserMixin, 有用户属性

* is_authenticated: 是否被验证
* is_active: 是否被激活
* is_anonymous: 是否是匿名用户
* get_id(): 获得用户id,并转换成unicode类型
"""


class User(db.Model, UserMixin):
    __tablename__ = "tbl_users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(60))
    password = db.Column(db.String(300))
    is_mfa = db.Column(db.Boolean, unique=True)
    otp_secret_key = db.Column(db.String(120),info="mfa信息")
    is_disabled = db.Column(db.Boolean, info="用户状态,是否禁用")
    create_time = db.Column(db.DateTime, default=datetime.datetime.now, info="创建时间")
    update_time = db.Column(db.DateTime, onupdate=datetime.datetime.now, info="更新时间")

    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict

    db.to_dict = to_dict

