from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Bus, Book

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

class BusSerializer(serializers.ModelSerializer):
    arrival_time_str = serializers.ReadOnlyField()
    
    class Meta:
        model = Bus
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ('user', 'status')
