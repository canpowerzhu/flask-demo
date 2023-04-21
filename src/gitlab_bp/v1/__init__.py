# @Author  : kane.zhu
# @Time    : 2023/4/19 11:46
# @Software: PyCharm
# @Description:

import gitlab

from settings.conf import PrdConfig
from log_settings import logger


def create_gitlab_obj():
    """
    : 初始化gitlab的连接对象
    :return:
    """
    try:
        gl = gitlab.Gitlab(url=PrdConfig.GITLAB_URL, private_token=PrdConfig.GITLAB_PRIVATE_TOKEN)

        return gl
    except Exception as e:
        logger.error("初始化gitlab连接对象异常： {}".format(str(e)))


gitlab_obj = create_gitlab_obj()
