# Generated by Django 2.2.5 on 2019-12-15 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acagiaApp', '0037_auto_20191214_0537'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='credit',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='memberevent',
            name='division',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='memberevent',
            name='reward',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
