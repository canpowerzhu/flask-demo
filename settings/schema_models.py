# @Author  : kane.zhu
# @Time    : 2023/5/19 17:28
# @Software: PyCharm
# @Description:

import re
from typing import List, Optional

from pydantic import BaseModel, Field, validator

from log_settings import logger


# wifi管理请求参数控制
class WifiData(BaseModel):
    wifi_name: str = Field(..., description="WiFi名称")
    wifi_asset_type: str = Field(..., description="WiFi设备类型")
    wifi_asset_sn: str = Field(..., description="WiFi序列号")
    wifi_asset_mac: str = Field(..., description="WiFi MAC地址")
    wifi_manage_pass: str = Field(..., description="WiFi管理密码")
    wifi_connect_pass: str = Field(..., description="WiFi连接密码")


# 增加wifi信息的结构校验
class BulkWifiBody(BaseModel):
    wifi_list: List[WifiData] = Field(..., description="校验批量增加wifi的数据校验")


class SendWifiPass(BaseModel):
    wifi_name: str
    phone_number: Optional[str]

    @validator("phone_number")
    def phone_validation(cls, v):
        logger.debug(f"phone in 2 validator:{v}")
        regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
        if v and not re.search(regex, v, re.I):
            raise ValueError("Phone Number Invalid.")
        return v


# 流程工单的类目分类

class AddWorkFlowCategory(BaseModel):
    work_order_category_name: str = Field(..., description="父级目录的名称")
    work_order_second_category_name: str = Field(..., description="子级分类名称")
    description: Optional[str]



class CreateWorkOrder(BaseModel):
    urgent_level: int  # 紧急程度 0-问题咨询 1-报障
    work_order_category_id: int  # 绑定到哪个类目
    work_order_name:  str = Field(..., description="工单的名称标题")
    work_order_content:  str = Field(..., description="工单的内容")

class CreateWorkFlow(BaseModel):
    work_order_flow_name:  str # 工单流程的标题
    bind_category: int # 绑定到哪个类目
    step_one:  int # step_one
    step_two:  int # step_two
    step_three:  int # step_three
    step_four: Optional[int]
    step_five:  Optional[int]
    step_six:  Optional[int]


class CreateConfigItem(BaseModel):
    config_name: str
    config_key: str
    config_value: str
    config_group: Optional[str]
    description: Optional[str]

