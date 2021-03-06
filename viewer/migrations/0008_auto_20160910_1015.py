# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-10 07:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0007_auto_20160910_0951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contour',
            name='dicomImage',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contourFiles', to='viewer.DicomImage'),
        ),
        migrations.AlterField(
            model_name='contour',
            name='producedBy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contourFiles', to='viewer.TrainableModel'),
        ),
        migrations.AlterField(
            model_name='diagnosis',
            name='disease',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='diagnoses', to='viewer.Disease'),
        ),
        migrations.AlterField(
            model_name='dicomimage',
            name='owner',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='dicomImages', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='pathologycontour',
            name='diagnosis',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pathologyContours', to='viewer.Diagnosis'),
        ),
    ]
