# @Author  : kane.zhu
# @Time    : 2023/3/23 15:11
# @Software: PyCharm
# @Description:


import jenkins
from settings.conf import PrdConfig

# 初始化jenkins连接对象
def init_jenkins_object():
    server = jenkins.Jenkins(PrdConfig.JENKINS_HOST,username="kane_zhu",password="Moppo123")
    return  server


