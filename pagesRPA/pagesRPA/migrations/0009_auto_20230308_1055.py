# Generated by Django 3.2 on 2023-03-08 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagesRPA', '0008_element_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='element',
            name='after_delay',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=3),
        ),
        migrations.AddField(
            model_name='element',
            name='before_delay',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=3),
        ),
    ]
