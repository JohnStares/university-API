from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication


from .models import Departments
from faculty.models import Faculties
from .serializers import DepartmentSerializer

# Create your views here.
class DepartmentsView(APIView):
    permission_classes = [AllowAny]
    #authentication_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = DepartmentSerializer(data=request.data)

            if serializer.is_valid():
                faculty = Faculties.objects.get(name=serializer.validated_data["faculty"])

                if faculty:
                    serializer.save(faculty=faculty)

                    return Response({"msg": "Department Added."}, status=status.HTTP_201_CREATED)
            
            return Response({"error_msg": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        except Faculties.DoesNotExist:
            return Response({"error_msg": "Faculty does not exist, Try adding a valid faculty name"}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                "error": "Having difficulties adding department",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    def get(self, request):
        try:
            departments = Departments.objects.all()

            serializers = DepartmentSerializer(departments, many=True)

            if serializers.data == []:
                return Response({"msg": "No department have been added."}, status=status.HTTP_200_OK)

            return Response(serializers.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
