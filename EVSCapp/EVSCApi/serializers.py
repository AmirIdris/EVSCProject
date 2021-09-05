
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from EVSCapp import models
from EVSCapp.models import Notification, Report,Vehicle,TrafficPolice,Records,VehicleTracker
from django.conf import settings
from django.db.models import fields
from rest_auth.models import TokenModel
from rest_auth.utils import import_callable
from rest_auth.serializers import UserDetailsSerializer as DefaultUserDetailsSerializer
from rest_framework import serializers
from rest_framework.fields import BooleanField, CharField, Field, IntegerField,ReadOnlyField,DecimalField
from django.utils import timezone
from django.shortcuts import get_object_or_404








class VehicleSerializer(serializers.ModelSerializer):

    class Meta:
        model=Vehicle
        fields = "__all__"

class RecordSerializer(serializers.Serializer):
    pk = serializers.ReadOnlyField()
    vehicle = serializers.CharField(max_length=15)
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    vehicle_speed = serializers.IntegerField()
    status = serializers.BooleanField(read_only=True)
    created_at=serializers.SerializerMethodField(read_only=True)

    def create(self,validated_data):
        # vehicle = Vehicle.objects.filter(vehicle_plate__iexact = validated_data['vehicle'])
        vehicle = Vehicle.objects.get(vehicle_plate = validated_data['vehicle'])
        obj=Records.objects.create(vehicle_speed=validated_data['vehicle_speed'],vehicle=vehicle,latitude = validated_data['latitude'],longitude = validated_data['longitude'],duration = timezone.now())
        return obj

    def get_created_at(self,instance):
        return instance.created_at.strftime("%B %d %Y")



rest_auth_serializers=getattr(settings,'REST_AUTH_SERIALIZERS',{})
DefaultUserDetailsSerializer=import_callable(
    rest_auth_serializers.get('USER_DETAILS_SERIALIZER',DefaultUserDetailsSerializer)
)

class CustomTokenSerializer(serializers.ModelSerializer):
    user=DefaultUserDetailsSerializer(read_only=True)
    class Meta:
        model=TokenModel
        fields=('key','user',)


class FcmDevicesSerializer(serializers.ModelSerializer):

    class Meta:
        model=TrafficPolice
        exclude=('id','user','phone_number','status','location')



class UserProfileSerializer(serializers.Serializer):
    username = ReadOnlyField()
    email = ReadOnlyField()
    first_name = ReadOnlyField()
    last_name = ReadOnlyField()
    phone_number = ReadOnlyField(source = "traffic_police.phone_number")
    latitude = DecimalField(source = "traffic_police.user.latitude", max_digits=9, decimal_places=6)
    longitude = DecimalField(source = "traffic_police.user.longitude", max_digits=9, decimal_places=6)





class NotificationSerializer(serializers.Serializer):
    notification_id = ReadOnlyField(source = "id")
    record_id = ReadOnlyField(source = "records.id")
    plate_number = ReadOnlyField(source = "records.vehicle.vehicle_plate")
    vehicle_speed = ReadOnlyField(source = "records.vehicle_speed")
    latitude = ReadOnlyField(source = "records.latitude")
    longtude = ReadOnlyField(source = "records.longitude")
    


    

    
    




class ReportSerializer(serializers.ModelSerializer):
    # author=serializers.StringRelatedField(read_only=True)
    created_at=serializers.SerializerMethodField(read_only = False)
    # user_has_reported=serializers.SerializerMethodField(read_only=True)

    # reports=serializers.StringRelatedField(many=True)

    class Meta:
        model=Report
        # fields = ('description','records','traffic_police','created_at')
        exclude =["records","traffic_police"]
        

    def get_created_at(self,instance):
        return instance.created_at.strftime("%B %d %Y")

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=TrafficPolice
        fields =('phone_number',)

class UserSerializer(serializers.ModelSerializer):
    traffic_police = ProfileSerializer(required = True)

    class Meta:
        model = User
        fields =('id','username','email','password','first_name','last_name','traffic_police')


    def update(self, instance, validated_data):
        instance.username = validated_data.get('username',instance.username)
        instance.email = validated_data.get('email',instance.email)
        instance.first_name = validated_data.get('first_name',instance.first_name)
        instance.last_name = validated_data.get('last_name',instance.last_name)
        instance.username = validated_data.get('username',instance.username)
        instance.username = validated_data.get('username',instance.username)
        # traffic_police = TrafficPolice.objects.get(user = instance)
        # print(traffic_police.phone_number)
                
        # instance.set_password(validated_data['password'])
        instance.save()
        # traffic_polices = validated_data.pop('traffic_police')
        # phone_number = list(traffic_polices.items())
        # traffic_police.phone_number = phone_number[0][1]

        # traffic_police.save(update_fields=['phone_number'])
        # print(phone_number[0][1])
        # print(traffic_polices)       

        return instance


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
      Serializer for password change endpoint.

    """
    old_password = serializers.CharField(required = True)
    new_password = serializers.CharField(required = True)
    

class VehicleTrackerSerializer(serializers.Serializer):
    pk = serializers.ReadOnlyField()
    records = serializers.CharField(max_length=15)
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6)


    def create(self,validated_data):
        # vehicle = Vehicle.objects.filter(vehicle_plate__iexact = validated_data['vehicle'])
        record = Records.objects.get(id = validated_data['records'])
        obj=VehicleTracker.objects.create(records=record,latitude = validated_data['latitude'],longitude = validated_data['longitude'])
        return obj

