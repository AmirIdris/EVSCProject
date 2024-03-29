# Generated by Django 3.2.6 on 2021-08-23 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EVSCapp', '0011_auto_20210823_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='is_chewing_chat',
            field=models.BooleanField(default=False, verbose_name='Chewing Chat'),
        ),
        migrations.AlterField(
            model_name='report',
            name='is_drunk',
            field=models.BooleanField(default=False, verbose_name='Drunk'),
        ),
        migrations.AlterField(
            model_name='report',
            name='is_not_having_license',
            field=models.BooleanField(default=False, verbose_name='Does Not Have license'),
        ),
        migrations.AlterField(
            model_name='report',
            name='is_using_cell_phone',
            field=models.BooleanField(default=False, verbose_name='Using CellPhone'),
        ),
    ]
