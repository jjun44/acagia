# Generated by Django 2.2.5 on 2019-10-30 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acagiaApp', '0014_auto_20191029_0627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_days',
            field=models.CharField(choices=[('M', 'Mon'), ('T', 'Tu'), ('W', 'Wed'), ('Th', 'Th'), ('F', 'Fri'), ('Sa', 'Sat'), ('S', 'Sun')], max_length=10),
        ),
    ]
