# Generated by Django 5.1.1 on 2024-10-07 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_cc', '0008_remove_event_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='type',
            field=models.CharField(default='', max_length=50),
        ),
    ]