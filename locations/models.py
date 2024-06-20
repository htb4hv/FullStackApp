from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone

class Location(models.Model):
    LATLONG = models.CharField(max_length=100)
    TITLE = models.CharField(max_length=200)
    OPENTIME = models.CharField(max_length=200, null=True, blank=True, default=None)
    CLOSETIME = models.CharField(max_length=200, null=True, blank=True, default=None)
    TYPE_CHOICES = [
        ('restroom', 'Restroom'),
        ('parking', 'Parking Spot'),
        ('study', 'Study Spot')
    ]
    TYPE = models.CharField(max_length=10, choices=TYPE_CHOICES)
    DESCRIPTION = models.TextField()
    APPROVED = models.BooleanField(default=False)
    DENIED = models.BooleanField(default=False)
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review_text = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='reviews')
    created_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"Review by {self.user.username} on {self.location}"


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)


def create_notification(user, message):
    Notification.objects.create(user=user, message=message)