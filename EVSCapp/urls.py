from django.urls import path,include
urlpatterns = [
    path('api/rest-auth/',include("rest_auth.urls")),
    
]