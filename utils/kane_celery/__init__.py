# @Author  : kane.zhu
# @Time    : 2022/11/8 16:13
# @Software: PyCharm
# @Description:

from settings.conf import PrdConfig
from utils.kane_celery import cele_schedule


def make_celery(app):
    from celery import Celery
    cele = Celery(app.import_name, backend=PrdConfig.CELERY_RESULT_BACKEND,
                  broker=PrdConfig.BROKER_URL)
    cele.config_from_object(cele_schedule)
    cele.conf.update(app.config)
    TaskBase = cele.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    cele.Task = ContextTask
    return cele
