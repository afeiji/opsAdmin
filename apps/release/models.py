#encoding:utf-8

from django.db import models
from django.contrib.auth import get_user_model
User =get_user_model()

class Deploy(models.Model):
    STATUS = (
        (0, '申请'),
        (1, '已审核'),
        (2, '灰度'),
        (3, '上线'),
        (4, '取消上线'),
    )
    name = models.CharField(max_length=40, verbose_name=u'项目名称')
    version = models.CharField(max_length=40, verbose_name=u'项目版本')
    info = models.CharField(max_length=100, verbose_name=u'版本描述')
    applicant = models.ForeignKey(User, verbose_name=u'申请人', related_name='applicant')
    reviewer = models.ForeignKey(User, verbose_name=u'审核人', null=True, blank=True, related_name='reviewer')
    assign_to = models.ForeignKey(User, verbose_name=u'上线人', null=True, blank=True, related_name='assigned')
    detail = models.TextField(verbose_name=u'上线详情')
    status = models.IntegerField(default=0, choices=STATUS, verbose_name='上线状态')
    console_output = models.TextField(default='', verbose_name=u'上线输出结果', help_text='jenkins控制台输出的结果')
    apply_time = models.DateTimeField(auto_now_add=True, verbose_name=u'申请时间')
    deploy_time = models.DateTimeField(auto_now=True, verbose_name=u'上线完成时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '发布系统'
        verbose_name_plural = verbose_name
        ordering = ['-apply_time']
