# Generated by Django 3.1.7 on 2021-04-05 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('professor', '0001_initial'),
        ('student', '0001_initial'),
        ('system', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Supervisor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percent', models.IntegerField(choices=[(25, 'Q1'), (50, 'Half'), (75, 'Q3'), (100, 'Full')], default=100)),
                ('professor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='professor', to='professor.professor')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='student', to='student.student')),
            ],
        ),
        migrations.CreateModel(
            name='JuryInvitation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(0, 'Rejected'), (1, 'Accepted'), (2, 'In Progress')], default=2)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('jury_date', models.DateField()),
                ('disserta', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='student.dissertation')),
                ('professor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='professor.professor')),
            ],
        ),
        migrations.CreateModel(
            name='Adminstrator',
            fields=[
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='system.group')),
                ('professor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='professor.professor')),
            ],
        ),
        migrations.AddConstraint(
            model_name='supervisor',
            constraint=models.UniqueConstraint(fields=('student', 'professor'), name='supervisor'),
        ),
    ]
