from django.urls import path,include,re_path
from django.urls.resolvers import URLPattern
from pages.views import (index,
                        SignUpPageView,
                        pages,
                        manage_vehicle,
                        manage_traffic_police,
                        manage_system_admin,
                        add_vehicle,
                        add_vehicle_save,
                        edit_vehicle,
                        edit_vehicle_save,
                        delete_vehicle,
                        admin_profile,
                        admin_profile_update,
                        add_traffic_police,
                        add_user,
                        add_user_save,
                        detail_info_view,
                        records_view,
                        search_all_traffic_police,
                        SearchResultsView,
                        edit_traffic_police,
                        delete_traffic_police,
                        edit_traffic_police_save

                        )

urlpatterns = [
    
    path('',index,name='home'),
    path('signup/', SignUpPageView.as_view(), name = 'register'),

    #vehicle related urls
    path('manage_vehicle/',manage_vehicle, name = 'manage_vehicle'),
    path('add_vehicle/',add_vehicle, name = 'add_vehicle'),
    path('add_vehicle_save',add_vehicle_save, name = 'add_vehicle_save'),
    path('edit_vehicle/<vehicle_id>',edit_vehicle, name = 'edit_vehicle'),
    path('edit_vehicle_save/', edit_vehicle_save, name = 'edit_vehicle_save'),
    path('delete_vehicle/<vehicle_id>', delete_vehicle, name = 'delete_vehicle'),
    # traffic related urls
    path('manage_traffic_police/',manage_traffic_police, name = 'manage_traffic_police'),
    path('add_traffic_police', add_traffic_police, name = 'add_traffic_police'),
    path('more_traffic_info/<traffic_id>/', detail_info_view, name = 'detail_info'),
    path('search_traffic',search_all_traffic_police, name = 'search_traffic_police'),
    path('edit_traffic_police/<traffic_police_id>',edit_traffic_police, name = 'edit_traffic_police'),
    path('edit_traffic_police_save', edit_traffic_police_save, name = 'edit_traffic_police_save'),
    path('delete_traffic_police/<traffic_police_id>',delete_traffic_police, name = 'delete_traffic_police'),

    # admin related urls
    path('manage_system_admin/',manage_system_admin, name = 'manage_system_admin'),
    path('admin_profile', admin_profile, name = 'admin_profile'),
    path('admin_profile_update', admin_profile_update, name = 'admin_profile_update'),
    
    path('add_user/',add_user, name = 'add_user'),
    path('add_user_save', add_user_save, name = 'add_user_save'),
    
    #record related urls
    path('view_records/',records_view, name = 'view_records'),

    # pages urls
    re_path(r'^.*\.*', pages, name='pages'),

    
]