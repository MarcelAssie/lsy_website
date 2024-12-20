# Generated by Django 5.0.7 on 2024-12-07 13:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('administration', '0001_initial'),
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='absence',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='absences', to='authentication.student'),
        ),
        migrations.AddField(
            model_name='coefficient',
            name='school_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.class'),
        ),
        migrations.AddField(
            model_name='note',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.student'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='class_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.class'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.subject'),
        ),
        migrations.AddField(
            model_name='note',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.subject'),
        ),
        migrations.AddField(
            model_name='coefficient',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.subject'),
        ),
        migrations.AddField(
            model_name='teacherschedule',
            name='class_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.class'),
        ),
        migrations.AddField(
            model_name='teacherschedule',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.teacher'),
        ),
        migrations.AlterUniqueTogether(
            name='coefficient',
            unique_together={('school_class', 'subject')},
        ),
    ]
