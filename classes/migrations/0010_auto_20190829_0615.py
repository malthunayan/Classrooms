# Generated by Django 2.1.5 on 2019-08-29 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0009_auto_20190829_0614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='exam_grade',
            field=models.PositiveSmallIntegerField(),
        ),
    ]
