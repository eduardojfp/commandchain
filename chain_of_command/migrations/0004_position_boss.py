# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chain_of_command', '0003_auto_20140914_2131'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='boss',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
