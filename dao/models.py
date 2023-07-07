# @Author  : kane.zhu
# @Time    : 2022/11/8 14:39
# @Software: PyCharm
# @Description:

from flask_login import UserMixin
import datetime

from sqlalchemy import UniqueConstraint

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
    is_mfa = db.Column(db.Boolean)
    otp_secret_key = db.Column(db.String(120), info="mfa信息")
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
    token = db.Column(db.String(100), default='', info="令牌")
    account_code = db.Column(db.String(50), info="域名账户码")
    account_status = db.Column(db.Boolean, info="域名账户是否有域名 1 表示账户下有域名, 0 则没有域名")
    remark = db.Column(db.String(100), info="备注")


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
    locked = db.Column(db.Boolean, info="是否锁定")
    autorenew_enabled = db.Column(db.Boolean, info="是否自动续费")
    name_status = db.Column(db.String(50), info="域名是否有解析")
    expire_date = db.Column(db.DateTime, default=datetime.datetime.now, info="过期时间")
    create_date = db.Column(db.DateTime, onupdate=datetime.datetime.now, info="创建时间")


class WifiInfo(db.Model):
    __tablename__ = "tbl_wifi_info"
    id = db.Column(db.Integer, primary_key=True)
    wifi_name = db.Column(db.String(100), info="wifi名称", unique=True)
    wifi_status = db.Column(db.Boolean, info="wifi状态", default=True)
    wifi_asset_status = db.Column(db.Boolean, info="wifi设备状态", default=True)
    wifi_asset_type = db.Column(db.String(100), info="wifi设备型号")
    wifi_asset_sn = db.Column(db.String(100), info="设备序列号")
    wifi_asset_mac = db.Column(db.String(100), info="设备Mac地址")
    wifi_manage_pass = db.Column(db.String(200), info="wifi管理员密码")
    wifi_connect_pass = db.Column(db.String(200), info="wifi连接密码")
    create_by = db.Column(db.String(50), info="创建者", default="admin")
    create_date = db.Column(db.DateTime, default=datetime.datetime.now, info="创建时间")
    update_date = db.Column(db.DateTime, onupdate=datetime.datetime.now, info="更新时间")


## 工单模块

# 工单
class WorkOrder(db.Model):
    __tablename__ = "tbl_work_order"
    id = db.Column(db.Integer, primary_key=True)
    work_order_name = db.Column(db.String(100), info="工单名称", unique=True)
    work_order_content = db.Column(db.Text,nullable=True) #工单内容
    transfer_max_count = db.Column(db.Integer, info="工单允许转派的最大次数", default=3)
    transfer_type = db.Column(db.Integer, info="转派类型 0-内部转派 1-外部转派", nullable=True, default=None)
    transfer_by = db.Column(db.String(50), info="转派发起人", default="admin")
    is_aborted = db.Column(db.Boolean, info="是否终止", default=False)
    create_by = db.Column(db.String(50), info="创建者", default="admin")
    create_date = db.Column(db.DateTime, default=datetime.datetime.now, info="创建时间")
    update_date = db.Column(db.DateTime, onupdate=datetime.datetime.now, info="更新时间")


# 工单附件详情表
class WorkOderAttachInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    work_order_name_id = db.Column(db.Integer, info="附件资源所属的工单ID")
    attach_url = db.Column(db.String(50), info="转派发起人", default="admin")
    # 这里设置附件的访问链接有效期，工单完成后的30天失效 资源进入冷冻期 使用STS模式进行访问控制
    create_by = db.Column(db.String(50), info="创建者", default="admin")
    create_date = db.Column(db.DateTime, default=datetime.datetime.now, info="创建时间")
    update_date = db.Column(db.DateTime, onupdate=datetime.datetime.now, info="更新时间")


# 工单分类
class WorkOrderCategory(db.Model):
    __tablename__ = "tbl_work_order_category"
    id = db.Column(db.Integer, primary_key=True)
    work_order_category_name = db.Column(db.String(100), info="工单分类名称")
    work_order_second_category_name = db.Column(db.String(100), info="二级工单分类名称")
    create_by = db.Column(db.String(50), info="创建者", default="admin")
    create_date = db.Column(db.DateTime, default=datetime.datetime.now, info="创建时间")
    update_date = db.Column(db.DateTime, onupdate=datetime.datetime.now, info="更新时间")

    __table_args__ = (
        # 主分类和二级分类联合唯一
        UniqueConstraint('work_order_category_name', 'work_order_second_category_name', name='uix_category'),  # 联合唯一
        # Index('ix_id_name', 'name', 'email'), #索引
    )


# 工单流程
class WorkOrderFlow(db.Model):
    __tablename__ = "tbl_work_order_flow"
    id = db.Column(db.Integer, primary_key=True)
    work_order_flow_name = db.Column(db.String(100), info="工单流程名称", unique=True)
    bind_category = db.Column(db.Integer, info="绑定分类")## 这里创建的时候必须绑定到哪个分类
    step_one = db.Column(db.Integer, info="预设字段1")  ## 选择对应的人员ID
    step_two = db.Column(db.Integer, info="预设字段2")  ## 选择对应的人员ID
    step_three = db.Column(db.Integer, info="预设字段3")  ## 选择对应的人员ID
    step_four = db.Column(db.Integer, info="预设字段4")  ## 选择对应的人员ID
    step_five = db.Column(db.Integer, info="预设字段5")  ## 选择对应的人员ID
    step_six = db.Column(db.Integer, info="预设字段6")  ## 选择对应的人员ID
    create_by = db.Column(db.String(50), info="创建者", default="admin")
    create_date = db.Column(db.DateTime, default=datetime.datetime.now, info="创建时间")
    update_date = db.Column(db.DateTime, onupdate=datetime.datetime.now, info="更新时间")
