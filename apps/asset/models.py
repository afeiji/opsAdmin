#encoding:utf-8
from django.db import models

class Cloud(models.Model):
    name = models.CharField(max_length=50, verbose_name="云厂商名称")
    code = models.CharField(max_length=50, verbose_name="云厂商英文名")

class Host(models.Model):
    cloud = models.ForeignKey(Cloud)
    cpu = models.CharField(max_length=5, verbose_name="CPU")
    memory = models.CharField(max_length=100, verbose_name="内存/M")
    creationtime = models.DateTimeField(verbose_name="创建时间")
    expiredTime = models.DateTimeField(verbose_name="过期时间")
    instancechargetype = models.CharField(max_length=50, verbose_name="实例计费类型")
    instanceId = models.CharField(max_length=100, verbose_name="实例ID")
    instancename = models.CharField(max_length=100, verbose_name="实例名称")
    status = models.CharField(max_length=50, verbose_name="实例状态")
    privateipaddress = models.CharField(max_length=50, verbose_name="内网IP")
    publicipaddress = models.CharField(max_length=50, blank=True, default="",  verbose_name="公网网IP")
    zoneid = models.CharField(max_length=50, verbose_name="实例所在地域")


    class Meta:
        verbose_name = '主机信息'
        ordering = ['-creationtime']