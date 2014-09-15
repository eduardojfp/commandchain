# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chain_of_command', '0006_auto_20140915_0001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='Organization',
            field=models.ForeignKey(db_constraint=False, to='chain_of_command.Organization', null=True),
        ),
        migrations.AlterField(
            model_name='position',
            name='boss',
            field=models.ForeignKey(default=0, null=True, db_constraint=False, to='chain_of_command.Position'),
        ),
    ]
