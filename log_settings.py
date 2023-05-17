# @Author  : kane.zhu
# @Time    : 2022/11/7 21:29
# @Software: PyCharm
# @Description:
import os.path
import time
from flask import request
from loguru import logger

log_path = os.path.join(os.getcwd(), 'logs')
if not log_path:
    os.mkdir(log_path)

log_path_error = os.path.join(log_path, f'{time.strftime("%Y-%m-%d")}_error.log')
log_path_info = os.path.join(log_path, f'{time.strftime("%Y-%m-%d")}_info.log')
log_path_debug = os.path.join(log_path, f'{time.strftime("%Y-%m-%d")}_debug.log')


# 增加level决定 信息记录到哪个文件
logger.add(log_path_error, rotation="12:00", level='ERROR',retention="5 days", enqueue=True)
logger.add(log_path_info, rotation="12:00", level='INFO',retention="3 days", enqueue=True)

