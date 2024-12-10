from datetime import timedelta

from django.middleware.csrf import logger
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import StateSerializer, CitySerializer, VehicleBrandSerializer, VehicleTypeSerializer
from .models import State, City, UserDetails, VehicleDetails, VehicleTypes, VehicleBrands, RentalRequests, Rentals


# Create your views here.


class StateClass(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer


class CityClass(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class UserClass(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def get(self, request):
        try:
            # Retrieve all users
            users = UserDetails.objects.all()

            # List to store all user details
            user_list = []

            # Iterate through each user
            for user in users:
                # Prepare user details dictionary
                user_details = {
                    'id': user.id,
                    'fullName': user.fullName,
                    'phoneNumber': user.phoneNumber,
                    'dateOfBirth': user.dateOfBirth,
                    'email': user.email,
                    'gender': user.gender,
                    'password': user.password,
                    'city': user.city.city,
                    'state': user.state.state
                }

                # Conditionally add profilePicture if it exists
                if user.profilePicture:
                    user_details['profilePicture'] = user.profilePicture.url


                # Add to user list
                user_list.append(user_details)
            # Return the list of all users
            return Response(user_list, status=status.HTTP_200_OK)

        except Exception as e:
            # Detailed error logging
            logger.error(f"Unexpected error in get method: {str(e)}", exc_info=True)
            return Response(
                {'error': 'An unexpected error occurred while fetching users'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        try:
            data = request.data  # DRF will handle parsing
            print(data)

            # Personal Details

            fullName = data.get('fullName')
            phoneNumber = data.get('phoneNumber')
            dateOfBirth = data.get('dateOfBirth')
            email = data.get('email')
            gender = data.get('gender')
            password = data.get('password')
            cityid = data.get('city')
            stateid = data.get('state')
            profile = request.FILES.get('profilePicture')

            city = City.objects.get(id=cityid)
            state = State.objects.get(id=stateid)
            # Create the user


            user = UserDetails.objects.create(
                fullName=fullName,
                phoneNumber=phoneNumber,
                email=email,
                gender=gender,
                password=password,
                city=city,
                state=state,
                profilePicture=profile
            )
            if data.get('dateOfBirth') != 'null':
                user.dateOfBirth = dateOfBirth;
            print(user)
            user.save()

            # Return the created user's details
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(f"Error: {e}")
            return Response({'error': 'An error occurred while creating user'}, status=status.HTTP_400_BAD_REQUEST)


class VehicleBrandClass(viewsets.ModelViewSet):
    queryset = VehicleBrands.objects.all()
    serializer_class = VehicleBrandSerializer


class VehicleTypeClass(viewsets.ModelViewSet):
    queryset = VehicleTypes.objects.all()
    serializer_class = VehicleTypeSerializer


class VehicleClass(APIView):
    def get(self, request):
        try:
            # Retrieve all users
            vehicles = VehicleDetails.objects.all()

            # List to store all user details
            vehicles_list = []

            # Iterate through each user
            for vehicle in vehicles:
                # Prepare user details dictionary
                vehicle_details = {
                    'id': vehicle.id,
                    'vehicleName': vehicle.vehicleName,
                    'description': vehicle.description,
                    'vehicleType': vehicle.vehicleType.vehicleType,
                    'brand': vehicle.brand.vehicleBrand,
                    'rent': vehicle.rent,
                    'availability':vehicle.availability,
                    'vehicleTypeId':vehicle.vehicleType.id,
                    'brandId':vehicle.brand.id
                }
                # print(vehicle_details)
                vehicles_list.append(vehicle_details)
                # print(vehicles_list)
            # Return the list of all users
            return Response(vehicles_list, status=status.HTTP_200_OK)

        except Exception as e:
            # Detailed error logging
            logger.error(f"Unexpected error in get method: {str(e)}", exc_info=True)
            return Response(
                {'error': 'An unexpected error occurred while fetching vehicles'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self,request):
        try:
            data = request.data  # DRF will handle parsing
            print(data)

            # Personal Details

            vehicleName = data.get('vehicleName')
            description = data.get('description')
            typeId = data.get('vehicleType')
            brandId = data.get('brand')
            rent = data.get('rentPerDay')

            vehicleType = VehicleTypes.objects.get(id=typeId)
            brand = VehicleBrands.objects.get(id=brandId)
            # Create the user
            vehicle = VehicleDetails.objects.create(
                vehicleName=vehicleName,
                description=description,
                vehicleType=vehicleType,
                brand=brand,
                rent=rent,
            )
            print(vehicle)
            vehicle.save()

            # Return the created user's details
            return Response({'message': 'Vehicle added successfully'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(f"Error: {e}")
            return Response({'error': 'An error occurred while adding vehicle'}, status=status.HTTP_400_BAD_REQUEST)


class VehicleDetail(APIView):
    def get(self, request, vehicle_id):
        try:
            # Retrieve specific user by ID
            vehicle = get_object_or_404(VehicleDetails, id=vehicle_id)

            # Prepare user details dictionary
            vehicle_details = {
                'id': vehicle.id,
                'vehicleName': vehicle.vehicleName,
                'description': vehicle.description,
                'vehicleType': vehicle.vehicleType.id,
                'brand': vehicle.brand.id,
                'rent': vehicle.rent,
                'availability':vehicle.availability
            }

            # Return the user details
            return Response(vehicle_details, status=status.HTTP_200_OK)

        except VehicleDetails.DoesNotExist:
            return Response(
                {'error': f'Vehicle with ID {vehicle_id} not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Unexpected error in get_by_id method: {str(e)}", exc_info=True)
            return Response(
                {'error': 'An unexpected error occurred while fetching user details'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, vehicle_id):
        # print(vehicle_id)
        try:
            # Retrieve the user
            vehicle = get_object_or_404(VehicleDetails, id=vehicle_id)
            data = request.data
            # Personal Details Update
            vehicle.vehicleName = data.get('vehicleName', vehicle.vehicleName)
            vehicle.description = data.get('description', vehicle.description)
            typeId = data.get('vehicleType')
            vehicle.vehicleType = VehicleTypes.objects.get(id=typeId['id'])
            brandId = data.get('brand')
            vehicle.brand = VehicleBrands.objects.get(id=brandId['id'])
            vehicle.rent = data.get('rent', vehicle.rent)
            vehicle.availability = data.get('availability', vehicle.availability)
            vehicle.save()


            # Retrieve updated user details (similar to GET method)
            vehicle_details = {
                'id': vehicle.id,
                'vehicleName': vehicle.vehicleName,
                'description': vehicle.description,
                'vehicleType': vehicle.vehicleType.vehicleType,
                'brand': vehicle.brand.vehicleBrand,
                'rent': vehicle.rent,
            }

            return Response(vehicle_details, status=status.HTTP_200_OK)

        except VehicleDetails.DoesNotExist:
            return Response(
                {'error': f'Vehicle with ID {vehicle_id} not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            logger.error(f"Unexpected error in put method: {str(e)}", exc_info=True)
            return Response(
                {'error': 'An unexpected error occurred while updating user details'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, vehicle_id):
        try:
            # Retrieve the user
            vehicle = get_object_or_404(VehicleDetails, id=vehicle_id)

            # Delete the user
            vehicle.delete()

            return Response(
                {'message': f'Vehicle with ID {vehicle_id} deleted successfully'},
                status=status.HTTP_200_OK
            )

        except VehicleDetails.DoesNotExist:
            return Response(
                {'error': f'Vehicle with ID {vehicle_id} not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Unexpected error in delete method: {str(e)}", exc_info=True)
            return Response(
                {'error': 'An unexpected error occurred while deleting Vehicle'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class VehicleClassForUser(APIView):
    def get(self, request):
        try:
            # Retrieve all users
            vehicles = VehicleDetails.objects.all()

            # List to store all user details
            vehicles_list = []

            # Iterate through each user
            for vehicle in vehicles:
                # Prepare user details dictionary
                vehicle_details = {
                    'id': vehicle.id,
                    'vehicleName': vehicle.vehicleName,
                    'description': vehicle.description,
                    'vehicleType': vehicle.vehicleType.id,
                    'brand': vehicle.brand.id,
                    'rent': vehicle.rent,
                }

                if vehicle.availability == True:
                    vehicles_list.append(vehicle_details)
                else:
                    continue
            # Return the list of all users
            return Response(vehicles_list, status=status.HTTP_200_OK)

        except Exception as e:
            # Detailed error logging
            logger.error(f"Unexpected error in get method: {str(e)}", exc_info=True)
            return Response(
                {'error': 'An unexpected error occurred while fetching vehicles'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class VehicleDetailForUser(APIView):
    def get(self, request, vehicle_id):
        try:
            # Retrieve specific user by ID
            vehicle = get_object_or_404(VehicleDetails, id=vehicle_id)

            # Prepare user details dictionary
            vehicle_details = {
                'id': vehicle.id,
                'vehicleName': vehicle.vehicleName,
                'description': vehicle.description,
                'vehicleType': vehicle.vehicleType.vehicleType,
                'brand': vehicle.brand.vehicleBrand,
                'rent': vehicle.rent,
            }

            # Return the user details
            return Response(vehicle_details, status=status.HTTP_200_OK)

        except VehicleDetails.DoesNotExist:
            return Response(
                {'error': f'Vehicle with ID {vehicle_id} not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Unexpected error in get_by_id method: {str(e)}", exc_info=True)
            return Response(
                {'error': 'An unexpected error occurred while fetching user details'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserLogin(APIView):
    def post(self,request):
        data = request.data
        email = data.get('email')
        password = data.get('password')

        try:
            user = UserDetails.objects.get(email=email)
            # print(user.is_admin)
            if (password == user.password):
                # print('password')
                if(user.is_admin == True):
                    return Response({'message': 'Login successful', 'userId': user.id,'user':1})
                else:
                    return Response({'message': 'Login successful', 'userId': user.id,'user':2})

            else:
                return Response({'error': 'Invalid password'}, status=400)
        except UserDetails.DoesNotExist:
            return Response({'error': 'Invalid email'}, status=400)

        return Response({'error': 'Invalid request method'}, status=405)


class RentalRequest(APIView):
    def get(self, request):
        try:
            # Retrieve all users
            requests = RentalRequests.objects.all()

            # List to store all user details
            requests_list = []

            # Iterate through each user
            for req in requests:
                # Prepare user details dictionary
                request_details = {
                    'id': req.id,
                    'user': req.user.fullName,
                    'vehicle': req.vehicle.vehicleName,
                    'startDate': req.startDate,
                    'endDate': req.endDate,
                    'requestStatus': req.requestStatus,
                }
                requests_list.append(request_details)

            # Return the list of all users
            return Response(requests_list, status=status.HTTP_200_OK)

        except Exception as e:
            # Detailed error logging
            logger.error(f"Unexpected error in get method: {str(e)}", exc_info=True)
            return Response(
                {'error': 'An unexpected error occurred while fetching requests'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(selfself,request):
        try:
            data = request.data  # DRF will handle parsing
            print(data)

            # Personal Details

            data = request.data
            startDate = data.get('startDate')
            endDate = data.get('endDate')
            vehicleId = data.get('vehicleId')
            vehicle = VehicleDetails.objects.get(id=vehicleId)
            userId = data.get('userId')
            user = UserDetails.objects.get(id=userId)

            existing_request = RentalRequests.objects.filter(
                user=user, vehicle=vehicle, startDate=startDate
            ).first()

            if existing_request:
                return Response({'message': 'Request already exists, Please Try Again Later'})

            # Create the request
            req = RentalRequests.objects.create(
                user=user,
                vehicle=vehicle,
                startDate=startDate,
                endDate=endDate
            )
            print(req)
            req.save()

            # Return the created user's details
            return Response({'message': 'Request added successfully'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(f"Error: {e}")
            return Response({'error': 'An error occurred while adding request'}, status=status.HTTP_400_BAD_REQUEST)


class RequestDetails(APIView):
    def get(self, request, request_id):
        try:
            # Retrieve specific user by ID
            req = get_object_or_404(RentalRequests, id=request_id)

            # Prepare user details dictionary
            request_details = {
                'id': req.id,
                'vehicleName': req.vehicle.vehicleName,
                'vehicleType': req.vehicle.vehicleType.vehicleType,
                'brand': req.vehicle.brand.vehicleBrand,
                'startDate':req.startDate,
                'endDate':req.endDate,
                'rent': req.vehicle.rent,
                'availability': req.vehicle.availability,
                'userName': req.user.fullName,
                'email': req.user.email,
                'phoneNumber': req.user.phoneNumber,
                'gender': req.user.gender,
                'dateOfBirth': req.user.dateOfBirth,
            }

            # Return the user details
            return Response(request_details, status=status.HTTP_200_OK)

        except RentalRequests.DoesNotExist:
            return Response(
                {'error': f'Request with ID {request_id} not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Unexpected error in get_by_id method: {str(e)}", exc_info=True)
            return Response(
                {'error': 'An unexpected error occurred while fetching request details'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, request_id):
        try:
            # Retrieve the user
            req = get_object_or_404(RentalRequests, id=request_id)

            # Delete the user
            req.delete()

            return Response(
                {'message': f'Request with ID {request_id} deleted successfully'},
                status=status.HTTP_200_OK
            )

        except RentalRequests.DoesNotExist:
            return Response(
                {'error': f'Vehicle with ID {request_id} not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Unexpected error in delete method: {str(e)}", exc_info=True)
            return Response(
                {'error': 'An unexpected error occurred while deleting Vehicle'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class RentalClass(APIView):
    def post(self, request):
        try:

            data = request.data
            # print(data)

            reqId = data.get('id')
            req = RentalRequests.objects.get(id=reqId)
            user = req.user
            vehicle = req.vehicle
            startDate = req.startDate
            endDate = req.endDate

            rental = Rentals.objects.create(
                user=user,
                vehicle=vehicle,
                startDate=startDate,
                endDate=endDate
            )
            # print(rental)
            rental.save()
            req.delete()


            return Response({'message': 'Request approved successfully'},status=status.HTTP_200_OK)

        except RentalRequests.DoesNotExist:
            return Response(
                {'error': f'Request with ID {rental.id} not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            logger.error(f"Unexpected error in put method: {str(e)}", exc_info=True)
            return Response(
                {'error': 'An unexpected error occurred while updating request details'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class RentalDetail(APIView):
    def get(self, request, user_id):
        try:
            # Retrieve specific user by ID
            rentals = Rentals.objects.filter(user=user_id)

            rental_list = []

            for rental in rentals:
                today = timezone.now().date()
                # yesterday = today - timedelta(days=1)
                yesterday = '2024-12-07'

                if yesterday <= str(rental.endDate):
                # if yesterday >= rental.endDate:
                    rental.active = False;

                rental_details = {
                    'vehicleName': rental.vehicle.vehicleName,
                    'vehicleType': rental.vehicle.vehicleType.vehicleType,
                    'startDate': rental.startDate,
                    'endDate': rental.endDate,
                    'status':rental.active,
                    'rent':rental.vehicle.rent
                }
                rental_list.append(rental_details)

            return Response(rental_list, status=status.HTTP_200_OK)

        except VehicleDetails.DoesNotExist:
            return Response(
                {'error': f'Rental Details for user with id{user_id} not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Unexpected error in get_by_id method: {str(e)}", exc_info=True)
            return Response(
                {'error': 'An unexpected error occurred while fetching Rental details'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
