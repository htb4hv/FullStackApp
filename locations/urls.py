from django.urls import path
from . import views

urlpatterns = [
    path('save_location/', views.save_location, name='save_location'),
    path('get_parking_locations/', views.get_parking_locations, name='get_parking_locations'),
    path('get_restroom_locations/', views.get_restroom_locations, name='get_restroom_locations'),
    path('get_study_locations/', views.get_study_locations, name='get_study_locations'),
    path('get_location/', views.get_location, name='get_all_locations'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard_url'),
    path('notifications/', views.display_notification, name='notification_url'),
    path('location_detail/<int:location_id>/', views.location_detail, name='location_detail'),
    path('location/<int:location_id>/submit_review/', views.submit_review, name='submit_review'),
]
