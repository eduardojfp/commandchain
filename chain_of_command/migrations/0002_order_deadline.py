# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('chain_of_command', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='Deadline',
            field=models.DateTimeField(null=True, auto_now=True),
            preserve_default=True,
        ),
    ]
