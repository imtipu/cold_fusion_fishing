# Generated by Django 4.2.8 on 2023-12-20 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_alter_dailyactivity_expected_cn_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailyactivity',
            name='live_fish',
            field=models.PositiveIntegerField(default=0, verbose_name='Live Fish'),
        ),
    ]
