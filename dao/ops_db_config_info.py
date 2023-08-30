# @Author  : kane.zhu
# @Time    : 2023/8/9 10:44
# @Software: PyCharm
# @Description: 针对配置表进行操作CRUD
import json

from dao.models import SysConfigInfo
from dao.models import db
from dto.sys_config_info_schema import SysConfigInfoSchema
from log_settings import logger

sys_config_info_schema = SysConfigInfoSchema()


def add_sys_config_info(sys_config_info: dict) -> bool:
    """
    : 增加配置项sql操作
    :param sys_config_info: 更新系统配置的数据字典
    :return:
    """
    try:
        db.session.execute(SysConfigInfo.__table__.insert(), [sys_config_info])
        db.session.commit()
    except Exception as e:
        logger.error(e)
        return False

    return True


def update_sys_config_info(update_data: dict) -> bool:
    """
   更新配置信息
   :param id: 更新的索引id
   :param update_data: 新的数据对象
   :return:
   """
    try:

        SysConfigInfo.query.filter(SysConfigInfo.id == id).update(update_data)
        db.session.commit()
        logger.info("更新配置项，请求体是{}".format(json.dumps(update_data)))
    except Exception as e:
        logger.error(e)
        return False, e
    return True, None


def get_sys_config_list(config_key=None, config_name=None, config_group=None) -> object:
    """
   获取系统配置，可以根据config_name,config_key,config_group进行单独或者联合查询 模糊查询
   config_name;
   config_key;
   config_group;
   :return
   """
    query = db.session.query(SysConfigInfo)

    if config_key:
        query = query.filter(SysConfigInfo.config_key.like(f'%{config_key}%'))

    if config_name:
        query = query.filter(SysConfigInfo.config_name.like(f'%{config_name}%'))

    if config_group:
        query = query.filter(SysConfigInfo.config_group.like(f'%{config_group}%'))

    try:

        result = query.all()
        # 借助marshmallow 格式化数据
        result_list_dict = sys_config_info_schema.dump(result, many=True)
        return True, result_list_dict

    except Exception as e:
        logger.error(e)
        return False, e





