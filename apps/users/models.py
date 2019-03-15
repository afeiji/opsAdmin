from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField("姓名", max_length=32, null=True, help_text="姓名")
    phone = models.CharField("电话", max_length=11, blank=True, default='', help_text="手机号")

    class Meta:
        # 注释
        verbose_name = "用户"
        # 以id正向排序
        ordering = ["id"]
        # 数据库名
        db_table = 'auth_user'

    def __str__(self):
        return self.username
