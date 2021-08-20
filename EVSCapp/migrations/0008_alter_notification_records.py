# Generated by Django 3.2.6 on 2021-08-20 07:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EVSCapp', '0007_alter_notification_recipient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='records',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='record_notification', to='EVSCapp.records'),
        ),
    ]
