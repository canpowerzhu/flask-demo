# flask-demo

[![AUR](https://img.shields.io/badge/license-Apache%20License%202.0-blue.svg)](https://github.com/canpowerzhu/flask-demo/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/canpowerzhu/flask-demo.svg?style=social&label=Stars)](https://github.com/canpowerzhu/flask-demo/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/canpowerzhu/flask-demo.svg?style=social&label=Fork)](https://github.com/canpowerzhu/flask-demo/network/members)

# FAQ

1. celery任务state在windows环境一直处理pending
   切换模式 -P threads解决
    ```
   celery -A tasks.task worker --loglevel=info -P threads
   ```
2. 如何启用flower进行监控任务状态
    ```
   celery -A tasks.task flower --address=0.0.0.0 --port=5555
   ```
3. 启用Beat用于crontab来跑定时任务
    ```
   celery -A tasks.task beat --loglevel=info
   ```
4. 我们安装完成celery后，import 导入异常如下：
    ```
   ImportError: cannot import name 'Celery' from partially initialized module 'celery' (most likely due to a circular import) 
   ```
   安装 importlib-metadata==4.13.0这个包即可

5. 生成二维码报错 No module named 'Image'
   ```shell
   pip3 install pillow==8.2.0

```

6. 生成二维码  'str' object has no attribute 'write'
   ```

需要固定qrcode版本 8.2.0

```