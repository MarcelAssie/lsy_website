# Generated by Django 5.0.7 on 2025-07-30 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='violence',
            name='witnesses',
            field=models.TextField(blank=True, help_text='Témoins éventuels (noms, rôles, observations)'),
        ),
    ]
