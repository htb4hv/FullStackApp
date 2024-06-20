from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Location, Review, create_notification, Notification
from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Avg
from django.core.serializers import serialize


# Create your views here.
@login_required
def save_location(request):
    if request.method == 'POST':
        latlong = request.POST.get('latlong')
        title = request.POST.get('title')
        opentime = request.POST.get('opentime')
        closetime = request.POST.get('closetime')
        type = request.POST.get('type')
        description = request.POST.get('description')

        Location.objects.create(LATLONG=latlong, TITLE=title, OPENTIME=opentime, CLOSETIME=closetime, TYPE=type, DESCRIPTION=description, APPROVED=False, DENIED=False, submitted_by=request.user)
        return JsonResponse({'message': 'Location saved successfully'})

    return JsonResponse({'message': 'Method not allowed'}, status=405)  # 405 is for Method Not Allowed


def get_location(request):
    # locations = Location.objects.filter(APPROVED=True).values('id','LATLONG', 'TITLE', 'TYPE', 'DESCRIPTION')


    locations = Location.objects.filter(APPROVED=True).values('id','LATLONG', 'OPENTIME', 'CLOSETIME', 'TITLE', 'TYPE', 'DESCRIPTION')
    location_list = list(locations)

    for loc in location_list:
        lat, lng = map(float, loc['LATLONG'].split(','))
        loc['latitude'] = lat
        loc['longitude'] = lng
        del loc['LATLONG']

    return JsonResponse({'locations': location_list}, safe=False)

def get_restroom_locations(request):
    locations = Location.objects.filter(APPROVED=True, TYPE='restroom').values('id','LATLONG', 'TITLE', 'TYPE', 'DESCRIPTION')
    # locations = Location.objects.filter(APPROVED=True).values('id','LATLONG', 'OPENTIME', 'CLOSETIME', 'TITLE', 'TYPE', 'DESCRIPTION')
    location_list = list(locations)

    for loc in location_list:
        lat, lng = map(float, loc['LATLONG'].split(','))
        loc['latitude'] = lat
        loc['longitude'] = lng
        del loc['LATLONG']

    return JsonResponse(location_list, safe=False)

def get_parking_locations(request):
    locations = Location.objects.filter(APPROVED=True, TYPE='parking').values('id', 'LATLONG', 'TITLE', 'TYPE',
                                                                               'DESCRIPTION')
    # locations = Location.objects.filter(APPROVED=True).values('id','LATLONG', 'OPENTIME', 'CLOSETIME', 'TITLE', 'TYPE', 'DESCRIPTION')
    location_list = list(locations)

    for loc in location_list:
        lat, lng = map(float, loc['LATLONG'].split(','))
        loc['latitude'] = lat
        loc['longitude'] = lng
        del loc['LATLONG']

    return JsonResponse(location_list, safe=False)

def get_study_locations(request):
    locations = Location.objects.filter(APPROVED=True, TYPE='study').values('id','LATLONG', 'TITLE', 'TYPE', 'DESCRIPTION')
    # locations = Location.objects.filter(APPROVED=True).values('id','LATLONG', 'OPENTIME', 'CLOSETIME', 'TITLE', 'TYPE', 'DESCRIPTION')
    location_list = list(locations)

    for loc in location_list:
        lat, lng = map(float, loc['LATLONG'].split(','))
        loc['latitude'] = lat
        loc['longitude'] = lng
        del loc['LATLONG']

    return JsonResponse(location_list, safe=False)


def admin_dashboard(request):
    unapproved_locations = Location.objects.filter(APPROVED=False, DENIED=False)

    if request.method == 'POST':
        if 'approve_location' in request.POST:
            location_id = request.POST.get('approve_location')
            location = Location.objects.get(pk=location_id)
            location.APPROVED = True
            location.save()

        elif 'reject_location' in request.POST:
            location_id = request.POST.get('reject_location')
            location = Location.objects.get(pk=location_id)
            #location.delete()  # Delete the location or handle rejection logic here
            location.DENIED = True
            create_notification(location.submitted_by, f"Your location submission '{location.TITLE}' has been denied.")
            location.delete()

        return redirect('admin_dashboard_url')


    return render(request, 'siteadmin.html', {'locations': unapproved_locations})

@login_required
def location_detail(request, location_id):
    location = get_object_or_404(Location, pk=location_id)
    reviews = location.reviews.all()

    # Calculate average rating
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    full_stars = int(average_rating)
    half_star = average_rating - full_stars >= 0.5
    empty_stars = 5 - full_stars - (1 if half_star else 0)

    # Convert integers to ranges
    full_stars_range = range(full_stars)
    empty_stars_range = range(empty_stars)

    context = {
        'location': location,
        'reviews': reviews,
        'average_rating': average_rating,
        'full_stars': full_stars_range,
        'half_star': half_star,
        'empty_stars': empty_stars_range
    }
    return render(request, 'location_detail.html', context)

@login_required()
def display_notification(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user, is_read=False)
    else:
        notifications = []

    return render(request, 'notifications.html', {'notifications': notifications})


@login_required
def submit_review(request, location_id):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        review_text = request.POST.get('review_text')
        location = get_object_or_404(Location, pk=location_id)

        Review.objects.create(
            location=location,
            user=request.user,
            rating=rating,
            review_text=review_text
        )
        return redirect('location_detail', location_id=location_id)


