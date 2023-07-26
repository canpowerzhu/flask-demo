# @Author  : kane.zhu
# @Time    : 2022/11/8 16:18
# @Software: PyCharm
# @Description:
import time

from flask import current_app

from log_settings import logger
from src import create_app
from utils.kane_celery import make_celery

# todo
# crontab实现定时任务

cele = make_celery(create_app())


@cele.task(name="celery_reverse_string-test")
def reverse(do_string):
    with current_app.app_context():
        time.sleep(60)
        return do_string[::-1]


@cele.task(name="celery.reverse_schedule")
def reverse_schedule():
    do_string = "12345678"
    logger.info("celery schedule")
    with current_app.app_context():
        return do_string[::-1]
