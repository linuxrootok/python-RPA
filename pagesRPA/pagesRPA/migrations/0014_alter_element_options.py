# Generated by Django 3.2 on 2023-03-21 02:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pagesRPA', '0013_alter_project_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='element',
            options={'ordering': ('id',), 'permissions': [('duplicate_selected', 'Can copy element')], 'verbose_name': 'Element', 'verbose_name_plural': 'Elements'},
        ),
    ]