# Generated by Django 4.2.8 on 2023-12-18 23:06

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-created_at'], 'verbose_name': 'Project', 'verbose_name_plural': 'Projects'},
        ),
        migrations.CreateModel(
            name='DailyActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('activity_date', models.DateField()),
                ('dead_fish', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('single_fish_weight', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Single Fish Weight (gm)')),
                ('feed_percentage', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Feed Percentage (%)')),
                ('undigested_percentage', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Undigested Percentage (%)')),
                ('feed_protein_percentage', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Feed Protein Percentage (%)')),
                ('expected_cn', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Expected C.N.')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='daily_activities', to='projects.project')),
            ],
            options={
                'verbose_name': 'Daily Activity',
                'verbose_name_plural': 'Daily Activities',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddConstraint(
            model_name='dailyactivity',
            constraint=models.UniqueConstraint(fields=('project', 'activity_date'), name='unique_daily_activity'),
        ),
    ]
