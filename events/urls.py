
from django.urls import path
from .views import *
urlpatterns = [
    path('register/',RegisterView.as_view()),
    path('event/register/',EventRegisterView.as_view()),
    path('event/register/<int:id>/',EventRegisterViewById.as_view()),
    path('booking/event/',UserBookingView.as_view()),
]
