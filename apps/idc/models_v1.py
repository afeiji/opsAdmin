from django.db import models

# Create your models here.

class Idc(models.Model):
    name = models.CharField("idc名称",max_length=100,)
    address = models.CharField("IDC地址",max_length=200,default="")
    phone = models.CharField("IDC联系电话",max_length=20,null=True)
    email = models.CharField("IDC的email地址",max_length=32)

    # def __str__(self):
    #     return self.name