# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chain_of_command', '0007_auto_20140915_0003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='Organization',
            field=models.ForeignKey(null=True, default=None, to='chain_of_command.Organization'),
        ),
        migrations.AlterField(
            model_name='position',
            name='boss',
            field=models.ForeignKey(null=True, default=None, to='chain_of_command.Position'),
        ),
    ]
