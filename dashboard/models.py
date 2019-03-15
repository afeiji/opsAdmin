from django.db import models

class Idc(models.Model):
    name = models.CharField("idc名称",max_length=100,)
    address = models.CharField("IDC地址",max_length=200,default="")
    phone = models.CharField("IDC联系电话",max_length=20,null=True)
    user = models.CharField("IDC联系人",max_length=32,null=True)

class Manufacturer(models.Model):
    name = models.CharField(max_length=30)

class Car(models.Model):
    manufacturer = models.ForeignKey(Manufacturer)
    name = models.CharField(max_length=30)
