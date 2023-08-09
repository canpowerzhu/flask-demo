# @Author  : kane.zhu
# @Time    : 2022/11/8 14:39
# @Software: PyCharm
# @Description:

import datetime
import ipaddress

from marshmallow import Schema,fields,validate

from flask_login import UserMixin
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import validates
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
    expire_time = db.Column(db.DateTime, default=datetime.datetime.now, info="过期时间")
    create_time = db.Column(db.DateTime, onupdate=datetime.datetime.now, info="创建时间")


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
    create_time = db.Column(db.DateTime, default=datetime.datetime.now, info="创建时间")
    update_time = db.Column(db.DateTime, onupdate=datetime.datetime.now, info="更新时间")


## 工单模块

# 工单
class WorkOrder(db.Model):
    __tablename__ = "tbl_work_order"
    id = db.Column(db.Integer, primary_key=True)
    urgent_level = db.Column(db.Integer, info="紧急程度 1-问题咨询, 2-保障")
    # 工单使用属于哪个分类 取决tbl_work_order_category这个表
    work_order_category_id = db.Column(db.Integer, info="选择工单类别的ID")
    work_order_name = db.Column(db.String(100), info="工单名称", unique=True)
    work_order_content = db.Column(db.Text, nullable=True)  # 工单内容
    transfer_max_count = db.Column(db.Integer, info="工单允许转派的最大次数", default=3) #大于3后 无法转派
    transfer_type = db.Column(db.Integer, info="转派类型 0-内部转派 1-外部转派", nullable=True, default=None)
    transfer_by = db.Column(db.String(50), info="转派发起人", default="admin")
    is_aborted = db.Column(db.Boolean, info="是否终止", default=False)
    create_by = db.Column(db.String(50), info="创建者", default="admin")
    create_time = db.Column(db.DateTime, default=datetime.datetime.now, info="创建时间")
    update_time = db.Column(db.DateTime, onupdate=datetime.datetime.now, info="更新时间")


# 工单附件详情表
class WorkOderAttachInfo(db.Model):
    __tablename__ = "tbl_work_order_attchment_info"
    id = db.Column(db.Integer, primary_key=True)
    work_order_name_id = db.Column(db.Integer, info="附件资源所属的工单ID")
    attach_url = db.Column(db.String(50), info="附件地址")
    # 这里设置附件的访问链接有效期，工单完成后的30天失效 资源进入冷冻期 使用STS模式进行访问控制
    create_by = db.Column(db.String(50), info="创建者", default="admin")
    create_time = db.Column(db.DateTime, default=datetime.datetime.now, info="创建时间")
    update_time = db.Column(db.DateTime, onupdate=datetime.datetime.now, info="更新时间")




# 工单分类
class WorkOrderCategory(db.Model):
    __tablename__ = "tbl_work_order_category"
    id = db.Column(db.Integer, primary_key=True)
    work_order_category_name = db.Column(db.String(100), info="工单分类名称", default="默认")
    work_order_second_category_name = db.Column(db.String(100), info="二级工单分类名称")
    description = db.Column(db.String(500), info="备注描述")
    # 由之前的status和deleted合并为blocked字段，禁用至灰色。无删除后唯一索引问题
    blocked = db.Column(db.Boolean, info="工单分类开启选项", default=False)
    create_by = db.Column(db.String(50), info="创建者", default="admin")
    create_time = db.Column(db.DateTime, default=datetime.datetime.now, info="创建时间")
    update_time = db.Column(db.DateTime, onupdate=datetime.datetime.now, info="更新时间")

    __table_args__ = (
        # 主分类和二级分类联合唯一
        UniqueConstraint('work_order_category_name', 'work_order_second_category_name', name='uix_category'),  # 联合唯一
        # Index('ix_id_name', 'name', 'email'), #索引
    )


# 工单流程 创建工单是否要绑定流程
class WorkOrderFlow(db.Model):
    __tablename__ = "tbl_work_order_flow"
    id = db.Column(db.Integer, primary_key=True)
    work_order_flow_name = db.Column(db.String(100), info="工单流程名称", unique=True)
    # 工单流程绑定到 取决tbl_work_order_category这个表 。如此依赖就和创建工单的流程对应起来
    bind_category = db.Column(db.Integer, info="绑定分类")
    step_one = db.Column(db.Integer, info="预设字段1",nullable=True)  ## 选择对应的人员ID
    step_two = db.Column(db.Integer, info="预设字段2",nullable=True)  ## 选择对应的人员ID
    step_three = db.Column(db.Integer, info="预设字段3",nullable=True)  ## 选择对应的人员ID
    step_four = db.Column(db.Integer, info="预设字段4",nullable=True)  ## 选择对应的人员ID
    step_five = db.Column(db.Integer, info="预设字段5",nullable=True)  ## 选择对应的人员ID
    step_six = db.Column(db.Integer, info="预设字段6",nullable=True)  ## 选择对应的人员ID
    status = db.Column(db.Boolean, info="工单流程状态标识", default=False)
    deleted = db.Column(db.Boolean, info="工单流程逻辑删除标识", default=False)
    create_by = db.Column(db.String(50), info="创建者", default="admin")
    create_time = db.Column(db.DateTime, default=datetime.datetime.now, info="创建时间")
    update_time = db.Column(db.DateTime, onupdate=datetime.datetime.now, info="更新时间")


### 系统管理模块
#### 配置信息表
class SysConfigInfo(db.Model):
    __tablename__ = "tbl_sys_config_info"
    id = db.Column(db.Integer, primary_key=True)
    config_name = db.Column(db.String(50), info="配置名称", nullable=True)
    config_key = db.Column(db.String(50), info="配置键", nullable=True)
    config_value = db.Column(db.String(50), info="配置值", nullable=True)
    config_group = db.Column(db.String(10), info="分类", nullable=True)
    description = db.Column(db.String(50), info="备注", nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now, info="创建时间")
    update_time = db.Column(db.DateTime, onupdate=datetime.datetime.now, info="更新时间")

class SysConfigInfoSchema(Schema):
    """
    配置信息表  tbl_sys_config_info 序列化与反序列化 校验等的schema
    """
    config_name = fields.String()
    config_key = fields.String()
    config_value = fields.String()
    config_group = fields.String()
    description = fields.String()
    create_time = fields.DateTime(format='%Y-%m-%d %H:%M:%S')
    update_time = fields.DateTime(format='%Y-%m-%d %H:%M:%S')



### 发布模块
class ProjectInfo(db.Model):
    __tablename__ = "tbl_project_info"
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(50), info="项目名称")
    project_code = db.Column(db.String(10), info="项目名称代码")
    base_image_name = db.Column(db.String(50), info="/base/apline-base-arthas-jdk8:3.1.2")
    health_check_interval = db.Column(db.Integer, info="两次健康检查间隔，默认30s",default=30)
    health_check_timeout = db.Column(db.Integer, info="健康检查超过这个时间，则失败，默认30s",default=30)
    health_check_retries = db.Column(db.Integer, info="连续检查失败次数超过，则失败，默认3",default=3)
    health_check_start_period = db.Column(db.Integer, info="应用初始化时间，启动过程 健康检查不计入，默认30s",default=30)
    project_ico= db.Column(db.String(10), info="项目icon地址，来自oss地址")
    description = db.Column(db.String(50), info="备注", nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now, info="创建时间")
    update_time = db.Column(db.DateTime, onupdate=datetime.datetime.now, info="更新时间")

class ModuleInfo(db.Model):
    __tablename__ = "tbl_module_info"
    id = db.Column(db.Integer, primary_key=True)
    module_name = db.Column(db.String(50), info="模块名称")
    module_package_name = db.Column(db.String(50), info="模块包名称")
    module_rel_path = db.Column(db.String(50), info="模块包的相对路径")
    module_env_pairs = db.Column(db.Text) #环境变量---json字符串{"TZ":"Asia/Shanghai","GOOGLE_API_KEY":"123456key"}
    module_port_pairs = db.Column(db.Text) #端口协议---json字符串{5000:"tcp",5001:"udp",5002:"tcp"}
    module_host_pairs = db.Column(db.Text) #主机解析---json字符串{"moppo-xxl": "192.168.9.227","scrm-bus-es":"192.168.3.4"}
    ## 目录挂载解析---json字符串
    # {"/data/logs/{module_name}/logs": "/mnt/logs",
    # "/data/app/{module_name}/{module_package_name}":"/mnt/scrm-bus-server.jar"
    # }
    module_volumes_pairs = db.Column(db.Text)
    # 当dump_oom_status为True, 启动参数增加 -XX:+HeapDumpOnOutOfMemoryError
    dump_oom_status = db.Column(db.Boolean, info="发生OOM时，是否dump", default=False)
    # 设置后 启动参数增加  -XX:HeapDumpPath=/tmp/dump.hprof
    dump_oom_path = db.Column(db.String(50), info="dump文件存储位置", default='/tmp/dump.hprof')

    # debug_status, 启动参数增加 -agentlib:jdwp=transport=dt_socket,address={{ debug_status_port }},server=y,suspend=n
    debug_status = db.Column(db.Boolean, info="是否开启debug启动模式", default=False)
    # debug开启后，debug_status_port 这个值不能为空
    debug_status_port = db.Column(db.String(5), info="开启debug时的端口")
    # 启动的自定义参数 存储json类型
    #{"file.encoding":"UTF-8","spring.profiles.active":"prod"}  拼接成"-Dfile.encoding=UTF-8”
    start_define_params = db.Column(db.Text)
    module_memory = db.Column(db.Integer, info="模块启动时的堆栈内存，Xmx Xms")



    project_id = db.Column(db.Integer, info="模块归属项目ID")
    #
    project_cloud_platform = db.Column(db.Integer, info="部署的平云台，意味着走哪个代理")
    description = db.Column(db.String(50), info="备注", nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now, info="创建时间")
    update_time = db.Column(db.DateTime, onupdate=datetime.datetime.now, info="更新时间")

    # 当开启dump后，必须输入dump文件的存储路径
    @validates('dump_oom_status')
    def validates_dump_oom_path(self,key,dump_oom_status):
        if dump_oom_status and not self.dump_oom_path:
            raise  ValueError("validates_dump_oom_path field cannot be empty when dump_oom_status is True.")

        return dump_oom_status


    # 当开启debug后，debug_status_port不能为空
    @validates('debug_status')
    def validates_debug_status_port(self, key, debug_status):
        if debug_status and not self.debug_status_port:
            raise ValueError("debug_status_port field cannot be empty when debug_status is True.")

        return debug_status


class CloudPlatformInfo(db.Model):
    __tablename__ = "tbl_cloud_platform_info"
    id = db.Column(db.Integer, primary_key=True)
    cloud_platform_name = db.Column(db.String(20), info="公云平台名称")
    # 这里的值应该是配置信息里面
    cloud_platform_code = db.Column(db.String(20), info="公云平台名称代码 AliCloud、HuaWeiCloud、AwsCloud")

    cloud_platform_proxy_active = db.Column(db.Boolean, info="云平台代理是否激活", default=False)
    cloud_platform_proxy_host = db.Column(db.String(10), info="代理主机地址")
    cloud_platform_proxy_port = db.Column(db.String(5), info="代理主机端口")
    cloud_platform_proxy_username = db.Column(db.String(10), info="代理主机登陆用户名")
    # 密码和密钥可以同时存在
    cloud_platform_proxy_password = db.Column(db.String(10), info="代理主机SSH密码")
    cloud_platform_proxy_ksa_key = db.Column(db.String(1000), info="代理主机SSH密钥")
    description = db.Column(db.String(50), info="备注", nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now, info="创建时间")
    update_time = db.Column(db.DateTime, onupdate=datetime.datetime.now, info="更新时间")

    @validates('cloud_platform_proxy_host')
    def validate_cloud_platform_proxy_host(self, key, cloud_platform_proxy_host):
        try:
            # Try to create an IP address object from the input
           ipaddress.ip_address(cloud_platform_proxy_host)
        except ValueError:
            # If the input is not a valid IP address, raise a ValueError
            raise ValueError(f"{key} field must be a valid IPv4 or IPv6 address.")
        return cloud_platform_proxy_host