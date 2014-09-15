# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chain_of_command', '0010_auto_20140915_0008'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='P',
            field=models.ForeignKey(to='chain_of_command.Position', default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='position',
            name='Organization',
            field=models.ForeignKey(to='chain_of_command.Organization'),
        ),
        migrations.AlterField(
            model_name='post',
            name='timestamp',
            field=models.TimeField(auto_now=True),
        ),
    ]
