# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-28 14:17
from __future__ import unicode_literals

from django.db import migrations

def transfer_medium(apps, schema_editor):
    NoticeSetting = apps.get_model('pinax_notifications', 'NoticeSetting')
    for notice_setting in NoticeSetting.objects.all():
        notice_setting.medium = notice_setting.medium_new
        notice_setting.save(update_fields=['medium'])


class Migration(migrations.Migration):

    dependencies = [
        ('pinax_notifications', '0004_auto_20170228_1415'),
    ]

    operations = [
        migrations.RunPython(transfer_medium),
    ]