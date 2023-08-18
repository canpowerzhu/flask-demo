# @Author  : kane.zhu
# @Time    : 2023/8/18 11:43
# @Software: PyCharm
# @Description:项目工程之子模块部分
import json

from marshmallow import Schema, fields, ValidationError,validates


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

    # 当开启dump后，必须输入dump文件的存储路径
    @validates('dump_oom_status')
    def validates_dump_oom_path(self, key, dump_oom_status):
        if dump_oom_status and not self.dump_oom_path:
            raise ValueError("validates_dump_oom_path field cannot be empty when dump_oom_status is True.")

        return dump_oom_status

    # 当开启debug后，debug_status_port不能为空
    @validates('debug_status')
    def validates_debug_status_port(self, key, debug_status):
        if debug_status and not self.debug_status_port:
            raise ValueError("debug_status_port field cannot be empty when debug_status is True.")

        return debug_status
