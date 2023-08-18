# @Author  : kane.zhu
# @Time    : 2023/8/18 11:39
# @Software: PyCharm
# @Description:

from marshmallow import Schema, fields

class SysConfigInfoSchema(Schema):
    """
    配置信  tbl_sys_config_info 序列化与反序列化 校验等的schema
    """
    config_name = fields.String()
    config_key = fields.String()
    config_value = fields.String()
    config_group = fields.String()
    description = fields.String()
    create_time = fields.DateTime(format='%Y-%m-%d %H:%M:%S')
    update_time = fields.DateTime(format='%Y-%m-%d %H:%M:%S')
