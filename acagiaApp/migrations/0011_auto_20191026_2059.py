# Generated by Django 2.2.5 on 2019-10-26 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acagiaApp', '0010_auto_20191026_2039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rank',
            name='rank',
            field=models.CharField(choices=[('White', 'White'), ('Orange', 'Orange'), ('Yellow', 'Yellow'), ('Green', 'Green'), ('Purple', 'Purple'), ('Blue', 'Blue'), ('Brown', 'Brown'), ('Red', 'Red'), ('Red/Black', 'Red/Black'), ('Black', 'Black')], default='None', max_length=10),
        ),
    ]