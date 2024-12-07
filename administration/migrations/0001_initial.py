# Generated by Django 5.0.7 on 2024-12-07 13:20

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Absence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('reason', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('4ème1', '4ème 1'), ('4ème2', '4ème 2'), ('4ème3', '4ème 3'), ('3ème1', '3ème 1'), ('3ème2', '3ème 2'), ('3ème3', '3ème 3'), ('2ndeC1', '2nde C1'), ('2ndeC2', '2nde C2'), ('2ndeC3', '2nde C3'), ('2ndeC4', '2nde C4'), ('2ndeC5', '2nde C5'), ('1èreC1', '1ère C1'), ('1èreC2', '1ère C2'), ('1èreC3', '1ère C3'), ('1èreC4', '1ère C4'), ('1èreC5', '1ère C5'), ('1èreD1', '1ère D1'), ('1èreD2', '1ère D2'), ('TerminaleC1', 'Terminale C1'), ('TerminaleC2', 'Terminale C2'), ('TerminaleC3', 'Terminale C3'), ('TerminaleC4', 'Terminale C4'), ('TerminaleC5', 'Terminale C5'), ('TerminaleD1', 'Terminale D1'), ('TerminaleD2', 'Terminale D2')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Coefficient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coefficient', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Information',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('category', models.CharField(choices=[('warning', 'Avertissement'), ('event', 'Évènement'), ('danger', 'Danger'), ('info', 'Information')], max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.DecimalField(decimal_places=2, max_digits=5)),
                ('date', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_week', models.CharField(choices=[('Lundi', 'Lundi'), ('Mardi', 'Mardi'), ('Mercredi', 'Mercredi'), ('Jeudi', 'Jeudi'), ('Vendredi', 'Vendredi')], max_length=10)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Histoire-Géographie', 'Histoire-Géographie'), ('Physique-Chimie', 'Physique-Chimie'), ('Français', 'Français'), ('Anglais', 'Anglais'), ('Langue Vivante 2', 'Langue Vivante 2'), ('Mathématiques', 'Mathématiques'), ('Éducation Civique et Morale', 'Éducation Civique et Morale'), ('Philosophie', 'Philosophie'), ('Arts Plastiques', 'Arts Plastiques'), ('Musique', 'Musique'), ('Éducation Physique et Sportive', 'Éducation Physique et Sportive'), ('Natation', 'Natation')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TeacherSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_week', models.CharField(choices=[('Lundi', 'Lundi'), ('Mardi', 'Mardi'), ('Mercredi', 'Mercredi'), ('Jeudi', 'Jeudi'), ('Vendredi', 'Vendredi')], max_length=10)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
            ],
        ),
    ]
