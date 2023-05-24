# @Author  : kane.zhu
# @Time    : 2023/5/19 17:04
# @Software: PyCharm
# @Description:
import json
import sys
from log_settings import logger
from flask import request
from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient

from utils.aliyun_cloud import config


class AliSms(object):
    def __init__(self):
        pass

    @staticmethod
    def create_client() -> Dysmsapi20170525Client:
        config.endpoint = f'dysmsapi.aliyuncs.com'
        return Dysmsapi20170525Client(config)

    @staticmethod
    def SendPassWord(
        ReceiveNumber:str,PassWord: str,
    ) -> None:
        # 工程代码泄露可能会导致AccessKey泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html
        client = AliSms.create_client()
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            phone_numbers=ReceiveNumber,
            sign_name='傲途跨境',
            template_code='SMS_146802154',
            template_param=json.dumps({'code':PassWord})
        )
        logger.info("TraceID: {},发送的内容是{}，接受人是{}".format(request.trace_id,PassWord,str(ReceiveNumber)))
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            res = client.send_sms_with_options(send_sms_request, runtime)
            print(res.body,res.status_code)
        except Exception as error:
            # 如有需要，请打印 error
            UtilClient.assert_as_string(error.message)


