# Generated by Django 2.2.5 on 2020-01-22 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acagiaApp', '0046_auto_20200120_0024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentterm',
            name='discount',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
