# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chain_of_command', '0005_auto_20140914_2356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='Organization',
            field=models.ForeignKey(to='chain_of_command.Organization', db_constraint=False),
        ),
        migrations.AlterField(
            model_name='position',
            name='boss',
            field=models.ForeignKey(to='chain_of_command.Position', db_constraint=False, default=0),
        ),
    ]
