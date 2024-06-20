from django.shortcuts import render, redirect
from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib import messages


def profile_view(request):
    user = request.user

    # Check if user is authenticated
    if user.is_authenticated:

        # Check if the user is in the Admin group
        if user.groups.filter(name='Site_Admin').exists():
            # If user is admin, redirect to admin portion of the application.
            return redirect('admin_dashboard_url')  # replace with the actual URL name or render admin template

        else:
            # If user is not admin, continue with extracting social information and render the default user page.
            social_info = SocialAccount.objects.get(user=user)
            additional_data = social_info.extra_data

            first_name = additional_data['given_name']
            last_name = additional_data['family_name']
            username = user.username

            context = {
                'first_name': first_name,
                'last_name': last_name,
                'username': username
            }

            # Render the regular profile template

            google_maps_api_key = settings.GOOGLE_MAPS_API_KEY

            return render(request, 'home.html', {'google_maps_api_key': google_maps_api_key, 'context':context})


    else:
        # If user is not authenticated, redirect to login page
        return redirect('account_login')  # or your preferrepd login URL


def home(request):
    user = request.user
    is_site_admin = user.groups.filter(name='Site_Admin').exists()
    google_maps_api_key = settings.GOOGLE_MAPS_API_KEY
    return render(request, 'home.html', {'google_maps_api_key': google_maps_api_key, 'is_site_admin':is_site_admin})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['login']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials. Please try again.')
    return render(request, 'account/login.html')

def restroom_view(request):
    google_maps_api_key = settings.GOOGLE_MAPS_API_KEY
    return render(request, 'restroom_map.html', {'google_maps_api_key': google_maps_api_key})

def parking_view(request):
    google_maps_api_key = settings.GOOGLE_MAPS_API_KEY
    return render(request, 'parking_map.html', {'google_maps_api_key': google_maps_api_key})

def study_view(request):
    google_maps_api_key = settings.GOOGLE_MAPS_API_KEY
    return render(request, 'study_map.html', {'google_maps_api_key': google_maps_api_key})

def saved_view(request):
    return render(request, 'saved_locations.html')