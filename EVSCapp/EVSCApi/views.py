from functools import partial
from django.core.exceptions import ValidationError
from django.http import request
from django.shortcuts import get_object_or_404
from numpy import record
from numpy.core import records
from rest_framework import response
# from TrafficReport.api.serializes import ReportSerializer
from EVSCapp.models import Notification, Report,TrafficPolice,Vehicle,Records,VehicleTracker
from rest_framework import generics, serializers,viewsets,status
from rest_framework.generics import UpdateAPIView, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from EVSCapp.EVSCApi.serializers import (ChangePasswordSerializer, VehicleSerializer,
                                          RecordSerializer,
                                          ReportSerializer,
                                          FcmDevicesSerializer,
                                          UserProfileSerializer,
                                          UserSerializer,
                                          NotificationSerializer,
                                          VehicleTrackerSerializer)

from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework.decorators import api_view

from django.views.decorators.csrf import csrf_exempt, csrf_protect,ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User

from EVSCapp import permissions
from django.db.models import Q

from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated


 

# List Available records .
class ListRecordAPiView(viewsets.ModelViewSet):
    queryset=Records.objects.all()
    serializer_class=RecordSerializer

class ListReport(generics.ListAPIView):
    queryset= Report.objects.all()
    serializer_class=ReportSerializer


# list record and create new records 
class RecordList(generics.ListCreateAPIView):
    """Create Records"""
    # retrive all records
    queryset = Records.objects.all()
    # change the format to Json
    serializer_class = RecordSerializer

    def get_queryset(self):
        if get_object_or_404(Records,status = True):
            return Records.objects.filter(status=False).order_by("-created_at")

    def perform_create(self, serializer):
        vehicle_plate = serializer.data['vehicle']
        latitude = serializer.data['latitude']
        longitude = serializer.data['longitude']
        vehicle_speed = serializer.data['vehicle_speed']
        address = serializer.data['address']
        print(vehicle_plate)
        print(latitude)
        vehicle = Vehicle.objects.get(vehicle_plate = vehicle_plate)
        print(vehicle)

        serializer.save(vehicle = vehicle.id, latitude = latitude,longitude = longitude,vehicle_speed=vehicle_speed,address=address)



class RecordViewSet(viewsets.ModelViewSet):
    queryset=Records.objects.all()
    lookup_field = "pk"
    serializer_class=RecordSerializer

    def perform_create(self, serializer):
        return serializer.save()


class LisVehicle(generics.ListAPIView):
    queryset= Vehicle.objects.all()
    serializer_class=VehicleSerializer


class VehicleDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Vehicle.objects.all()
    serializer_class=VehicleSerializer
    


class RecordDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Report.objects.all()
    serializer_class=RecordSerializer
    
class ReportCreateAPiView(generics.CreateAPIView):
    queryset=Report.objects.all()
    serializer_class=ReportSerializer

    def perform_create(self, serializer):
        reported_by=self.request.user
        print(reported_by)
        kwarg_pk=self.kwargs.get("pk")
        print(kwarg_pk)
        record=get_object_or_404(Records,pk=kwarg_pk)
        print(record)
        print(reported_by.id)
        traffic_police = TrafficPolice.objects.get(user_id = reported_by.id)
        if Report.objects.filter(traffic_police=traffic_police,records=record).exists():
            raise ValidationError("You have already reported")

        elif Report.objects.filter(records = record).exists():
            raise ValidationError("Record is already reported")

        else:
            if record.status == False and record.id == record.id:
                record.status=True
                record.save(update_fields=['status'])
            

            
            
            print(record.status) 
            serializer.save(records=record,traffic_police=traffic_police)


        
class ReportRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Report.objects.all()
    serializer_class=ReportSerializer


class ListFcmTokenDevices(generics.ListAPIView):
    queryset = TrafficPolice.objects.all()
    serializer_class = FcmDevicesSerializer


class MyProfileLoadAPIView(APIView):
    def get(self,request,format = None):
        user = self.request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

class ListUser(generics.ListAPIView):
    serializer_class=UserSerializer

    def get_queryset(self):
        if get_object_or_404(User,pk = self.request.user.pk):
            return User.objects.filter(Q(username__iexact=self.request.user.username))


class ListUserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer


    def put(self, request, *args, **kwargs):
        user = request.user
        serializer =UserSerializer(user, data = request.data,partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListNotification(generics.ListAPIView):
    serializer_class=NotificationSerializer
    def get_queryset(self):
        user = self.request.user
        
        print(user)
        return Notification.objects.filter(records__status = False,recipient__user=user)

        


        





class UpdateFcmTokenApiView(generics.RetrieveUpdateAPIView):
    queryset = TrafficPolice.objects.all()
    serializer_class = FcmDevicesSerializer
    lookup_field = 'user'
    permission_classes = [permissions.IsOwnerOrReadOnly]
    # @method_decorator(ensure_csrf_cookie)
    def patch(self, request, **kwargs):
        pk = self.kwargs.get('pk')

        traffic_police_object = TrafficPolice.objects.get(pk)
        serializer=FcmDevicesSerializer(traffic_police_object,data = request.data, partial = True)
        print(serializer.data['fcm_token'])
        if serializer.is_valid():
            serializer.save()

            return Response("{'message':'instance is saved successfully'}")

        return Response("{'message':'something wrong'}")

# password update Api logic resides in this method        
class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self,queryset = None):
        obj = self.request.user
        return obj

    def update(self,request,*args,**kwargs):

        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
                # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message':'password is updated successfully!',
                'data':[]
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
class VehicleTrackerView(generics.ListCreateAPIView):
    """Create Records"""
    # retrive all records
    queryset = VehicleTracker.objects.all()
    # change the format to Json
    serializer_class = VehicleTrackerSerializer

    # def get_queryset(self):
    #     if get_object_or_404(Records,status = True):
    #         return Records.objects.filter(status=False).order_by("-created_at")

    def perform_create(self, serializer):
        record_id = serializer.validated_data.get('records')
        latitude = serializer.validated_data.get('latitude')
        longitude = serializer.validated_data.get('longitude')

        print(record_id)
        print(latitude)
        record = Records.objects.get(pk = record_id)
        print(record)

        serializer.save(records = record.id, latitude = latitude,longitude = longitude)
