# @Author  : kane.zhu
# @Time    : 2023/3/20 17:12
# @Software: PyCharm
# @Description:
from dao import db
from  log_settings import logger
from dao.models import Domainaccount, Domainlist, Domaininfo
from flask_sqlalchemy import query

def get_domain_name_user_token():
    try:
        response = db.session.query(Domainaccount.username, Domainaccount.token).filter(
            Domainaccount.account_status == '1',Domainaccount.register_website == "www.name.com").all()

    except Exception as e:
        logger.error(e)
        return False,str(e)

    return True, response

#批量插入一级域名的信息
def db_ops_root_domain_bulk(bulk_insert_root_domain_info_dict:list):
    try:
        db.session.execute(Domainlist.__table__.insert(),bulk_insert_root_domain_info_dict)
        db.session.commit()
    except Exception as e:
        logger.error(e)
        return False, e

    return True


# 根据用户获取token
def db_ops_get_token(user):
    try:
        name_user_token = Domainaccount.query.filter_by(username=user).first()
    except Exception as e:
        logger.error(e)
        return False,e
    return True,name_user_token


def db_ops_get_root_domain(user):
    try:
        name_user_root_domain = Domainlist.query.filter_by(name_account=user).all()
    except Exception as e:
        logger.error(e)
        return False,e
    return True,name_user_root_domain


#批量插入子域名的信息
def db_ops_sub_domain_bulk(app,bulk_insert_sub_domain_info,root_domain,count):
    with app.app_context():
        try:
            if len(bulk_insert_sub_domain_info) != 0:
                db.session.execute(Domaininfo.__table__.insert(),bulk_insert_sub_domain_info)
                Domainlist.query.filter_by(domain_name=root_domain).update({"name_status": count})
                db.session.commit()
            else:
                Domainlist.query.filter_by(domain_name=root_domain).update({"name_status": count})
                db.session.commit()
        except Exception as e:
            logger.error(e)
            return False

        return True



