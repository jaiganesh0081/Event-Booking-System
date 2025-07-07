from django.db import models
from django.contrib.auth.models import AbstractUser


class UserModel(AbstractUser):
    is_admin = models.BooleanField(default=False)
# Create your models here.
class EventModel(models.Model):
    title=models.CharField(max_length=150)
    description=models.CharField(max_length=150)
    datetime=models.DateTimeField()
    location=models.CharField(max_length=150)
    seats_available=models.IntegerField()
    created_by=models.ForeignKey(UserModel,on_delete=models.CASCADE,related_name='event')

    def __str__(self):
        return self.title


class BookingModel(models.Model):
    user=models.ForeignKey(UserModel,on_delete=models.CASCADE,related_name='booking')
    event=models.ForeignKey(EventModel,on_delete=models.CASCADE,related_name='booking')
    quantity=models.PositiveIntegerField(default=1)
    booking_time=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=('user','event')
    