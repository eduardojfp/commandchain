# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hierarchy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('Name', models.CharField(max_length=80)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('Content', models.TextField()),
                ('TS', models.TimeField(auto_now_add=True)),
                ('IsRead', models.BooleanField(default=False)),
                ('Issuer', models.ForeignKey(to='chain_of_command.Member')),
                ('Receiver', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('Deadline', models.DateTimeField(null=True, auto_now_add=True)),
                ('Issuer', models.ForeignKey(to='chain_of_command.Member')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('Name', models.CharField(unique=True, max_length=80)),
                ('Description', ckeditor.fields.RichTextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('Name', models.CharField(max_length=80)),
                ('CanGrantMembership', models.BooleanField(default=False)),
                ('CanIssueOrders', models.BooleanField(default=False)),
                ('CanEditOrganization', models.BooleanField(default=False)),
                ('CanEditPrivileges', models.BooleanField(default=False)),
                ('Percolates', models.BooleanField(default=False)),
                ('Organization', models.ForeignKey(to='chain_of_command.Organization')),
                ('associated', models.ManyToManyField(to='chain_of_command.Member', null=True, blank=True)),
                ('boss', models.ForeignKey(to='chain_of_command.Position', default=None, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('Title', models.TextField()),
                ('timestamp', models.TimeField(auto_now=True)),
                ('Content', ckeditor.fields.RichTextField()),
                ('Visible', models.BooleanField(default=True)),
                ('Creator', models.ForeignKey(to='chain_of_command.Member')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='order',
            name='P',
            field=models.ForeignKey(default=0, to='chain_of_command.Position'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='Post',
            field=models.ForeignKey(to='chain_of_command.Post'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='Organization',
            field=models.ForeignKey(to='chain_of_command.Organization'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='User',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hierarchy',
            name='issuer',
            field=models.ForeignKey(to='chain_of_command.Position', related_name='Fi'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hierarchy',
            name='receiver',
            field=models.ForeignKey(to='chain_of_command.Member'),
            preserve_default=True,
        ),
    ]
