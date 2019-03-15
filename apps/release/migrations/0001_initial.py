# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-03-12 09:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Deploy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='项目名称')),
                ('version', models.CharField(max_length=40, verbose_name='项目版本')),
                ('info', models.CharField(max_length=100, verbose_name='版本描述')),
                ('detail', models.TextField(verbose_name='上线详情')),
                ('status', models.IntegerField(choices=[(0, '申请'), (1, '已审核'), (2, '灰度'), (3, '上线'), (4, '取消上线')], default=0, verbose_name='上线状态')),
                ('console_output', models.TextField(default='', help_text='jenkins控制台输出的结果', verbose_name='上线输出结果')),
                ('apply_time', models.DateTimeField(auto_now_add=True, verbose_name='申请时间')),
                ('deploy_time', models.DateTimeField(auto_now=True, verbose_name='上线完成时间')),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicant', to=settings.AUTH_USER_MODEL, verbose_name='申请人')),
                ('assign_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned', to=settings.AUTH_USER_MODEL, verbose_name='上线人')),
                ('reviewer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviewer', to=settings.AUTH_USER_MODEL, verbose_name='审核人')),
            ],
            options={
                'verbose_name': '发布系统',
                'verbose_name_plural': '发布系统',
                'ordering': ['-apply_time'],
            },
        ),
    ]
