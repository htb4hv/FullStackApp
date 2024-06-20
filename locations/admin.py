from django.contrib import admin
from .models import Location
from .models import Review

admin.site.register(Location)
admin.site.register(Review)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['TITLE', 'TYPE', 'OPENTIME', 'CLOSETIME', 'DESCRIPTION', 'APPROVED']
    list_editable = ['APPROVED']
# Register your models here.
