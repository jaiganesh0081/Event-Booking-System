from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .permission import *
from .serializer import *
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .swagger import *
from django.core.mail import send_mail
from django.conf import settings


class RegisterView(APIView):
    @register
    def post(self,request):
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":serializer.data},status=status.HTTP_201_CREATED)
        return Response({"errors":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    


class EventRegisterView(APIView):
    permission_classes=[IsAuthenticated,AdminOnlyOrReadOnly]

    @swagger_auto_schema(
        operation_description="Get all events (Admin Only)",
        responses={200: EventSerializer(many=True), 404: 'Not Found'}
    )
    def get(self,request):
        try:
            events=EventModel.objects.all()
        except EventModel.DoesNotExist:
            return Response({"errors":"No data found"},status=status.HTTP_404_NOT_FOUND)
        serializer=EventSerializer(events,many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new event",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["title", "description", "datetime", "location", "seats_available"],
            properties={
                "title": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Title of the event"
                ),
                "description": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Detailed description of the event"
                ),
                "datetime": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format="date-time",  # This helps Swagger UI expect correct format
                    description="Date and time in format YYYY-MM-DDTHH:MM (e.g., 2025-12-25T12:30)"
                ),
                "location": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Location where the event will be held"
                ),
                "seats_available": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Number of available seats for the event"
                )
            }
        ),
        responses={
            201: "Successfully created the event",
            400: "Bad Request - Invalid input"
        })

    def post(self,request):
        serializer=EventSerializer(data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message":serializer.data},status=status.HTTP_201_CREATED)
        return Response({"errors":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    


class EventRegisterViewById(APIView):
    permission_classes=[IsAuthenticated,AdminOnly]


    @swagger_auto_schema(
            operation_description="Get event by ID",
            responses={200:EventSerializer,404:"Not Found"}
    )
    def get(self,request,id):
        event=get_object_or_404(EventModel,id=id)
        serializer=EventSerializer(event)
        return Response({"message":serializer.data},status=status.HTTP_200_OK)


    @swagger_auto_schema(
            request_body=EventSerializer,
            operation_description='Update the event by ID',
            responses={200:EventSerializer,404:"Not Found"}
    )
    def put(self,request,id):
        event=get_object_or_404(EventModel,id=id)
        serializer=EventSerializer(event,request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":serializer.data},status=status.HTTP_202_ACCEPTED)
        return Response({"errors":serializer.errors},status=status.HTTP_400_BAD_REQUEST)



class UserBookingView(APIView):
    permission_classes=[IsAuthenticated]

    @getbookingdetail
    def get(self,request):
        user=request.user
        try:
            User_booked=BookingModel.objects.filter(user=user)
        except BookingModel.DoesNotExist:
            return Response({"errors":"No data found"},status=status.HTTP_404_NOT_FOUND)
        serializer=UserBookingSerializer(User_booked,many=True)
        return Response({"message":serializer.data},status=status.HTTP_200_OK)

    @userbooks
    def post(self,request):
        serializer=UserBookingSerializer(data=request.data,context={"request":request})
        if serializer.is_valid():
            serializer.save()
            subject="Your Booking is confirmed"
            message="Thankyou for using as app .Please support as to achieved more celebraty events"
            recipient='jairajchamp1@gmail.com'

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [recipient],
                fail_silently=False

            )
            return Response({"message":serializer.data},status=status.HTTP_201_CREATED)
        return Response({"errors":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

