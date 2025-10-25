from rest_framework import serializers

from .models import Student, StudentCourses
from courses.models import Courses

class StudentProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")
    department = serializers.StringRelatedField()

    class Meta:
        model = Student
        fields = ["first_name", "last_name", "email", "mat_no", "date_of_birth", "gender", "level", "department", "courses", "get_academic_progress", "get_cumulative_gpa"]


class StudentCourseRegistrationSerializer(serializers.ModelSerializer):
    courses_id = serializers.ListField(child=serializers.CharField(), required=True, write_only=True) 
    class Meta:
        model = StudentCourses
        fields = '__all__'
        read_only_fields = ["student_id"]

    def create(self, validated_data):
        student = self.context.get("student")

        if not student:
            raise serializers.ValidationError("Student not found")
        
        courses = validated_data.pop("courses_id")

        if isinstance(courses, list):
            added_courses = []
            for course in courses:
                try:
                    course_instance = Courses.objects.get(title=course)

                    add_course = StudentCourses.objects.create(student_id=student, courses_id=course_instance, **validated_data)

                    added_courses.append(add_course)
                
                except Courses.DoesNotExist:
                    raise serializers.ValidationError(f"{course} does not exist")
            
            return added_courses

        else:
           pass

