# Generated by Django 3.1.7 on 2021-04-05 13:05

from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('system', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dissertation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('description', models.TextField()),
                ('is_approved', models.BooleanField(default=False)),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('jury_date', django_jalali.db.models.jDateField()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('system.user',),
        ),
        migrations.CreateModel(
            name='StudentFields',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_at', models.DateField(auto_now_add=True)),
                ('is_graduated', models.BooleanField(default=False)),
                ('is_daily', models.BooleanField(default=True)),
                ('describtion', models.CharField(blank=True, max_length=300)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='system.group')),
                ('orientation', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='system.orientation')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='student.student')),
            ],
        ),
        migrations.CreateModel(
            name='JuryRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(0, 'Rejected'), (1, 'Accepted'), (2, 'In Progress')], default=2)),
                ('jury_date', models.DateField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('supervisor_ok', models.BooleanField(default=False)),
                ('supervisor_quote', models.CharField(blank=True, max_length=400)),
                ('manager_ok', models.BooleanField(default=False)),
                ('manager_quote', models.CharField(blank=True, max_length=400)),
                ('staff_ok', models.BooleanField(default=False)),
                ('staff_quote', models.CharField(blank=True, max_length=400)),
                ('dissertation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='student.dissertation')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='student.student')),
            ],
        ),
        migrations.CreateModel(
            name='DissertationReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=400)),
                ('summary', models.CharField(max_length=500)),
                ('problems', models.CharField(max_length=500)),
                ('proceedings', models.CharField(max_length=500)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('supervisor_ok', models.BooleanField(default=False)),
                ('manager_ok', models.BooleanField(default=False)),
                ('supervisor_quote', models.CharField(blank=True, max_length=400)),
                ('manager_quote', models.CharField(blank=True, max_length=400)),
                ('disserta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.dissertation')),
            ],
        ),
        migrations.AddField(
            model_name='dissertation',
            name='student',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='student.student'),
        ),
        migrations.CreateModel(
            name='AchievementReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade_average', models.JSONField()),
                ('status', models.IntegerField(choices=[(0, 'Rejected'), (1, 'Accepted'), (2, 'In Progress')], default=2)),
                ('report_id', models.CharField(blank=True, max_length=20)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('supervisor_ok', models.BooleanField(default=False)),
                ('manager_ok', models.BooleanField(default=False)),
                ('supervisor_quote', models.CharField(blank=True, max_length=400)),
                ('manager_quote', models.CharField(blank=True, max_length=400)),
                ('disserta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.dissertationreport')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.student')),
            ],
        ),
        migrations.AddConstraint(
            model_name='achievementreport',
            constraint=models.UniqueConstraint(fields=('student', 'disserta'), name='report'),
        ),
    ]
