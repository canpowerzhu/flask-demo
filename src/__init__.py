# @Author  : kane.zhu
# @Time    : 2022/11/7 21:23
# @Software: PyCharm
# @Description:


import uuid

from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required, decode_token

from dao import DatabaseConfig
from dao import db
from log_settings import logger
from settings.conf import PrdConfig
from src.aliyun_bp.v1.ali_domain import domain_ali_bp
from src.aliyun_bp.v1.ali_mail import mail_ali_bp
from src.aliyun_bp.v1.sts_main import sts_api_bp
from src.asset_bp.v1.wifi_bp import wifi_info_bp
from src.celery_bp.v1.celery_main import task_bp
from src.domain_bp.v1.name_domain import domain_name_bp
from src.gitlab_bp.v1.gitlab_funcs import gitlab_bp
from src.jenkins_bp.v1.jenkins_job import jenkins_ops_bp
from src.login_out_bp.v1.auth import login_out_bp
from src.ticket_bp.v1.ticket_ops import ticket_bp
from src.user_bp.v1.user_crud import user_crud_bp
from src.sys_config_bp.v1.sys_config_funcs import sysconfig_bp

from flask_marshmallow import Marshmallow


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(DatabaseConfig)
    # 设置jwt相关信息
    app.config['JWT_SECRET_KEY'] = PrdConfig.SALT
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = PrdConfig.JWT_ACCESS_TOKEN_EXPIRES
    jwt = JWTManager()
    jwt.init_app(app)

    # 增加marshmallow使用 序列化、反序列化 数据字段校验功能
    ma = Marshmallow()
    ma.init_app(app)
    @app.before_request
    def add_trace_id():
        trace_id = request.headers.get('X-Trace-Id')
        if not trace_id:
            trace_id = str(uuid.uuid4())
        request.trace_id = trace_id

    @app.before_request
    @jwt_required(optional=True)
    def before():
        url = request.path
        # 明确白名单接口地址， 首页、登陆以及注册无需验证
        # /v1/wifi/send_wifi_pass 这个参数先不做登陆限制
        pass_list = ['/', '/login', '/signup', '/v1/wifi/get_wifi_pass', '/favicon.ico']
        prefix = url.startswith(tuple(['/mfa', '/verify_mfa_code']))
        # 静态资源白名单
        static_whitelist = url.endswith(tuple(['.html', '.js']))

        # 这里不做静态资源的限制,因为前后端要分离
        if url not in pass_list and not prefix and not static_whitelist:
            auth_header = request.headers.get('Authorization')
            # 如果请求头中没有 Authorization 字段，拒绝访问
            if not auth_header:
                return jsonify({"code": 401, "message": "Full authentication is required to access this resource-1"})

            # 不在白名单 而且存在token
            if auth_header and auth_header.startswith('Bearer '):
                # "提取token 0-6 被Bearer和空格占用 取下标7以后的所有字符"
                token = auth_header[7:]
                logger.info("请求的token是{},解析的结果是{}".format(token, decode_token(token)))
            try:
                jwt_required()(None)  # 调用 @jwt_required 装饰器来进行令牌验证
            except Exception as e:
                # 处理令牌验证失败的情况
                return jsonify({"code": 401, "message": "Full authentication is required to access this resource-2"})

    @app.after_request
    def add_trace_id_to_logs(response):
        logger.info('Trace ID in Flask after_request: {trace_id}', trace_id=request.trace_id)
        return response

    if config is not None:
        if isinstance(config, dict):
            app.config.update(config)
        elif config.endswith('.py'):
            app.config.from_pyfile(config)
    setup_app(app)
    return app


def setup_app(app):
    # Create tables if they do not exist already
    @app.before_first_request
    def create_tables():
        db.create_all()

    db.init_app(app)
    app.register_blueprint(login_out_bp)
    app.register_blueprint(user_crud_bp, url_prefix="/v1/user")
    app.register_blueprint(domain_name_bp, url_prefix="/v1/domain")
    app.register_blueprint(sts_api_bp, url_prefix="/v1/ali_cloud/sts")
    app.register_blueprint(domain_ali_bp, url_prefix="/v1/ali_cloud/domain")
    app.register_blueprint(task_bp, url_prefix="/v1/celery_kane")
    app.register_blueprint(jenkins_ops_bp, url_prefix="/v1/jenkins")
    app.register_blueprint(mail_ali_bp, url_prefix="/v1/ali_cloud/mail")
    app.register_blueprint(gitlab_bp, url_prefix="/v1/gitlab")
    app.register_blueprint(wifi_info_bp, url_prefix="/v1/wifi")
    app.register_blueprint(ticket_bp, url_prefix="/v1/ticket")
    app.register_blueprint(sysconfig_bp, url_prefix="/v1/sysconfig")
