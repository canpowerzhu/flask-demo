# @Author  : kane.zhu
# @Time    : 2023/8/18 11:41
# @Software: PyCharm
# @Description:

from marshmallow import Schema, fields, ValidationError, post_load, validate
from utils.transfer_to_pinyin import words_transfer_to_letter


def is_all_upper(s):
    if not s.isupper():
        raise ValidationError("project_code only allows uppercase")


class ProjectInfoSchema(Schema):
    id = fields.Integer()
    project_name = fields.String(required=True, error_messages={"required": "project_name is required"})
    project_code = fields.String(validate=is_all_upper)
    project_repo = fields.URL(required=True,
                              error_messages={"required": "project_repo is required",
                                              "invalid": "Please enter the content in URL format"})
    base_image_name = fields.String(required=True)
    base_image_code = fields.Integer(dump_only=True, error_messages={"invalid": "Please params generate by System"})
    health_check_interval = fields.Integer(validate=validate.Range(min=10, max=60,
                                                                   error="health_check_interval the value range is  between 10 and 60, the unit is (s) "))
    health_check_retries = fields.Integer(
    validate = validate.Range(min=3, max=5, error="health_check_interval the value range is  between 3 and 5 "))
    health_check_start_period = fields.Integer(validate=validate.Range(min=60, max=120,
                                                                       error="health_check_interval the value range is  between 60 and 120,the unit is (s) "))
    project_ico = fields.String(required=True)
    description = fields.String()
    project_status = fields.Boolean()
    create_time = fields.DateTime(format='%Y-%m-%d %H:%M:%S')
    update_time = fields.DateTime(format='%Y-%m-%d %H:%M:%S')

    @post_load
    def calucate_version_code(self, item, **kwargs):
        print("转换数据{}".format(item))
        base_image_name = item['base_image_name']
        if base_image_name:
            version_parts = base_image_name.split('.')
            base_image_code = int(''.join(version_parts))
            item['base_image_code'] = base_image_code

        if 'project_code' not in item or item['project_code'] is None:
            project_name = item['project_name']
            item['project_code'] = words_transfer_to_letter(project_name)

        return item