# @Author  : kane.zhu
# @Time    : 2023/4/6 21:48
# @Software: PyCharm
# @Description: 这里编写处理阿里云邮箱的服务相关
import json
from log_settings import logger
from settings.conf import PrdConfig

import requests


class AliMailDepartment(object):
    """
    调用API都是使用标准 HTTPS 协议，method=POST而且contentType=application/json
    add_department: 新增部门
    update_department： 更新部门，这里主要是部门的相关属性更新
    edit_departemnt： 编辑部门,这里主要是部门的下属账号变更
    delete_department： 删除部门，不在使用。内部会校验部门内是否有账号
    query_department： 罗列部门
    """

    def __init__(self, access_target, ali_mail_headers):
        self.access_target = access_target
        self.ali_mail_header = ali_mail_headers

    def add_department(self, department_name, custom_department_id):
        ali_mail_url = '{}/v0/ud/createDepartment'.format(PrdConfig.ALI_MAIL_URL)
        department_body = {"access":
                               {"accessTarget": self.access_target},
                           "param": {
                               # 这里的parentId 是写死的 ，因为初始创建已固定
                               "parentId": "-----Z-----6Y-N0Z:2:-----6anfhR",
                               "name": department_name,
                               "customDepartmentId": custom_department_id
                           },
                           "extend": {
                               "x-aliyun-department-orde": "1",
                               "x-aliyun-department-contact-share": "1"
                           }
                           }

        return self.__result_do_with(ali_mail_url, department_body)

    def update_department(self, department_id, parent_id, name):
        ali_mail_url = '{}/v0/ud/updateDepartment'.format(PrdConfig.ALI_MAIL_URL)
        department_body = {"access": {"accessTarget": self.access_target},
                           "param": {
                               "departmentId": department_id,
                               "parentId": parent_id,
                               "name": name
                           }
                           }
        return self.__result_do_with(ali_mail_url, department_body)

    def edit_departemnt(self, department_id, email_list):
        ali_mail_url = '{}/v0/ud/updateDepartment'.format(PrdConfig.ALI_MAIL_URL)
        department_body = {"access": {"accessTarget": self.access_target},
                           "param": {
                               "toDepartmentId": department_id,
                               "emails": email_list  # 这里传入的是一个list,list必不为空
                           }
                           }

        return self.__result_do_with(ali_mail_url, department_body)

    def delete_department(self, department_id):
        ali_mail_url = '{}/v0/ud/removeDepartment'.format(PrdConfig.ALI_MAIL_URL)
        department_body = {"access": {"accessTarget": self.access_target},
                           "param": {"departmentId": department_id}}

        return self.__result_do_with(ali_mail_url, department_body)

    def query_department(self):
        ali_mail_url = '{}/v0/ud/getDepartmentList'.format(PrdConfig.ALI_MAIL_URL)
        department_body = {"access": {"accessTarget": self.access_target}, "param": {}}

        return self.__result_do_with(ali_mail_url, department_body)

    def __result_do_with(self, ali_mail_url, department_body):
        res = requests.post(url=ali_mail_url, headers=self.ali_mail_header, data=json.dumps(department_body))
        logger.info("阿里云企业邮箱: 部门操作{}，参数{}".format(ali_mail_url, department_body))
        result_after_do_with = {"code": 200, "status": "success",
                                "data": json.loads(res.content)} if res.status_code == 200 else {"code": 500,
                                                                                                 "status": "Failed",
                                                                                                 "data": json.loads(
                                                                                                     res.content)}

        return result_after_do_with


class AliMailAccount(object):
    def __init__(self, access_target, ali_mail_headers):
        self.access_target = access_target
        self.ali_mail_header = ali_mail_headers

    def add_mail_account(self, account_list):
        # 这里account的对象是list, 可以实现批量创建，届时接口实现模版导入导出

        # {
        #     "name": accout_info['name'],
        #     "displayName": accout_info['display_name'],
        #     "activeStatus": accout_info['active_status'],
        #     "passwd": PrdConfig.ALI_MAIL_DEFAULT_PASSWD,
        #     "email": accout_info['email'],
        #     "employeeNo": accout_info['employee_no'],
        #     "departmentId": accout_info['department_id'],
        #     "initPasswdChanged": accout_info['init_passwd_changed'],
        #     "mobilePhone": accout_info['mobile_phone'],
        #     "nickName": accout_info['nick_name']
        # }

        ali_mail_url = '{}/v0/ud/createAccounts'.format(PrdConfig.ALI_MAIL_URL)
        mail_account_body = {"access": {"accessTarget": self.access_target},
                             "param": {"accounts": account_list}}

        return self.__result_do_account(ali_mail_url, mail_account_body)


    def __result_do_account(self, ali_mail_url, account_body):
        res = requests.post(url=ali_mail_url, headers=self.ali_mail_header, data=json.dumps(account_body))
        logger.info("阿里云企业邮箱: 账户操作{}，参数{}".format(ali_mail_url, account_body))
        result_after_do_with = {"code": 200, "status": "success",
                                "data": json.loads(res.content)} if res.status_code == 200 else {"code": 500,
                                                                                                 "status": "Failed",
                                                                                                 "data": json.loads(
                                                                                                     res.content)}

        return result_after_do_with