# @Author  : kane.zhu
# @Time    : 2022/11/7 21:22
# @Software: PyCharm
# @Description:
from settings.conf import PrdConfig
from src import create_app

if __name__ == '__main__':
    app = create_app({'SECRET_KEY': 'affedasafafqwe'})
    app.run(host=PrdConfig.SERVER_HOST, port=PrdConfig.SERVER_PORT)
