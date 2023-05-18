# @Author  : kane.zhu
# @Time    : 2022/11/7 21:23
# @Software: PyCharm
# @Description:


from flask import g, Flask,request,jsonify
from log_settings import logger
import uuid
from dao import DatabaseConfig
from src.aliyun_bp.v1.ali_mail import mail_ali_bp

from src.user_bp.v1.user_crud import user_crud_bp
from src.aliyun_bp.v1.sts_main import sts_api_bp
from src.celery_bp.v1.celery_main import task_bp
from src.login_out_bp.v1.auth import login_out_bp
from src.domain_bp.v1.name_domain import domain_name_bp
from src.aliyun_bp.v1.ali_domain import domain_ali_bp
from src.jenkins_bp.v1.jenkins_job import jenkins_ops_bp
from src.gitlab_bp.v1.gitlab_funcs import gitlab_bp
from dao import db
from settings.conf import PrdConfig
import jwt
from jwt import exceptions





def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(DatabaseConfig)

    @app.before_request
    def add_trace_id():
        trace_id = request.headers.get('X-Trace-Id')
        if not trace_id:
            trace_id = str(uuid.uuid4())
        request.trace_id = trace_id

    @app.before_request
    def before():
        url = request.path
        # 明确白名单接口地址， 首页、登陆以及注册无需验证
        pass_list = ['/','/login','/signup']
        # 这里不做静态资源的限制
        if url in pass_list:
            pass
        else:
            return jsonify({"code":401,"message":"Full authentication is required to access this resource"})

    @app.before_request
    def jwt_authentication():
        """
        1.获取请求头Authorization中的token
        2.判断是否以 Bearer开头
        3.使用jwt模块进行校验
        4.判断校验结果,成功就提取token中的载荷信息,赋值给g对象保存
        """
        auth = request.headers.get('Authorization')
        if auth and auth.startswith('Bearer '):
            "提取token 0-6 被Bearer和空格占用 取下标7以后的所有字符"
            token = auth[7:]
            "校验token"
            g.username = None
            try:
                "判断token的校验结果"
                payload = jwt.decode(token, PrdConfig.SALT, algorithms=['HS256'])
                "获取载荷中的信息赋值给g对象"
                g.username = payload.get('username')
            except exceptions.ExpiredSignatureError:  # 'token已失效'
                g.username = 1
            except jwt.DecodeError:  # 'token认证失败'
                g.username = 2
            except jwt.InvalidTokenError:  # '非法的token'
                g.username = 3

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
    app.register_blueprint(user_crud_bp,url_prefix="/v1/user")
    app.register_blueprint(domain_name_bp,url_prefix="/v1/domain")
    app.register_blueprint(sts_api_bp,url_prefix="/v1/ali_cloud/sts")
    app.register_blueprint(domain_ali_bp,url_prefix="/v1/ali_cloud/domain")
    app.register_blueprint(task_bp,url_prefix="/v1/celery_kane")
    app.register_blueprint(jenkins_ops_bp,url_prefix="/v1/jenkins")
    app.register_blueprint(mail_ali_bp,url_prefix="/v1/ali_cloud/mail")
    app.register_blueprint(gitlab_bp,url_prefix="/v1/gitlab")