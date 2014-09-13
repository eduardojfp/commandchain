# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hierarchy',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True,
                                        primary_key=True, verbose_name='ID')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True,
                                        primary_key=True, verbose_name='ID')),
                ('Name', models.CharField(max_length=80)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True,
                                        primary_key=True, verbose_name='ID')),
                ('Content', models.TextField()),
                ('TS', models.TimeField(default='CURRENT_TIMESTAMP')),
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
                ('id', models.AutoField(serialize=False, auto_created=True,
                                        primary_key=True, verbose_name='ID')),
                ('Issuer', models.ForeignKey(to='chain_of_command.Member')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True,
                                        primary_key=True, verbose_name='ID')),
                ('Name', models.CharField(max_length=80)),
                ('Description', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True,
                                        primary_key=True, verbose_name='ID')),
                ('Name', models.CharField(max_length=80)),
                ('CanGrantMembership', models.BooleanField(default=False)),
                ('CanIssueOrders', models.BooleanField(default=False)),
                ('CanEditOrganization', models.BooleanField(default=False)),
                ('CanEditPrivileges', models.BooleanField(default=False)),
                ('Percolates', models.BooleanField(default=False)),
                ('Organization',
                 models.ForeignKey(to='chain_of_command.Organization')),
                ('associated',
                 models.ManyToManyField(to='chain_of_command.Member')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True,
                                        primary_key=True, verbose_name='ID')),
                ('Title', models.TextField()),
                ('timestamp', models.TimeField()),
                ('Content', models.TextField()),
                ('Visible', models.BooleanField(default=True)),
                ('Creator', models.ForeignKey(to='chain_of_command.Member')),
            ],
            options={
            },
            bases=(models.Model,),
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
            field=models.ForeignKey(related_name='Fi',
                                    to='chain_of_command.Position'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hierarchy',
            name='receiver',
            field=models.ForeignKey(to='chain_of_command.Member'),
            preserve_default=True,
        ),
    ]
