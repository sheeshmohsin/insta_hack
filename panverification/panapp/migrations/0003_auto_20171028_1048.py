# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('panapp', '0002_userdata_is_scanned'),
    ]

    operations = [
        migrations.CreateModel(
            name='FailedUserData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('invalid', models.CharField(max_length=2, choices=[(1, b'Name Invalid'), (2, b'DOB Invalid'), (3, b'PAN Invalid'), (4, b'IMG Invalid'), (5, b'IMG Forged')])),
            ],
        ),
        migrations.CreateModel(
            name='FeedbackData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('feedback_for', models.CharField(max_length=2, choices=[(1, b'Name Feedback'), (2, b'DOB Feedback'), (3, b'PAN Feedback'), (4, b'IMG Feedback')])),
                ('details', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='userdata',
            name='feedback_dob',
        ),
        migrations.RemoveField(
            model_name='userdata',
            name='feedback_name',
        ),
        migrations.RemoveField(
            model_name='userdata',
            name='feedback_pan',
        ),
        migrations.AddField(
            model_name='feedbackdata',
            name='user_data',
            field=models.ForeignKey(to='panapp.UserData'),
        ),
        migrations.AddField(
            model_name='faileduserdata',
            name='user_data',
            field=models.ForeignKey(to='panapp.UserData'),
        ),
    ]
