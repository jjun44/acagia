# Generated by Django 2.2.5 on 2020-02-18 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acagiaApp', '0051_auto_20200218_0805'),
    ]

    operations = [
        migrations.AddField(
            model_name='memberrank',
            name='days_left',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
