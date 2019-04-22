#encoding:utf-8

from devops.celery import app
from utils.jenkins_api import JenkinsApi
from time import sleep
from .models import Deploy
from django.core.mail import send_mail
import time


@app.task(name='代码上线')
def code_release(pk, deploy):
    """
    后台执行上线任务（后台jenkins构建任务）
    :param deploy: Deploy实例(申请上线会往数据库里插一条记录，传过来的就是这条记录）
    :return:
    """
    # jenkins = JenkinsApi()
    # number = jenkins.get_next_build_number(deploy['name'])
    # # Tag是自己在jenkins命名的tag变量名
    # jenkins.build_job(deploy['name'], parameters={'Tag': deploy['version']})
    # sleep(20)
    # console_output = jenkins.get_build_console_output(deploy['name'], number)
    # deploy["console_output"] = console_output
    # # deploy.save()

    jenkins = JenkinsApi()
    number = jenkins.get_next_build_number(deploy['name'])
    # Tag是自己在jenkins命名的tag变量名
    jenkins.build_job(deploy['name'], parameters={'Tag': deploy['version']})
    time.sleep(15)
    console_output = jenkins.get_build_console_output(deploy['name'], number)
    deploy['console_output'] = console_output
    Deploy.objects.filter(pk=pk).update(**deploy)
    # return deploy
    return '[{}] Project release completed.......'.format(deploy['name'])


@app.task(name='发送邮件')
def send_email(email_title, email_content, email_list):
    send_mail(email_title, email_content, 'service@notice.169kang.com', email_list,
              fail_silently=False)
    return '邮件发送成功！！！'


@app.task(name='打印日志')
def print_log():
    cur_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    file = r'/tmp/devops8.txt'
    with open(file, 'a+') as f:
        f.write(cur_time+'\n')
