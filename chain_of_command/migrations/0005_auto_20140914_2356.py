# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chain_of_command', '0004_position_boss'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='boss',
            field=models.ForeignKey(default=0, to='chain_of_command.Position'),
        ),
    ]
