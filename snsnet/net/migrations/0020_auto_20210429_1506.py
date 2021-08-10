# Generated by Django 3.1.7 on 2021-04-29 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('net', '0019_post_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='inst_likers',
            field=models.ManyToManyField(related_name='post_workers', to='net.Health_Institution'),
        ),
        migrations.AddField(
            model_name='post',
            name='prof_likers',
            field=models.ManyToManyField(related_name='post_workers', to='net.Health_Professional'),
        ),
    ]
