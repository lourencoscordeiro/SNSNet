# Generated by Django 3.1.7 on 2021-04-28 18:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('net', '0013_auto_20210428_1823'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='user',
        ),
    ]
