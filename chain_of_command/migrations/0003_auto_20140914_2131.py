# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('chain_of_command', '0002_order_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='Name',
            field=models.CharField(unique=True, max_length=80),
        ),
    ]
