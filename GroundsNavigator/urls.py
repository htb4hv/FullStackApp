"""
URL configuration for GroundsNavigator project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from locations.views import save_location
from allauth.account.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth.models import Group
from allauth.socialaccount.models import SocialAccount
from .views import saved_view

@receiver(user_logged_in)
def user_logged_in_(request, user, **kwargs):
    social_account = SocialAccount.objects.get(user=user)
    email = social_account.extra_data.get('email')

    SITE_ADMIN_EMAILS = ['htb4hv@virginia.edu', 'pfa3qy@virginia.edu', 'cgm7vq@virginia.edu', 'mzg7fh@virginia.edu', 'sco9cdq@virginia.edu', 'seandwsy@vt.edu', 'cs3240.super@gmail.com']

    if email in SITE_ADMIN_EMAILS:
        # Add user to Admin group
        admin_group, created = Group.objects.get_or_create(name='Site_Admin')
        user.groups.add(admin_group)
    else:
        print(f"{email} is NOT admin")


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', views.profile_view, name='profile'),
    path('accounts/login/', views.login_view, name='account_login'),
    path('restrooms/', views.restroom_view, name='restrooms'),
    path('parking/', views.parking_view, name='parking'),
    path('study/', views.study_view, name='study'),
    path('', views.home, name='home'),
    path('', include('locations.urls')),
    path('locations/', save_location, name='save_location'),
    path('saved/', saved_view, name='saved'),
]
