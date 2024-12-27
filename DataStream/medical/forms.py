from django import forms
from django.contrib.auth.models import User
from .models import Teacher, Student, Course, Schedule, Grade, Department

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class TeacherForm(forms.ModelForm):
    first_name = forms.CharField(label='Имя', max_length=30)
    last_name = forms.CharField(label='Фамилия', max_length=30)
    email = forms.EmailField(label='Email')

    class Meta:
        model = Teacher
        fields = ['department', 'position', 'academic_degree', 'phone', 'photo']

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        if instance:
            initial = kwargs.get('initial', {})
            initial['first_name'] = instance.user.first_name
            initial['last_name'] = instance.user.last_name
            initial['email'] = instance.user.email
            kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        teacher = super().save(commit=False)
        if teacher.user_id:
            user = teacher.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.save()
        if commit:
            teacher.save()
        return teacher

class StudentForm(forms.ModelForm):
    first_name = forms.CharField(label='Имя', max_length=30)
    last_name = forms.CharField(label='Фамилия', max_length=30)
    email = forms.EmailField(label='Email')

    class Meta:
        model = Student
        fields = ['group', 'student_id', 'year_of_admission', 'phone']

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        if instance:
            initial = kwargs.get('initial', {})
            initial['first_name'] = instance.user.first_name
            initial['last_name'] = instance.user.last_name
            initial['email'] = instance.user.email
            kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        student = super().save(commit=False)
        if student.user_id:
            user = student.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.save()
        if commit:
            student.save()
        return student

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'department', 'description', 'credits', 'semester']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['course', 'teacher', 'day_of_week', 'start_time', 'end_time', 
                 'room', 'lesson_type', 'group']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'course', 'grade', 'date', 'teacher', 'comments']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'comments': forms.Textarea(attrs={'rows': 2}),
        } 