# @Author  : kane.zhu
# @Time    : 2022/12/2 16:21
# @Software: PyCharm
# @Description:

from celery.schedules import crontab

beat_schedule = {
    'add-every-30-seconds': {
        'task': 'celery.reverse_schedule',
        'schedule': crontab(minute="*"),
    },
}
