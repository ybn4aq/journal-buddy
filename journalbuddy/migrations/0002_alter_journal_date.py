# Generated by Django 4.2.11 on 2024-03-24 13:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journalbuddy', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='date',
            field=models.DateField(default=datetime.date(2024, 3, 24)),
        ),
    ]