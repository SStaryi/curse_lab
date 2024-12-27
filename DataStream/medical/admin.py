from django.contrib import admin
from .models import Department, Teacher, Student, Course, Schedule, Grade

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'position', 'academic_degree', 'phone')
    list_filter = ('department', 'position', 'academic_degree')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', 'student_id', 'year_of_admission', 'phone')
    list_filter = ('group', 'year_of_admission')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'student_id', 'phone')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'credits', 'semester')
    list_filter = ('department', 'semester')
    search_fields = ('name', 'description')

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('course', 'teacher', 'day_of_week', 'start_time', 'end_time', 'room', 'group')
    list_filter = ('day_of_week', 'lesson_type', 'group')
    search_fields = ('course__name', 'teacher__user__last_name', 'room', 'group')

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'grade', 'date', 'teacher')
    list_filter = ('grade', 'date', 'course')
    search_fields = ('student__user__last_name', 'course__name', 'teacher__user__last_name') 