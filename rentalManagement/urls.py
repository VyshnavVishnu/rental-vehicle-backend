from django.urls import path,include
from . import views
from rest_framework.routers import SimpleRouter

from .views import (UserClass, VehicleClass, VehicleDetail,
                    VehicleClassForUser, VehicleDetailForUser, UserLogin, RentalRequest, RequestDetails, RentalClass,
                    RentalDetail)

router = SimpleRouter()

router.register('state',views.StateClass)
router.register('city',views.CityClass)
router.register('brands',views.VehicleBrandClass)
router.register('types',views.VehicleTypeClass)

urlpatterns = [
    path('',include(router.urls)),
    path('users/', UserClass.as_view(), name='user-form-list'),
    # path('users/<int:user_id>/', UserDetail.as_view(), name='user-detail'),

    path('vehicle/', VehicleClass.as_view(), name='vehicle-form-list'),
    path('vehicle/<int:vehicle_id>/', VehicleDetail.as_view(), name='vehicle-detail'),

    path('vehicleForUser/', VehicleClassForUser.as_view(), name='vehicle-form-userlist'),
    path('vehicleForUser/<int:vehicle_id>/', VehicleDetailForUser.as_view(), name='vehicle-detail'),

    path('userLogin/', UserLogin.as_view(), name='vehicle-detail'),

    path('rentalRequest/',RentalRequest.as_view(), name='rental-requests'),
    path('requestDetails/<int:request_id>/',RequestDetails.as_view(), name='request-details'),

    path('rentals/', RentalClass.as_view(), name='rentals'),
    path('rentalDetails/<int:user_id>/', RentalDetail.as_view(), name='rentalDetails'),

]