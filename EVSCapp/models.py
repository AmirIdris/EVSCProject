from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django_extensions.db.models import TimeStampedModel



# Create your models here.


class Vehicle(models.Model):
    """Model definition for Vehicle."""
    vehicle_plate=models.CharField(max_length=11)
    vehicle_type=models.CharField(max_length=100)
    vehicle_owner=models.CharField(max_length=100)


    # TODO: Define fields here

    class Meta:
        """Meta definition for Vehicle."""

        verbose_name = 'Vehicle'
        verbose_name_plural = 'Vehicles'

    def __str__(self):
        """Unicode representation of Vehicle."""
        return str(self.vehicle_plate)

class Records(models.Model):
    """Model definition for Records."""
    vehicle=models.ForeignKey(Vehicle,on_delete=models.CASCADE,related_name="records")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,null=True)
    address=models.CharField(max_length=50)
    vehicle_speed=models.IntegerField(null=True)
    duration=models.TimeField(null = True)
    status=models.BooleanField("is_reported",default=False)

    created_at=models.DateTimeField(auto_now_add=True)


    # TODO: Define fields here

    class Meta:
        """Meta definition for Records."""

        verbose_name = 'Record'
        verbose_name_plural = 'Records'

    def __str__(self):
        """Unicode representation of Records."""
        return str(self.vehicle.vehicle_plate)



class TrafficPoliceLocation(models.Model):
    location_name = models.CharField(max_length=50)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.location_name



class TrafficPolice(models.Model):
    """Model definition for TrafficPolice."""
    gender_choices=(('M','Male'),('F','Female'))
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='traffic_police')
    location = models.OneToOneField(TrafficPoliceLocation, on_delete=models.CASCADE, related_name='traffic_location',null=True)
    fcm_token=models.TextField(null=True)
    phone_number=models.CharField(max_length=100)
    status=models.BooleanField("Active",default=True)
    gender = models.CharField(max_length = 1, choices = gender_choices ,default='M')
    


    # TODO: Define fields here

    class Meta:
        """Meta definition for TrafficPolice."""

        verbose_name = 'TrafficPolice'
        verbose_name_plural = 'TrafficPolices'

    def __str__(self):
        """Unicode representation of TrafficPolice."""
        return self.user.username

class Notification(models.Model):
    recipient=models.ForeignKey(TrafficPolice,on_delete=models.CASCADE,related_name="traffic_police_notification")
    records=models.OneToOneField(Records,on_delete=models.CASCADE,related_name="record_notification")
    content=models.TextField(null=True)


    def __str__(self):
        return str(self.records.vehicle)
        

class Report(models.Model):
    """Model definition for Report."""
    description=models.TextField()
    records=models.ForeignKey(Records,on_delete=models.CASCADE,related_name="report")
    traffic_police=models.ForeignKey(TrafficPolice,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)



    # TODO: Define fields here

    class Meta:
        """Meta definition for Report."""

        verbose_name = 'Report'
        verbose_name_plural = 'Reports'

        permissions=(
            ('read_repor','can read report'),
        )

    def __str__(self):
        """Unicode representation of Report."""
        return self.description
class SystemAdmin(models.Model):
    """Model definition for SystemAdmin."""
    gender_choices=(('M','Male'),('F','Female'))
    user=models.OneToOneField(User, on_delete=models.CASCADE,related_name="system_admin")
    phone_number=models.CharField(max_length=50)
    status=models.BooleanField("Active",default=True)
    gender = models.CharField(max_length = 1, choices = gender_choices ,default='M')
    profile_picture = models.FileField(null = True)

    # TODO: Define fields here

    class Meta:
        """Meta definition for SystemAdmin."""

        verbose_name = 'SystemAdmin'
        verbose_name_plural = 'SystemAdmins'

    def __str__(self):
        """Unicode representation of SystemAdmin."""
        return str(self.user.username)


