# Generated by Django 5.2.1 on 2025-05-28 05:55

import django.core.files.storage
import pathlib
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tuzilma', '0010_alter_direction_faculty_alter_direction_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduleupload',
            name='file',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location=pathlib.PurePosixPath('/home/cbekoder/PycharmProjects/fjsti_register_bot/files/schedules')), upload_to='', verbose_name='Fayl'),
        ),
    ]
