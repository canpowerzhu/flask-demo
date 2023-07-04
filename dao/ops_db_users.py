# @Author  : kane.zhu
# @Time    : 2023/2/24 16:58
# @Software: PyCharm
# @Description:

from dao.models import User,db
from log_settings import logger
from sqlalchemy import or_

# 注册用户
def db_ops_reg_user(reg_user_info_dict):
    try:
        db.session.execute(User.__table__.insert(),[reg_user_info_dict])
        db.session.commit()
    except Exception as e:
        logger.error(e)
        return False

    return True


def db_ops_get_user(email):
    try:
        get_user_passwd,get_user_secret_key = db.session.query(User.password,User.otp_secret_key).filter(or_(User.email == email,User.username == email)).first()

    except Exception as e:
        logger.error(e)
        return False
    return get_user_passwd,get_user_secret_key

