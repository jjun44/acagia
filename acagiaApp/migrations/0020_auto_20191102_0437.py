# Generated by Django 2.2.5 on 2019-11-02 04:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('acagiaApp', '0019_auto_20191102_0426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='member',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='att_mem', to='acagiaApp.Member'),
            preserve_default=False,
        ),
    ]
