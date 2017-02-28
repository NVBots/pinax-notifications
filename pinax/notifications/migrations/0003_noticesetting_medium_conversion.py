# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def convert_medium(apps, schema_editor):
    NoticeSetting = apps.get_model('pinax_notifications', 'NoticeSetting')
    for notice_setting in NoticeSetting.objects.all():
        try:
            notice_setting.medium_new = int(notice_setting.medium)
        except:
            notice_setting.medium_new = 0
        notice_setting.medium = None
        notice_setting.save(update_fields=['medium', 'medium_new'])
    


class Migration(migrations.Migration):

    dependencies = [
        ('pinax_notifications', '0002_noticesetting_medium_new'),
    ]

    operations = [
        migrations.RunPython(convert_medium),
    ]
