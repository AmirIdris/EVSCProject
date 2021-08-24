from django.db import router
from django.urls import path,include,re_path
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
                                    # list_records,
                                    ListNotification,
                                    RecordList,
                                    ChangePasswordView

                                   
                                    )

from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views
from EVSCapp.EVSCApi import views as qv
from django.urls import reverse_lazy


router=DefaultRouter()
router.register("records",qv.RecordViewSet)
# router.register('devices', FCMDeviceAuthorizedViewSet)


urlpatterns = [
    # path("",include(router.urls)),
    path("",include(router.urls)),
    path('rest-auth/',include("rest_auth.urls")),
    
    # path('records/',list_records,name='list-rcords'),
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
    # path('reset-password/',auth_views.PasswordResetView.as_view(success_url=reverse_lazy('password_reset_done')), name='reset_password'),
    # path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    # path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    # path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('password_reset_complete')),name='password_reset_confirm')
    # path('devices/<int:pk>',fcm_token_detail,name='create-device-token')
    # path('records/<int:pk>/report',ReportCreateAPiView.as_view(),name='create-record')
    
]
