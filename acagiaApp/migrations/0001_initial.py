# Generated by Django 2.2.5 on 2019-10-22 20:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Academy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aca_name', models.CharField(max_length=30)),
                ('aca_type', models.CharField(choices=[('MMA', 'MMA'), ('General', 'General')], default='General', max_length=10)),
                ('office_phone', models.CharField(max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=20)),
                ('state', models.CharField(choices=[('CA', 'California'), ('NY', 'New York')], max_length=2)),
                ('zip', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('mem_type', models.CharField(choices=[('Stu', 'Student'), ('Inst', 'Instructor'), ('Other', 'Other')], default='Stu', max_length=4)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('cell_phone', models.CharField(max_length=12)),
                ('email', models.EmailField(max_length=40)),
                ('img', models.ImageField(blank=True, height_field='300', null=True, upload_to='mem_photos', width_field='200')),
                ('pay_day', models.DateField(auto_now_add=True)),
                ('aca_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='acagiaApp.Academy')),
                ('addr_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='acagiaApp.Address')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_start', models.DateField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Hold', 'Hold')], max_length=7)),
                ('mem_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='acagiaApp.Member')),
            ],
        ),
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank_type', models.CharField(choices=[('General', 'General'), ('BJJ', 'Jiu-jitsu'), ('TKD', 'Taekwondo')], max_length=10)),
                ('rank', models.CharField(choices=[('White', 'White'), ('Orange', 'Orange'), ('Yellow', 'Yellow'), ('Green', 'Green'), ('Purple', 'Purple'), ('Blue', 'Blue'), ('Brown', 'Brown'), ('Red', 'Red'), ('Red/Black', 'Red/Black'), ('Black', 'Black')], max_length=10)),
                ('days_attended', models.IntegerField(default=0)),
                ('stu_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='acagiaApp.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_hire', models.DateField(auto_now_add=True)),
                ('mem_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='acagiaApp.Member')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=40)),
                ('course_days', models.CharField(max_length=7)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('inst_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='acagiaApp.Instructor')),
            ],
        ),
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comp_date', models.DateField()),
                ('comp_name', models.CharField(max_length=30)),
                ('division', models.CharField(max_length=20)),
                ('weight', models.FloatField(blank=True, null=True)),
                ('reward', models.CharField(blank=True, max_length=20, null=True)),
                ('stu_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='acagiaApp.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_attended', models.DateTimeField(auto_now_add=True)),
                ('course_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='acagiaApp.Course')),
                ('stu_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='acagiaApp.Student')),
            ],
        ),
        migrations.AddField(
            model_name='academy',
            name='addr_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='acagiaApp.Address'),
        ),
        migrations.AddField(
            model_name='academy',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
