# @Author  : kane.zhu
# @Time    : 2023/5/19 17:28
# @Software: PyCharm
# @Description:

from pydantic import BaseModel,Field, validator
from typing import List,Optional
from log_settings import logger
import re



class WifiData(BaseModel):
    wifi_name: str = Field(..., description="WiFi名称")
    wifi_asset_type: str = Field(..., description="WiFi设备类型")
    wifi_asset_sn: str = Field(..., description="WiFi序列号")
    wifi_asset_mac: str = Field(..., description="WiFi MAC地址")
    wifi_manage_pass: str = Field(..., description="WiFi管理密码")
    wifi_connect_pass: str = Field(..., description="WiFi连接密码")

# 增加wifi信息的结构校验
class BulkWifiBody(BaseModel):
    wifi_list: List[WifiData] = Field(...,description="校验批量增加wifi的数据校验")


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

