# Generated by Django 2.2.5 on 2019-11-02 04:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('acagiaApp', '0018_auto_20191102_0422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='att_course', to='acagiaApp.Course'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='member',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='att_mem', to='acagiaApp.Member'),
        ),
    ]
