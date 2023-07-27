from .models import User
from rest_framework import serializers
from django.core.exceptions import ValidationError
from phonenumber_field.serializerfields import PhoneNumberField

def validate_min_length(value):
    if len(value) < 6:
        raise ValidationError("your password should be 6 characters or more.")

class UserListSerializer(serializers.ModelSerializer): 
    class Meta:
        model = User
        fields = ['username','email','phone_number','password']

class UserCreationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=25) 
    email = serializers.EmailField(max_length=80)
    phone_number = PhoneNumberField(allow_null=False,allow_blank=False)
    password = serializers.CharField(max_length=20,validators=[validate_min_length],write_only=True)

    class Meta:
        model = User
        fields = ['username','email','phone_number','password']

    def validate(self,attrs):
        username_exists=User.objects.filter(username=attrs['username']).exists()
        
        if username_exists:
            raise serializers.ValidationError(detail='User with this username already exists')
        
        email_exists=User.objects.filter(email=attrs['email']).exists()
        
        if email_exists:
            raise serializers.ValidationError(detail='User with this email already exists')
        
        phone_number_exists=User.objects.filter(phone_number=attrs['phone_number']).exists()
        
        if phone_number_exists:
            raise serializers.ValidationError(detail='User with this phonenumber already exists')
        
        return super().validate(attrs)

    def create(self,validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            phone_number = validated_data['phone_number']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


