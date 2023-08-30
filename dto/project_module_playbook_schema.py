# @Author  : kane.zhu
# @Time    : 2023/8/24 11:53
# @Software: PyCharm
# @Description:


from marshmallow import Schema, fields, ValidationError,validates_schema,validate


class ProjectModulePlaybookSchema(Schema):
    id = fields.Integer()
    project_name = fields.String()
    project_code = fields.String()
    module_name = fields.String()
    md5 = fields.String()
    content = fields.String()
    src_ip = fields.IPv4()
    # '配置类型 TEXT JSON XML YAML HTML Properties
    type = fields.Str(validate=validate.OneOf(["TEXT","JSON","XML","YAML","HTML","Properties"]))
    description = fields.String()


class ProjectModuleCombineSchema(Schema):
    id = fields.Integer()
    project_id = fields.Integer(required=True)
    module_name = fields.String(required=True)
    module_package_name = fields.String(required=True)
    module_rel_path = fields.String(required=True)
    module_env_pairs = fields.Dict()
    module_port_pairs = fields.Dict()
    module_host_pairs = fields.Dict()
    module_volumes_pairs = fields.Dict()
    dump_oom_status = fields.Boolean()
    dump_oom_path = fields.String()
    debug_status = fields.Boolean()
    debug_status_port = fields.Integer()
    start_define_params = fields.String()
    module_memory = fields.Integer()
    project_cloud_platform = fields.Integer()
    project_name = fields.String()
    project_code = fields.String()
    base_image_name = fields.String()
    health_check_interval = fields.Integer()
    health_check_retries = fields.Integer()
    health_check_timeout = fields.Integer()
    health_check_start_period = fields.Integer()
