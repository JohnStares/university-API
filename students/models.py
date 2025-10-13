from django.db import models


from authentication.models import CustomUser
from departments.models import Departments
from courses.models import Courses


# Create your models here.
class Student(models.Model):
    GENDER = (
        ('M', 'Male'),
        ('F', "Female")
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    mat_no = models.CharField(max_length=13, null=True, blank=True)
    date_of_birth = models.DateField(null=False, blank=False)
    gender = models.CharField(max_length=6, choices=GENDER)


    level = models.IntegerField(default=100)

    department = models.ForeignKey(Departments, related_name="student_department", on_delete=models.CASCADE)
    courses = models.ManyToManyField(Courses, through="StudentCourses", related_name="student_courses")


    def __str__(self):
        return f"{self.mat_no} {self.user.get_full_name()}"
    

    def get_semester_gpa(self, semester, year):
        """Calculates GPA for a particular semester"""

        course_enrollment = StudentCourses.objects.filter(
            student_id = self,
            semester = semester,
            academic_year = year,
            grade__isnull=False
        ).select_related("courses_id", "grade")

        total_grade_points = 0
        total_course_units = 0

        for courses in course_enrollment:
            if courses.grade and courses.courses_id.units:
                total_grade_points += courses.grade.grade_points * courses.courses_id.units
                total_course_units += courses.courses_id.units

        return round(total_grade_points / total_course_units, 2) if total_course_units > 0 else 0
        

    def get_cumulative_gpa(self, year=None, semester=None):
        '''Get CGPA for a specific semster'''
        course_enrollment = StudentCourses.objects.filter(
            student_id = self,
            grade__isnull=False
        ).select_related("courses_id", "grade")

        first_semester_total_grade_points = 0
        first_semester_total_course_units = 0

        second_semester_total_grade_points = 0
        second_semester_total_course_units = 0



        
        if year and semester:
            course_enrollment = course_enrollment.filter(
                models.Q(year__lt=year) |
                models.Q(year=year, semester__lte=semester)
            )


            for courses in course_enrollment:
                if courses.grade and courses.courses_id:
                    first_semester_total_grade_points += courses.grade.grade_points * courses.courses_id.units
                    first_semester_total_course_units += courses.courses_id.units
        
        else:
             for courses in course_enrollment:
                if courses.semester == 1:
                    if courses.grade and courses.courses_id:
                        first_semester_total_grade_points += courses.grade.grade_points * courses.courses_id.units
                        first_semester_total_course_units += courses.courses_id.units

                elif courses.semester == 2:
                    if courses.grade and courses.courses_id:
                        second_semester_total_grade_points += courses.grade.grade_points * courses.courses_id.units
                        second_semester_total_course_units += courses.courses_id.units

                    
        total_grade_points = first_semester_total_grade_points + second_semester_total_grade_points
        total_course_units = first_semester_total_course_units + second_semester_total_course_units

        return round(total_grade_points / total_course_units, 2) if first_semester_total_course_units and second_semester_total_course_units > 0 else 0.00


        
    def get_academic_progress(self):
        """Get GPA for each semester and overal CGPA"""
        semesters = StudentCourses.objects.filter(
            student_id=self
        ).values("academic_year", "semester").distinct().order_by("academic_year", "semester")

        progress = []

        for semester in semesters:
            gpa = self.get_semester_gpa(semester['semester'], semester['academic_year'])

            progress.append({
                "semester": semester["semester"],
                "year": semester["academic_year"],
                "gpa": gpa
            })

        cgpa = self.get_cumulative_gpa()

        return {
            "semester_gpas": progress,
            "cgpa": cgpa
        }


class GradeScale(models.Model):
    grade = models.CharField(max_length=2)
    grade_points = models.IntegerField()
    description = models.CharField(max_length=10)


    def __str__(self) -> str:
        return f"{self.grade}"
    



class StudentCourses(models.Model):
    SEMESTER = (
        (1, "1st semester"),
        (2, "2nd semester")
    )

    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    courses_id = models.ForeignKey(Courses, on_delete=models.CASCADE)
    grade = models.ForeignKey(GradeScale, on_delete=models.SET_NULL, null=True, blank=True)
    semester = models.IntegerField(choices=SEMESTER, default=1)
    academic_year = models.IntegerField()

    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    class Meta:
        unique_together = ["student_id", "courses_id", "semester", "academic_year"]

    def __str__(self) -> str:
        return f"{self.student_id} - {self.courses_id} ({self.get_semester_display()}) {self.academic_year}"
    
    @property
    def grade_points(self):
        if self.grade and self.courses_id.units:
            return self.grade.grade_points * self.courses_id.units
        
        return 0
        
