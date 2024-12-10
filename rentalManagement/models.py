from django.db import models


class State(models.Model):
    state = models.CharField(max_length=20)

    def __str__(self):
        return self.state


class City(models.Model):
    city = models.CharField(max_length=20)
    state = models.ForeignKey(State,on_delete=models.CASCADE)

    def __str__(self):
        return self.city


class UserDetails(models.Model):
    fullName = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phoneNumber = models.CharField(max_length=10)
    password = models.CharField(max_length=50)
    gender = models.CharField(max_length=20)
    state = models.ForeignKey(State,on_delete=models.CASCADE)
    city = models.ForeignKey(City,on_delete=models.CASCADE)
    dateOfBirth = models.DateField(null=True,blank=True)
    profilePicture = models.FileField(upload_to='profile/',null=True, blank=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.fullName


class VehicleTypes(models.Model):
    vehicleType = models.CharField(max_length=30)

    def __str__(self):
        return self.vehicleType


class VehicleBrands(models.Model):
    vehicleBrand = models.CharField(max_length=30)

    def __str__(self):
        return self.vehicleBrand


class VehicleDetails(models.Model):
    vehicleName = models.CharField(max_length=25)
    description = models.TextField()
    vehicleType = models.ForeignKey(VehicleTypes,on_delete=models.CASCADE)
    brand = models.ForeignKey(VehicleBrands, on_delete=models.CASCADE)
    rent = models.CharField(max_length=10)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return self.vehicleName


class RentalRequests(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(VehicleDetails, on_delete=models.CASCADE)
    startDate = models.DateField()
    endDate = models.DateField()
    requestStatus = models.BooleanField(default=False)

    def __str__(self):
        return self.user.fullName


class Rentals(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(VehicleDetails, on_delete=models.CASCADE)
    startDate = models.DateField()
    endDate = models.DateField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.fullName
