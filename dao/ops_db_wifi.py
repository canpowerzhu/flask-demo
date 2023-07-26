# @Author  : kane.zhu
# @Time    : 2023/2/24 16:58
# @Software: PyCharm
# @Description:

from dao.models import WifiInfo, db
from log_settings import logger


# 批量设备插入信息
def db_ops_bulk_create(bulk_wifi_info_dict: list):
    try:
        db.session.execute(WifiInfo.__table__.insert(), bulk_wifi_info_dict)
        db.session.commit()
    except Exception as e:
        logger.error(e)
        return False

    return True


def db_ops_get_password(wifi_name):
    try:
        wifi_encrypt_pass = db.session.query(WifiInfo.wifi_connect_pass).filter(
            WifiInfo.wifi_name == wifi_name).scalar()
    except Exception as e:
        logger.error(e)
        return False
    return wifi_encrypt_pass
