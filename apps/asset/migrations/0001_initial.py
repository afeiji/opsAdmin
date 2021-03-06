# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-03-27 16:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cloud',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='云厂商名称')),
                ('code', models.CharField(max_length=50, verbose_name='云厂商英文名')),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpu', models.CharField(max_length=5, verbose_name='CPU')),
                ('memory', models.CharField(max_length=100, verbose_name='内存/M')),
                ('creationtime', models.DateTimeField(verbose_name='创建时间')),
                ('expiredTime', models.DateTimeField(verbose_name='过期时间')),
                ('instancechargetype', models.CharField(max_length=50, verbose_name='实例计费类型')),
                ('instanceId', models.CharField(max_length=100, verbose_name='实例ID')),
                ('instancename', models.CharField(max_length=100, verbose_name='实例名称')),
                ('status', models.CharField(max_length=50, verbose_name='实例状态')),
                ('privateipaddress', models.CharField(max_length=50, verbose_name='内网IP')),
                ('publicipaddress', models.CharField(blank=True, default='', max_length=50, verbose_name='公网网IP')),
                ('zoneid', models.CharField(max_length=50, verbose_name='实例所在地域')),
                ('cloud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asset.Cloud')),
            ],
            options={
                'verbose_name': '主机信息',
                'ordering': ['-creationtime'],
            },
        ),
    ]
