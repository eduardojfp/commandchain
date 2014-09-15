# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chain_of_command', '0008_auto_20140915_0006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='Organization',
            field=models.ForeignKey(default=None, blank=True, null=True, to='chain_of_command.Organization'),
        ),
        migrations.AlterField(
            model_name='position',
            name='boss',
            field=models.ForeignKey(default=None, blank=True, null=True, to='chain_of_command.Position'),
        ),
    ]
