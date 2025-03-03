# Generated by Django 5.1.6 on 2025-03-02 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='age',
        ),
        migrations.AddField(
            model_name='student',
            name='department',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='phone',
            field=models.CharField(default=0, max_length=15),
            preserve_default=False,
        ),
    ]
