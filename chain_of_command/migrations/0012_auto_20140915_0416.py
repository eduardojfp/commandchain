# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('chain_of_command', '0011_auto_20140915_0023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='Content',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
