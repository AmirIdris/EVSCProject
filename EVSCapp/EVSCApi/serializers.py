from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from EVSCapp import models
from EVSCapp.models import Notification, Report,Vehicle,TrafficPolice,Records
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


# class RecordSerializer(serializers.ModelSerializer):
#     status = serializers.ReadOnlyField()
#     class Meta:
#         model=Records
#         fields=['id','vehicle','latitude','longitude','vehicle_speed','address','status']

class RecordSerializer(serializers.Serializer):
    pk = serializers.ReadOnlyField()
    vehicle = serializers.CharField(max_length=15)
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    vehicle_speed = serializers.IntegerField()
    status = serializers.BooleanField(read_only=True)
    address = serializers.CharField(max_length = 50)
    created_at=serializers.SerializerMethodField(read_only=True)

    def create(self,validated_data):
        # vehicle = Vehicle.objects.filter(vehicle_plate__iexact = validated_data['vehicle'])
        vehicle = Vehicle.objects.get(vehicle_plate = validated_data['vehicle'])
        obj=Records.objects.create(address = validated_data['address'],vehicle_speed=validated_data['vehicle_speed'],vehicle=vehicle,latitude = validated_data['latitude'],longitude = validated_data['longitude'],duration = timezone.now())
        return obj

    def get_created_at(self,instance):
        return instance.created_at.strftime("%B %d %Y")

# class RecordSerializer(serializers.ModelSerializer):
#     created_at=serializers.SerializerMethodField(read_only=True)
#     latitude = serializers.CharField()
#     longitude = serializers.CharField()
#     # vehicle_plate = serializers.CharField(source = "vehicle.vehicle_plate")
#     # location=PointField()
#     class Meta:
#         model=Records
#         exclude=['duration','status']


#     def create(self,validated_data):
        
        
#         obj=Records.objects.create(address = validated_data['address'],vehicle_speed=validated_data['vehicle_speed'],vehicle=validated_data['vehicle'],latitude = validated_data['latitude'],longitude = validated_data['longitude'])
#         return obj

#     def get_created_at(self,instance):
#         return instance.created_at.strftime("%B %d %Y")

# class ReportSerializer(serializers.ModelSerializer):
    
#     created_at=serializers.SerializerMethodField(read_only=True)


#     class Meta:
#         model = Report
#         exclude = ["records","traffic_police"]

#     def get_created_at(self,instance):
#         return instance.created_at.strftime("%B %d %Y")

#     def get_traffic_police_has_reported(self,instance):
#         request = self.context.get("request")
#         return instance.traffic_police.filter(pk=request.user.pk).exists()

#     def create(self, validated_data):
#         return Report.objects.create(**validated_data)




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


class UserSerializer(serializers.ModelSerializer):
    # id = serializers.ReadOnlyField()
    # username = serializers.CharField(max_length=50)
    # email = serializers.EmailField()
    # first_name = serializers.CharField(max_length=50)
    # last_name = serializers.CharField(max_length=50)
    
    class Meta:
        model = User
        fields = ('id','username','email','password','first_name','last_name')



    # def update(self, instance, validated_data):
    #     request = self.context.get('request',None)
    #     traffic_police = get_object_or_404(TrafficPolice, user_id = request.user.id)
    #     print(validated_data.get('username', instance.username))
    #     instance.username = validated_data.get('username', instance.username)
    #     instance.password = validated_data.get('password', instance.password)
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.first_name = validated_data.get('first_name', instance.first_name)
    #     instance.last_name = validated_data.get('last_name', instance.last_name)
    
    #     return instance




# class RecordSerializer(serializers.Serializer):
#     # records=serializers.SerializerMethodField(read_only=False)
#     id = ReadOnlyField()
#     recipient = ReadOnlyField(source = "traffic_police_notification.recipient")
#     records = ReadOnlyField(source = "record_notification.vehicle.plate_number")




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

    # def get_user_has_reported(self,instance):
    #     request=self.context.get("request")

    #     return instance.traffic_police.filter(pk=request.user.pk).exists()

    # def create(self,validated_data):
    #     reports_record=RecordSerializer.create(RecordSerializer(),validated_data)
    #     reports,created=Records.objects.create(records=reports_record)
    #     return reports


# class MobileDeviceSerializer(serializers.ModelSerializer):
#     """Serializer For MobileDevice Identification"""
#     class Meta:
#         model=MobileDevices
#         fields=('participants','token')


#     def create(self,validated_data):
#         """ Creating MobileDeice instances """
#         return MobileDevices.objects.create(**validated_data)

