# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-24 02:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminsite', '0002_auto_20170423_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='identity',
            field=models.CharField(blank=True, choices=[('normal', 'normal'), ('author', 'author')], max_length=10, null=True, verbose_name='身份'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='nick_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='昵称'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image',
            field=models.URLField(blank=True, max_length=100, null=True, verbose_name='头像地址'),
        ),
    ]