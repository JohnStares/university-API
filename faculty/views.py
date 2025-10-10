from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny


from .serializers import FacultySerializer
from .models import Faculties


# Create your views here.
class FacultyView(APIView):
    permission_classes = [AllowAny]
    #authentication_classes = [JWTAuthentication]


    def post(self, request):
        try:
            serializer = FacultySerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()

                return Response({"msg": "Faculty created successfully."}, status=status.HTTP_201_CREATED)
            
            return Response({"error_msg": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"error": "Having issues adding faculty.", "detials": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def get(self, request):
        try:
            faculties = Faculties.objects.all()

            serializers = FacultySerializer(faculties, many=True)

            if serializers.data == []:
                return Response({"msg": "No faculty has been added yet"}, status=status.HTTP_200_OK)
            
            return Response(serializers.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

