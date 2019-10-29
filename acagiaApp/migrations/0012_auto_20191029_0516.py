# Generated by Django 2.2.5 on 2019-10-29 05:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('acagiaApp', '0011_auto_20191026_2059'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_date', models.DateField()),
                ('event_start_time', models.TimeField(blank=True, null=True)),
                ('event_end_time', models.TimeField(blank=True, null=True)),
                ('event_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='StudentEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('division', models.CharField(max_length=30)),
                ('weight', models.FloatField(blank=True, null=True)),
                ('reward', models.CharField(blank=True, max_length=20, null=True)),
                ('aca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='se_aca', to='acagiaApp.Academy')),
                ('event', models.ForeignKey(on_delete=models.SET('Deleted'), related_name='se_event', to='acagiaApp.Event')),
            ],
        ),
        migrations.CreateModel(
            name='StudentRank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('days_at_this_rank', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='instructor',
            name='mem',
        ),
        migrations.RenameField(
            model_name='member',
            old_name='pay_day',
            new_name='member_since',
        ),
        migrations.RemoveField(
            model_name='course',
            name='inst',
        ),
        migrations.RemoveField(
            model_name='rank',
            name='days_attended',
        ),
        migrations.RemoveField(
            model_name='rank',
            name='stu',
        ),
        migrations.RemoveField(
            model_name='student',
            name='date_of_start',
        ),
        migrations.AddField(
            model_name='course',
            name='aca',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, related_name='course_aca', to='acagiaApp.Academy'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='instructor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='course_inst', to='acagiaApp.Member'),
        ),
        migrations.AlterField(
            model_name='address',
            name='street',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='aca',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='att_aca', to='acagiaApp.Academy'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='att_course', to='acagiaApp.Course'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='member',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='att_mem', to='acagiaApp.Member'),
        ),
        migrations.AlterField(
            model_name='member',
            name='aca',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mem_aca', to='acagiaApp.Academy'),
        ),
        migrations.AlterField(
            model_name='student',
            name='mem',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='stu_mem', to='acagiaApp.Member'),
        ),
        migrations.DeleteModel(
            name='Competition',
        ),
        migrations.DeleteModel(
            name='Instructor',
        ),
        migrations.AddField(
            model_name='studentrank',
            name='rank',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sr_rank', to='acagiaApp.Rank'),
        ),
        migrations.AddField(
            model_name='studentrank',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sr_stu', to='acagiaApp.Student'),
        ),
        migrations.AddField(
            model_name='studentevent',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='se_stu', to='acagiaApp.Student'),
        ),
    ]
