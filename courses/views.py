from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated


from .models import Courses
from faculty.models import Faculties
from .serializers import CoursesSerializer
from departments.models import Departments


# Create your views here.
class CourseView(APIView):
    permission_classes = [AllowAny]
    #authentication_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = CoursesSerializer(data=request.data)

            if serializer.is_valid():

                departement = Departments.objects.get(name=serializer.validated_data['departments'])
                faculty = Faculties.objects.get(name=serializer.validated_data["faculty"])

                if departement and faculty:
                    serializer.save(departments=departement, faculty=faculty)

                    return Response({"msg": "Course added"}, status=status.HTTP_201_CREATED)
                
            return Response({"error_msg": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        except Departments.DoesNotExist:
            return Response({"error_msg": "Department does not exist. Try input a valid department name"}, status=status.HTTP_400_BAD_REQUEST)
        
        except Faculties.DoesNotExist:
            return Response({"error_msg": "Faculty does not exist. Try input a valid department name"}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def get(self, request):
        try:
            courses = Courses.objects.all()

            serializers = CoursesSerializer(courses, many=True)

            if serializers.data == []:
                return Response({"msg": "No courses added yet"}, status=status.HTTP_200_OK)

            return Response(serializers.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)