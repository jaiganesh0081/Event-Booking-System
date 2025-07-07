from rest_framework import serializers
from .models import *



class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserModel
        fields=['username','password','is_admin']
        extra_kwargs={
            "password":{
                "write_only":True
            }
        }
    
    def create(self,validated_data):
        return UserModel.objects.create_user(**validated_data)

class EventSerializer(serializers.ModelSerializer):
    created_by=RegisterSerializer(read_only=True)
    datetime = serializers.DateTimeField()
    class Meta:
        model=EventModel
        fields=['id','title','description','datetime','location','seats_available','created_by']

    def create(self,validated_data):
        user=self.context['request'].user
        return EventModel.objects.create(created_by=user,**validated_data)
    def update(self,instance,validated_data):
        for key,value in validated_data.items():
            setattr(instance,key,value)
        instance.save()
        return instance
    

class UserBookingSerializer(serializers.ModelSerializer):
    event=EventSerializer(read_only=True)
    event_id=serializers.PrimaryKeyRelatedField(queryset=EventModel.objects.all(),write_only=True)
   
    
    class Meta:
        model=BookingModel
        fields=['event','event_id','quantity']
    
    def create(self,validated_data):
        user=self.context['request'].user
        quantity=validated_data.pop('quantity')
        event=validated_data.pop('event_id')
        
        if quantity>event.seats_available:
            raise serializers.ValidationError("No available seats")
        event.seats_available-=quantity
        event.save()

        booking=BookingModel.objects.create(user=user,quantity=quantity,event=event)
        return booking
    

