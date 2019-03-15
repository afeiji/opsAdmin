#encoding:utf-8

import os
import django
from celery import Celery, platforms
from django.conf import settings
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devops.settings')
django.setup()
app = Celery('devops')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
platforms.C_FORCE_ROOT = True # 使用root启动
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
