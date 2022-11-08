# @Author  : kane.zhu
# @Time    : 2022/11/8 14:39
# @Software: PyCharm
# @Description:

from dao import db


class User(db.Model):
    __tablename__ = 'tbl_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(60))

