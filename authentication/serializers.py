from rest_framework import serializers
from django.contrib.auth import authenticate

from students.models import Student
from lecturers.models import Lecturer
from .models import CustomUser

class StudentRegistrationSerializer(serializers.ModelSerializer):
    # User fields
    first_name = serializers.CharField(write_only=True, required=True)
    last_name = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    # Student fields
    mat_no = serializers.CharField(write_only=True, required=True)
    date_of_birth = serializers.DateField(write_only=True, required=True, input_formats=['%d-%m-%Y', '%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d'])
    gender = serializers.CharField(write_only=True, required=True)
    department = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = Student
        fields = ["first_name", "last_name", "email", "mat_no", "department", "date_of_birth", "gender", "password", "password2"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Password doesn't match."})
        
        return attrs
    
    def create(self, validated_data):
        # Extra data for User field
        user_data = {
            "username": "Hello",
            "first_name": validated_data.pop('first_name'),
            "last_name": validated_data.pop('last_name'),
            "email": validated_data.pop('email',),
            "user_type": "student"
        }
        validated_data.pop('password2')
        password = validated_data.pop('password')

        # Create User instance
        user = CustomUser.objects.create_user(**user_data, password=password)

        # Create Student instance (OneToOne relationship magic happens here)
        student = Student.objects.create(user=user, **validated_data)

        return student
    

class LecturerRegistrationSerializer(serializers.ModelSerializer):
    # User fields
    first_name = serializers.CharField(write_only=True, required=True)
    last_name = serializers.CharField(write_only=True, required=True)
    email = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)


    # Lecturer fields
    title = serializers.CharField(write_only=True, required=True)
    date_of_birth = serializers.DateField(write_only=True, required=True, input_formats=['%d-%m-%Y', '%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d'])
    gender = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Lecturer
        fields = ["first_name", "last_name", "email", "password", "password2", "title", "date_of_birth", "gender"]


    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Password doesn't match."})
        
        return attrs
    
    def create(self, validated_data):
        # Extract User fields

        user_data = {
            "username": "None",
            "first_name": validated_data.pop('first_name'),
            "last_name": validated_data.pop('last_name'),
            "email": validated_data.pop('email',),
            "user_type": "lecturer"
        }

        validated_data.pop("password2")
        password = validated_data.pop('password')

        # Create User instance

        user = CustomUser.objects.create_user(**user_data, password=password)

        # Create Lecturer instance (OneToOne relationship magic happens here)

        lecturer = Lecturer.objects.create(user=user, **validated_data)

        return lecturer


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:

            user_instace = CustomUser.objects.get(email=email)

            if email and password:
                user = authenticate(
                    request=self.context.get('request'),
                    username =user_instace.username,
                    password = password
                )

                if not user:
                    raise serializers.ValidationError("Can't log in user with the provided credential above. Try providing a valid credential.", code='authorization')
                
                attrs["user"] = user
                return attrs
            
            else:
                raise serializers.ValidationError("email and password is required", code='authorization')
        
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User doesn't exist")
    
