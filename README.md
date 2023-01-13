# flask-demo
some common module based on flask


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

