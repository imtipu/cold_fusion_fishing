# Generated by Django 4.2.9 on 2024-01-09 07:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_remove_dailyactivity_undigested_percentage'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='expected_cn',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Expected C.N.'),
        ),
    ]
