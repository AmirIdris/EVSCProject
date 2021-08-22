from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from numpy import record
# from TrafficReport.api.serializes import ReportSerializer
from EVSCapp.models import Notification, Report,TrafficPolice,Vehicle,Records
from rest_framework import generics, serializers,viewsets,status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from EVSCapp.EVSCApi.serializers import (VehicleSerializer,
                                          RecordSerializer,
                                          ReportSerializer,
                                          FcmDevicesSerializer,
                                          UserProfileSerializer,
                                          UserSerializer,
                                          NotificationSerializer)

from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework.decorators import api_view

from django.views.decorators.csrf import csrf_exempt, csrf_protect,ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User

from EVSCapp import permissions

from rest_framework.decorators import api_view
 

# List Available records .
class ListRecordAPiView(viewsets.ModelViewSet):
    queryset=Records.objects.all()
    serializer_class=RecordSerializer

class ListReport(generics.ListAPIView):
    queryset= Report.objects.all()
    serializer_class=ReportSerializer
# List all available records
# class RecordList(APIView):
#     # queryset = Records.objects.all()
#     # serializer_class = RecordSerializer

#     def get(self,request, format = None):
#         records = Records.objects.all()
#         serializer = RecordSerializer(records, many = True)
#         return Response(serializer.data)

# @api_view(['GET','POST'])
# def list_records(request):
#     if request.method == 'GET':
#         records = Records.objects.all()
#         serializer = RecordSerializer(records, many = True)
#         return Response(serializer.data)




class RecordList(generics.ListCreateAPIView):
    """Create Records"""
    queryset = Records.objects.all()
    serializer_class = RecordSerializer

    def get_queryset(self):
        record = get_object_or_404(Records,status = False)
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






# List User Detail View 
# class ListDetailRecordAPiView(generics.RetrieveAPIView):
#     queryset=Records.objects.all()
#     lookup_field = "slug"
#     serializer_class=RecordSerializer
    

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
    
class ReportCreateAPiView(generics.ListCreateAPIView):
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


# class ReportCreateAPiView(APIView):
#     serializer_class = RecordSerializer
#     def get_queryset(self):
#         queryset = Records.objects.all()
#         return queryset

#     def get(self,request, *args,**kwagrs):
#         try:    
#             id = self.kwargs.get("pk")
#             print(id)
#             if id != None:
#                 record=Records.objects.get(pk=id)
#                 serializer = RecordSerializer(record)
                
#         except:
#             records = self.get_queryset()
#             print(records)
#             serializer = RecordSerializer(records,many=True)
#             return Response(serializer.data)  

        
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
    queryset= User.objects.all()
    serializer_class=UserSerializer

class ListUserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer


class ListNotification(generics.ListAPIView):
    queryset=Notification.objects.all()
    serializer_class=NotificationSerializer


 


    
# @api_view(['GET', 'PUT'])
# def fcm_token_detail(request,pk):
#     try:
#         fcm_token = TrafficPolice.objects.get(pk = pk)
#     except TrafficPolice.DoesNotExist:
#           return JsonResponse({'message': 'The token does not exist'}, status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         fcm_token_detail_serializer =  FcmDevicesSerializer(fcm_token)  
#         return JsonResponse(fcm_token_detail_serializer.data)
#     elif request.method ==  'PUT':
#         fcm_token_data = JSONParser().parse(request)
#         fcm_token_detail_serializer = FcmDevicesSerializer(fcm_token, data = fcm_token_data, partial = True)

#         if fcm_token_detail_serializer.is_valid():
#             fcm_token_detail_serializer.save()
#             return JsonResponse(fcm_token_detail_serializer.data)
#         return JsonResponse(fcm_token_detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        





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





# Store Deices Fcm token in the database

# class CreateFcmToken(APIView):
#     def post(self,request,format = None):
#         serializer = FcmDevicesSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status = status.HTTP_201_CREATED)
#         return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

# class CreateFcmTokenAPIView(generics.CreateAPIView):
#     """
#      Create New Fcm Token
#     """
#     queryset=TrafficPolice.objects.all()
#     serializer_class=FcmDevicesSerializer

#     def perform_update(self,serializer):
#         if serializer.is_valid():
#             user=serializer.validated_data['user']
#             fcm_token=serializer.validated_data['fcm_token']

#             if TrafficPolice.objects.filter(user = user,fcm_token = fcm_token).exists():
#                 raise ValidationError("Token is Already created and associated to the corresponding user")
#             else:
#                 serializer.save(user = user,fcm_token = fcm_token)


# class UpdateFcmTokenApiView(generics.RetrieveUpdateAPIView):
#     queryset=TrafficPolice.objects.all()
#     serializer_class = FcmDevicesSerializer
#     lookup_field = 'pk'


#     def get_object(self,pk):
#         return TrafficPolice.objects.get(pk = pk)

#     def patch(self, request, pk):
#         traffic_police_object=self.get_object(pk)
#         serializer=FcmDevicesSerializer(traffic_police_object,data = request.data, partial = True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response("{'message':'instance is updated successfully'}")
#         return Response("{'message': 'instance is not updated'}")





    # def update(self, request, *args ,**kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data = request.data, partial = True)

    #     user = data['user']
        
    #     traffic_police = TrafficPolice.objects.filter(user = user)

    #     if traffic_police.exists():
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response("{ 'message' : 'fcm_token is updated successfully'}")

    #         else:
    #             return Response("{'message':'something went wrong'}")

    #     else:
    #         return Response("{'message':'No user found'}")


        
