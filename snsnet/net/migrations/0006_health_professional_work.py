# Generated by Django 3.1.7 on 2021-04-10 18:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('net', '0005_remove_health_institution_is_validated'),
    ]

    operations = [
        migrations.AddField(
            model_name='health_professional',
            name='work',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='net.health_institution'),
        ),
    ]