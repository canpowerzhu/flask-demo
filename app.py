# @Author  : kane.zhu
# @Time    : 2022/11/7 21:22
# @Software: PyCharm
# @Description:
from src import create_app
from settings.conf import PrdConfig

if __name__ == '__main__':
    app = create_app()
    app.run(host=PrdConfig.SERVER_HOST, port=PrdConfig.SERVER_PORT)