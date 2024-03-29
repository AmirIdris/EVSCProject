# Generated by Django 3.2.6 on 2021-09-05 07:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EVSCapp', '0014_alter_records_vehicle_speed'),
    ]

    operations = [
        migrations.CreateModel(
            name='VehicleTracker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('records', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='record_tracking', to='EVSCapp.records')),
            ],
        ),
    ]
