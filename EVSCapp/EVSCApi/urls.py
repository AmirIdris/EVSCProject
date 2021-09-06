from django.db import router
from django.urls import path,include,re_path
from django.urls.conf import include
from EVSCapp.EVSCApi.views import (RecordDetailAPIView,
                                    LisVehicle,
                                    VehicleDetailAPIView,
                                    ReportRUDAPIView,
                                    UpdateFcmTokenApiView, 
                                    ListFcmTokenDevices,
                                    ListReport,
                                    MyProfileLoadAPIView,
                                    ListUser,
                                    ListUserDetail,
                                    RecordViewSet,
                                    ListNotification,
                                    RecordList,
                                    ChangePasswordView,
                                    VehicleTrackerView,
                                    VehicleStatusUpdateView

                                   
                                    )

from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views
from EVSCapp.EVSCApi import views as qv
from django.urls import reverse_lazy


router=DefaultRouter()
router.register("records",qv.RecordViewSet)



urlpatterns = [

    path("",include(router.urls)),
    path('rest-auth/',include("rest_auth.urls")),
    

    path('records/',RecordList.as_view(),name = 'list-records'),
    path('records/<int:pk>/',RecordDetailAPIView.as_view(),name='list-detail'),
    path("records/<int:pk>/report/", qv.ReportCreateAPiView.as_view(),name='create-report'),
    path('vehicles/',LisVehicle.as_view(),name='list-vehicle'),
    path('vehicles/<int:pk>/',VehicleDetailAPIView.as_view(),name='vehicle-detail'),
    path('reports/',ListReport.as_view(),name='report-list'),
    path('reports/<int:pk>',ReportRUDAPIView.as_view(),name='report-detail'),
    path('devices/',ListFcmTokenDevices.as_view(),name='list-device-token'),
    path('devices/<int:user>/',UpdateFcmTokenApiView.as_view(),name='create-device-token'),
    path('user-profile/',MyProfileLoadAPIView.as_view(),name ='retriev-user-profile'),
    path('user/',ListUser.as_view(), name ='users'),
    path('users/<int:pk>',ListUserDetail.as_view(), name = 'user-detail'),
    path('change-password/',ChangePasswordView.as_view(),name = 'change-password'),
    path('notifications/',ListNotification.as_view(),name='notifications'),
    path('track-vehicles/',VehicleTrackerView.as_view(),name = 'track-vehicles'),
    path('update-status/',VehicleStatusUpdateView.as_view(),name = 'update-status')

    
]
