from EVSCapp.models import Report,Vehicle,TrafficPolice,Records
from django.conf import settings
from django.db.models import fields
from rest_auth.models import TokenModel
from rest_auth.utils import import_callable
from rest_auth.serializers import UserDetailsSerializer as DefaultUserDetailsSerializer
from rest_framework import serializers
from rest_framework.fields import Field,ReadOnlyField,DecimalField








class VehicleSerializer(serializers.ModelSerializer):

    class Meta:
        model=Vehicle
        fields = "__all__"


# class RecordSerializer(serializers.ModelSerializer):
#     vehicle=VehicleSerializer(read_only=True)

#     class Meta:
#         model=Records
#         fields=['vehicle','location','vehicle_speed','duration']

class RecordSerializer(serializers.ModelSerializer):
    created_at=serializers.SerializerMethodField(read_only=True)
    latitude = serializers.CharField()
    longitude = serializers.CharField()
    # location=PointField()
    class Meta:
        model=Records
        exclude=['duration','location','status']


    def create(self,validated_data):
        latitude = validated_data['latitude']
        longitude = validated_data['longitude']
        location = Point(float(latitude), float(longitude),srid=4326)
        obj=Records.objects.create(address = validated_data['address'],vehicle_speed=validated_data['vehicle_speed'],vehicle=validated_data['vehicle'])
        obj.save(location = location)
        return obj

    def get_created_at(self,instance):
        return instance.created_at.strftime("%B %d %Y")

class ReportSerializer(serializers.ModelSerializer):
    
    created_at=serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = Report
        exclude = ["records","traffic_police"]

    def get_created_at(self,instance):
        return instance.created_at.strftime("%B %d %Y")

    def get_traffic_police_has_reported(self,instance):
        request = self.context.get("request")
        return instance.traffic_police.filter(pk=request.user.pk).exists()

    def create(self, validated_data):
        return Report.objects.create(**validated_data)




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


class UserSerializer(serializers.Serializer):
    id = ReadOnlyField()
    username = ReadOnlyField()
    email = ReadOnlyField()
    first_name = ReadOnlyField()
    last_name = ReadOnlyField()
    phone_number = ReadOnlyField(source = "traffic_police.phone_number")
    latitude = DecimalField(source = "traffic_police.user.latitude", max_digits=9, decimal_places=6)
    longitude = DecimalField(source = "traffic_police.user.longitude", max_digits=9, decimal_places=6)



class RecordSerializer(serializers.ModelSerializer):
    records=serializers.SerializerMethodField(read_only=False)
    created_at=serializers.SerializerMethodField()
    class Meta:
        model=Records
        fields="__all__"
    def get_created_at(self,instance):
        return instance.created_at.strftime("%B %d %Y")

    
    




class ReportSerializer(serializers.ModelSerializer):
    # author=serializers.StringRelatedField(read_only=True)
    # created_at=serializers.SerializerMethodField(read_only = False)
    # user_has_reported=serializers.SerializerMethodField(read_only=True)

    # reports=serializers.StringRelatedField(many=True)

    class Meta:
        model=Report
        fields = ('description','records','traffic_police','created_at')
        

    # def get_created_at(self,instance):
    #     return instance.created_at.strftime("%B %d %Y")

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

