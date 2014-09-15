# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chain_of_command', '0009_auto_20140915_0007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='associated',
            field=models.ManyToManyField(null=True, to='chain_of_command.Member', blank=True),
        ),
    ]
