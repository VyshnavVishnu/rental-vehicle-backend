from rest_framework import serializers
from .models import State,City,VehicleBrands,VehicleTypes


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = "__all__"


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class VehicleBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleBrands
        fields = "__all__"


class VehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleTypes
        fields = "__all__"
