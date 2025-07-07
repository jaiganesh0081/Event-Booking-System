#swagger.py
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import serializers
from drf_yasg.utils import swagger_auto_schema


from events.serializer import UserBookingSerializer

schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@myapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


# # serializers.py
class BookingRequestSerializer(serializers.Serializer):
    event_id = serializers.IntegerField(help_text="ID of the event")
    quantity = serializers.IntegerField(help_text="Number of seats to book")

class SwaggerRegisterSerializer(serializers.Serializer):
    username=serializers.CharField(help_text="Type your usernmae")
    password=serializers.FileField(help_text="Type your password")




userbooks =swagger_auto_schema(
        operation_description='Creating a New Booking',
        request_body=BookingRequestSerializer,  # 
        responses={201: UserBookingSerializer, 400: "Bad request"}
    )

register=swagger_auto_schema(
        request_body=SwaggerRegisterSerializer,
        responses={
            201: openapi.Response('User created successfully'),
            400: 'Bad Request'
        }
    )


getbookingdetail=swagger_auto_schema(
            operation_description="View user booked events",
            responses={
                200:UserBookingSerializer,404:"No data found"
            }
    )