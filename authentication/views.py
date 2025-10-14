from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError


from .serializers import (
    StudentRegistrationSerializer,
    LecturerRegistrationSerializer,
    LoginSerializer
)

from departments.models import Departments

# Create your views here.

class StudentRegister(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = StudentRegistrationSerializer(data=request.data)

            if serializer.is_valid():
                department = Departments.objects.get(name=serializer.validated_data["department"])

                if department:
                    serializer.save(department=department)

                    return Response({"msg": "Student Registration is successfully."}, status=status.HTTP_201_CREATED)
                
            return Response({"error_msg": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        

        except Departments.DoesNotExist:
            return Response({"error_msg": "Department doesn't exist."}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LecturerRegister(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = LecturerRegistrationSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()

                return Response({"msg": "Lecturer Registration is successfully."}, status=status.HTTP_201_CREATED)
            
            return Response({"error_msg": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data, context={"request": request})

            if serializer.is_valid():
                user = serializer.validated_data["user"]

                if user.user_type == "student":

                    refresh_token = RefreshToken.for_user(user)

                    return Response({
                    "msg": "Login Successful",
                    "refresh": str(refresh_token),
                    "access": str(refresh_token.access_token)
                }, status=status.HTTP_200_OK)

                elif user.user_type == "lecturer":
                    
                    refresh_token = RefreshToken.for_user(user)

                    return Response({
                    "msg": "Login Successful",
                    "refresh": str(refresh_token),
                    "access": str(refresh_token.access_token)
                }, status=status.HTTP_200_OK)
                
            
            return Response({"error_msg": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")

            if not refresh_token:
                return Response({"error_msg": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"msg": "Logged out successfully."}, status=status.HTTP_200_OK)
        
        except TokenError as t:
            return Response({
                "error_msg": "Token is invalid",
                "details": str(t)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

