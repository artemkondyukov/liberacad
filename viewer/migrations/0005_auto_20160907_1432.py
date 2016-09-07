# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-07 11:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0004_auto_20160831_2351'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contour',
            name='filename',
        ),
        migrations.RemoveField(
            model_name='contour',
            name='maskFilename',
        ),
        migrations.RemoveField(
            model_name='trainablemodel',
            name='structureFilename',
        ),
        migrations.RemoveField(
            model_name='trainablemodel',
            name='weightsFilename',
        ),
        migrations.AddField(
            model_name='contour',
            name='contourFile',
            field=models.FileField(default='/data/contour_files/default.npz', upload_to='data/contour_files/'),
        ),
        migrations.AddField(
            model_name='contour',
            name='maskFile',
            field=models.FileField(default='/data/mask_files/default.npz', upload_to='data/mask_files/'),
        ),
        migrations.AddField(
            model_name='trainablemodel',
            name='structureFile',
            field=models.FileField(default='data/trainable_models/structures/default.yaml', upload_to='data/trainable_models/structures/'),
        ),
        migrations.AddField(
            model_name='trainablemodel',
            name='weightsFile',
            field=models.FileField(default='data/trainable_models/weights/default.h5', upload_to='data/trainable_models/weights'),
        ),
        migrations.AlterField(
            model_name='dicomimage',
            name='file',
            field=models.FileField(default='data/dicom_images/default.dcm', upload_to='data/dicom_images/'),
        ),
    ]
