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


class Domainaccount(db.Model):
    __tablename__ = "tbl_domain_account"
    id = db.Column(db.Integer, primary_key=True)
    register_website = db.Column(db.String(50), info="域名注册服务商")
    username = db.Column(db.String(50), info="域名账户")
    password = db.Column(db.String(50), info="域名账户密码")
    token_name = db.Column(db.String(100), default='', info="令牌名称")
    token = db.Column(db.String(100),default='', info="令牌")
    account_code = db.Column(db.String(50), info="域名账户码")
    account_status = db.Column(db.Boolean, info="域名账户是否有域名 1 表示账户下有域名, 0 则没有域名")
    remark = db.Column(db.String(100),info="备注")

class Domaininfo(db.Model):
    __tablename__ = "tbl_domain_info"
    id = db.Column(db.Integer, primary_key=True)
    register_website = db.Column(db.String(100))
    name_account = db.Column(db.String(100), info="所属账户")
    domain_name = db.Column(db.String(100), info="根域名")
    fqdn = db.Column(db.String(100), info="二级域名")
    type = db.Column(db.String(20), info="域名解析方式A、CNAME、TXT")
    answer = db.Column(db.String(500), info="解析的属性值")


class Domainlist(db.Model):
    __tablename__ = "tbl_domain"
    id = db.Column(db.Integer, primary_key=True)
    name_account = db.Column(db.String(100), info="所属账户")
    domain_name = db.Column(db.String(100), info="域名")
    locked =  db.Column(db.Boolean,info="是否锁定")
    autorenew_enabled =  db.Column(db.Boolean,info="是否自动续费")
    name_status = db.Column(db.String(50), info="域名是否有解析")
    expire_date = db.Column(db.DateTime, default=datetime.datetime.now, info="过期时间")
    create_date = db.Column(db.DateTime, onupdate=datetime.datetime.now, info="创建时间")




