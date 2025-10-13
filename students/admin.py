from django.contrib import admin

from .models import Student, StudentCourses, GradeScale

# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["user", "mat_no", "date_of_birth", "gender", "level", "department", "display_cgpa", "get_academic_progress"]
    search_fields = ["user", "mat_no", "date_of_birth", "gender", "level", "department"]
    list_filter = ["mat_no", "gender", "department", "level"]

    def display_cgpa(self, obj):
        cgpa = obj.get_cumulative_gpa()

        return f"{cgpa:.2f}" if cgpa else 0.00
    
    display_cgpa.short_description = "CGPA"


    def display_gpa(self, obj):
        return obj.get_semester_gpa()
    
    display_gpa.short_description = 'GPA'

    def get_academic_progress(self, obj):
        return obj.get_academic_progress()
    
    get_academic_progress.short_description = "ACADEMIC PROGRESS"
    

@admin.register(StudentCourses)
class StudentCourseAdmin(admin.ModelAdmin):
    list_display = ["id", "student_id", "courses_id", "grade", "semester", "academic_year"]
    search_fields = ["student_id", "courses_id", "grade", "semester", "academic_year"]




@admin.register(GradeScale)
class GradeAdmin(admin.ModelAdmin):
    list_display = ["id", "grade", "grade_points", "description"]
    search_fields = ["grade", "grade_points", "description"]