from django.db import router
from django.urls import path
from django.urls.conf import include
from EVSCapp.EVSCApi.views import (RecordDetailAPIView,
                                    LisVehicle,
                                    VehicleDetailAPIView,
                                    ReportRUDAPIView,
                                    UpdateFcmTokenApiView, 
                                    ListFcmTokenDevices,
                                    # fcm_token_detail
                                    ListReport,
                                    MyProfileLoadAPIView,
                                    ListUser,
                                    ListUserDetail,
                                    RecordViewSet,
                                    # RecordList,
                                    list_records

                                   
                                    )

from rest_framework.routers import DefaultRouter
from EVSCapp.EVSCApi import views as qv


router=DefaultRouter()
router.register("records",qv.RecordViewSet)
# router.register('devices', FCMDeviceAuthorizedViewSet)


urlpatterns = [
    # path("",include(router.urls)),
    path("",include(router.urls)),
    path('rest-auth/',include("rest_auth.urls")),
    path('records/',list_records,name='list-rcords'),
    path('records/<int:pk>/',RecordDetailAPIView.as_view(),name='list-detail'),
    path("records/<int:pk>/report/", qv.ReportCreateAPiView.as_view(),name='create-report'),
    path('vehicles/',LisVehicle.as_view(),name='list-vehicle'),
    path('vehicles/<int:pk>/',VehicleDetailAPIView.as_view(),name='vehicle-detail'),
    path('reports/',ListReport.as_view(),name='report-list'),
    path('reports/<int:pk>',ReportRUDAPIView.as_view(),name='report-detail'),
    path('devices/',ListFcmTokenDevices.as_view(),name='list-device-token'),
    path('devices/<int:user>/',UpdateFcmTokenApiView.as_view(),name='create-device-token'),
    path('user-profile/',MyProfileLoadAPIView.as_view(),name ='retriev-user-profile'),
    path('users/',ListUser.as_view(), name ='users'),
    path('users/<int:pk>',ListUserDetail.as_view(), name = 'user-detail')
    # path('devices/<int:pk>',fcm_token_detail,name='create-device-token')
    # path('records/<int:pk>/report',ReportCreateAPiView.as_view(),name='create-record')
    
]
