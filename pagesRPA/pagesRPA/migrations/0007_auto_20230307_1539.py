# Generated by Django 3.2 on 2023-03-07 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagesRPA', '0006_auto_20230307_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='element',
            name='class_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='element',
            name='id_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='element',
            name='text',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='element',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
