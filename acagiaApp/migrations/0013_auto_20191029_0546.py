# Generated by Django 2.2.5 on 2019-10-29 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acagiaApp', '0012_auto_20191029_0516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='img',
            field=models.ImageField(blank=True, height_field='300', null=True, upload_to='profiles/', width_field='200'),
        ),
        migrations.AlterField(
            model_name='member',
            name='mem_type',
            field=models.CharField(choices=[('Stu', 'Student'), ('Inst', 'Instructor'), ('Other', 'Other')], default='Stu', max_length=5),
        ),
    ]