#encoding:utf-8

from devops.celery import app
from asset.qcloud import aly_ecs_api

@app.task(name="多云获取数据")
def get_data():
    aly_ecs_api.save_host()