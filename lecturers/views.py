from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


from .serializers import LecturerProfileSerializer, StudentProfileSerializer
from students.models import Student
from. models import Lecturer

# Create your views here.

class LecturerProfile(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            serilizer = LecturerProfileSerializer(request.user.lecturer)

            return Response(serilizer.data, status= status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class StudentsProfile(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            students = Student.objects.filter(
                department__in=Lecturer.objects.filter(pk=request.user.id).values("department")
            ).values("user__id", "user__first_name", "user__last_name", "mat_no")

            # Might be used later for optimization.
            # serializer = StudentProfileSerializer(students, many=True)

            return Response(list(students), status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class StudentProfile(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, id):
        try:

            student = Student.objects.get(pk=id)

            serializer = StudentProfileSerializer(student)

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Student.DoesNotExist:
            return Response({"error": "Student does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    



