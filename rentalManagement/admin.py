from django.contrib import admin
from .models import (City,State,UserDetails,VehicleDetails,VehicleTypes
,VehicleBrands,RentalRequests,Rentals)
# Register your models here.
admin.site.register(City)
admin.site.register(State)
admin.site.register(UserDetails)
admin.site.register(VehicleTypes)
admin.site.register(VehicleBrands)
admin.site.register(VehicleDetails)
admin.site.register(RentalRequests)
admin.site.register(Rentals)
