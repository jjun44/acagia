# Generated by Django 2.2.5 on 2019-10-26 17:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('acagiaApp', '0008_auto_20191026_0556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instructor',
            name='mem',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='inst_info', to='acagiaApp.Member'),
        ),
        migrations.AlterField(
            model_name='student',
            name='mem',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='stu_info', to='acagiaApp.Member'),
        ),
    ]