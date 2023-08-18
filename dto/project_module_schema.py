# @Author  : kane.zhu
# @Time    : 2023/8/18 11:43
# @Software: PyCharm
# @Description:项目工程之子模块部分
import json

from marshmallow import Schema, fields, ValidationError,validates_schema


class JSONField(fields.Str):
    def _deserialize(self, value, attr, data, **kwargs):
        if value is None:
            return None

        try:
            json.loads(value)
        except ValueError as e:
            raise ValidationError("Invalid JSON format") from e

        return value

class ModuleInfoSchema(Schema):
    id = fields.Integer()
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
    project_id = fields.Integer(required=True)
    module_status = fields.Boolean()
    project_cloud_platform = fields.Integer()
    description = fields.String()

    # 当开启dump后，必须输入dump文件的存储路径
    @validates_schema
    def validates_dump_oom_status(self, value, **kwargs):
        dump_oom_status_value = value.get('dump_oom_status')
        dump_oom_path_value = value.get('dump_oom_path')
        if dump_oom_status_value is True and not dump_oom_path_value:
            raise ValidationError("dump_oom_path is required when dump_oom_status is True.")

    # 当开启debug后，debug_status_port不能为空
    @validates_schema
    def validates_debug_status_port(self, value, **kwargs):
        debug_status_value = value.get('debug_status')
        debug_status_port_value = value.get('debug_status_port')
        if debug_status_value is True and not debug_status_port_value:
            raise ValidationError("debug_status_port is required when debug_status is True.")

