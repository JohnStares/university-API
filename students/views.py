from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication


from .serializers import StudentProfileSerializer, StudentCourseRegistrationSerializer
from courses.models import Courses
from .models import Student

# Create your views here.

class StudentProfileView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:

            serializer = StudentProfileSerializer(request.user.student)


            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request):
        try:
            student = Student.objects.get(user=request.user)
            serializer = StudentCourseRegistrationSerializer(data=request.data, context={"student": student})

            if serializer.is_valid():
                serializer.save()

                return Response({"msg": "Course registered successfully"}, status=status.HTTP_201_CREATED)
            
            return Response({"error_msg": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)