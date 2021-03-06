# Generated by Django 2.2.5 on 2019-10-23 05:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acagiaApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='academy',
            old_name='addr_id',
            new_name='addr',
        ),
        migrations.RenameField(
            model_name='academy',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='attendance',
            old_name='course_id',
            new_name='course',
        ),
        migrations.RenameField(
            model_name='attendance',
            old_name='stu_id',
            new_name='stu',
        ),
        migrations.RenameField(
            model_name='competition',
            old_name='stu_id',
            new_name='stu',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='inst_id',
            new_name='inst',
        ),
        migrations.RenameField(
            model_name='instructor',
            old_name='mem_id',
            new_name='mem',
        ),
        migrations.RenameField(
            model_name='member',
            old_name='aca_id',
            new_name='aca',
        ),
        migrations.RenameField(
            model_name='member',
            old_name='addr_id',
            new_name='addr',
        ),
        migrations.RenameField(
            model_name='rank',
            old_name='stu_id',
            new_name='stu',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='mem_id',
            new_name='mem',
        ),
    ]
