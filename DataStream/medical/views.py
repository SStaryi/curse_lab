from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import Department, Teacher, Student, Course, Schedule, Grade
from django.contrib import messages
from .forms import (DepartmentForm, TeacherForm, StudentForm, CourseForm, 
                   ScheduleForm, GradeForm)
from django.urls import reverse
from .filters import TeacherFilter, StudentFilter, CourseFilter, ScheduleFilter, GradeFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
import json
import csv
from django.http import HttpResponse
from openpyxl import Workbook
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Функция проверки является ли пользователь администратором
def is_admin(user):
    return user.is_superuser

# Функция проверки является ли пользователь преподавателем
def is_teacher(user):
    return hasattr(user, 'teacher')

# Функция проверки является ли пользователь студентом
def is_student(user):
    return hasattr(user, 'student')

# Декоратор для проверки прав администратора
def admin_required(view_func):
    decorated_view = login_required(user_passes_test(is_admin)(view_func))
    return decorated_view

# Декоратор для проверки прав преподавателя
def teacher_required(view_func):
    decorated_view = login_required(user_passes_test(is_teacher)(view_func))
    return decorated_view

@login_required
def dashboard(request):
    """Панель управления для авторизованных пользователей"""
    if is_admin(request.user):
        return render(request, 'medical/admin_dashboard.html', {
            'total_teachers': Teacher.objects.count(),
            'total_students': Student.objects.count(),
            'total_courses': Course.objects.count(),
            'recent_users': User.objects.order_by('-date_joined')[:5],
        })
    
    elif is_teacher(request.user):
        teacher = request.user.teacher
        return render(request, 'medical/teacher_dashboard.html', {
            'teacher': teacher,
            'my_schedule': Schedule.objects.filter(teacher=teacher).order_by('day_of_week', 'start_time'),
            'my_courses': Course.objects.filter(schedule__teacher=teacher).distinct(),
            'recent_grades': Grade.objects.filter(course__schedule__teacher=teacher).order_by('-date')[:5]
        })
    
    elif is_student(request.user):
        student = request.user.student
        return render(request, 'medical/student_dashboard.html', {
            'student': student,
            'my_schedule': Schedule.objects.filter(group=student.group).order_by('day_of_week', 'start_time'),
            'my_grades': Grade.objects.filter(student=student).order_by('-date')[:5],
            'my_courses': Course.objects.filter(schedule__group=student.group).distinct()
        })
    
    return redirect('medical:home')

@login_required
def schedule_list(request):
    schedule_filter = ScheduleFilter(
        request.GET, 
        queryset=Schedule.objects.all().order_by('day_of_week', 'start_time')
    )
    return render(request, 'medical/schedule_list.html', {
        'filter': schedule_filter,
        'schedules': schedule_filter.qs
    })

@admin_required
def teacher_list(request):
    teacher_filter = TeacherFilter(request.GET, queryset=Teacher.objects.all())
    return render(request, 'medical/teacher_list.html', {
        'filter': teacher_filter,
        'teachers': teacher_filter.qs
    })

@admin_required
def student_list(request):
    """Список студентов"""
    student_filter = StudentFilter(request.GET, queryset=Student.objects.all())
    return render(request, 'medical/student_list.html', {
        'filter': student_filter,
        'students': student_filter.qs,
        'title': 'Список студентов'  # Добавляем заголовок
    })

@login_required
def course_list(request):
    course_filter = CourseFilter(request.GET, queryset=Course.objects.all())
    return render(request, 'medical/course_list.html', {
        'filter': course_filter,
        'courses': course_filter.qs
    })

@teacher_required
def grade_list(request):
    grade_filter = GradeFilter(
        request.GET, 
        queryset=Grade.objects.all().order_by('-date')
    )
    return render(request, 'medical/grade_list.html', {
        'filter': grade_filter,
        'grades': grade_filter.qs
    })

# CRUD для преподавателей
@admin_required
def teacher_create(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Преподаватель успешно добавлен')
            return redirect('medical:teacher_list')
    else:
        form = TeacherForm()
    return render(request, 'medical/form_template.html', {
        'form': form,
        'title': 'Добавление преподавателя',
        'cancel_url': reverse('medical:teacher_list')
    })

@admin_required
def teacher_edit(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные преподавателя обновлены')
            return redirect('medical:teacher_list')
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'medical/form_template.html', {
        'form': form,
        'title': f'Редактирование преподавателя: {teacher.user.get_full_name()}',
        'cancel_url': reverse('medical:teacher_list')
    })

@admin_required
def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        teacher.delete()
        messages.success(request, 'Преподаватель удален')
        return redirect('medical:teacher_list')
    return render(request, 'medical/teacher_confirm_delete.html', {'teacher': teacher})

# Аналогичные функции для студентов
@admin_required
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Студент успешно добавлен')
            return redirect('medical:student_list')
    else:
        form = StudentForm()
    return render(request, 'medical/form_template.html', {
        'form': form,
        'title': 'Добавление студента',
        'cancel_url': reverse('medical:student_list')
    })

@admin_required
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные студента обновлены')
            return redirect('medical:student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'medical/form_template.html', {
        'form': form,
        'title': f'Редактирование студента: {student.user.get_full_name()}',
        'cancel_url': reverse('medical:student_list')
    })

@admin_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Студент удален')
        return redirect('medical:student_list')
    return render(request, 'medical/confirm_delete.html', {
        'object': student,
        'cancel_url': reverse('medical:student_list')
    })

# Аналогичные функции для курсов, расписания и оценок

# CRUD для курсов
@admin_required
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Курс успешно добавлен')
            return redirect('medical:course_list')
    else:
        form = CourseForm()
    return render(request, 'medical/form_template.html', {
        'form': form,
        'title': 'Добавление курса',
        'cancel_url': reverse('medical:course_list')
    })

@admin_required
def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Курс обновлен')
            return redirect('medical:course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'medical/form_template.html', {
        'form': form,
        'title': 'Редактирование курса',
        'cancel_url': reverse('medical:course_list')
    })

@admin_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Курс удален')
        return redirect('medical:course_list')
    return render(request, 'medical/confirm_delete.html', {
        'object': course,
        'cancel_url': reverse('medical:course_list')
    })

# CRUD для расписания
@admin_required
def schedule_create(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Занятие добавлено в расписание')
            return redirect('medical:schedule_list')
    else:
        form = ScheduleForm()
    return render(request, 'medical/form_template.html', {
        'form': form,
        'title': 'Добавление занятия',
        'cancel_url': reverse('medical:schedule_list')
    })

@admin_required
def schedule_edit(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk)
    if request.method == 'POST':
        form = ScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            messages.success(request, 'Расписание обновлено')
            return redirect('medical:schedule_list')
    else:
        form = ScheduleForm(instance=schedule)
    return render(request, 'medical/form_template.html', {
        'form': form,
        'title': 'Редактирование занятия',
        'cancel_url': reverse('medical:schedule_list')
    })

@admin_required
def schedule_delete(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk)
    if request.method == 'POST':
        schedule.delete()
        messages.success(request, 'Занятие удалено из расписания')
        return redirect('medical:schedule_list')
    return render(request, 'medical/confirm_delete.html', {
        'object': schedule,
        'cancel_url': reverse('medical:schedule_list')
    })

# CRUD для оценок
@teacher_required
def grade_create(request):
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Оценка добавлена')
            return redirect('medical:grade_list')
    else:
        form = GradeForm()
    return render(request, 'medical/form_template.html', {
        'form': form,
        'title': 'Добавление оценки',
        'cancel_url': reverse('medical:grade_list')
    })

@teacher_required
def grade_edit(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    if request.method == 'POST':
        form = GradeForm(request.POST, instance=grade)
        if form.is_valid():
            form.save()
            messages.success(request, 'Оценка обновлена')
            return redirect('medical:grade_list')
    else:
        form = GradeForm(instance=grade)
    return render(request, 'medical/form_template.html', {
        'form': form,
        'title': 'Редактирование оценки',
        'cancel_url': reverse('medical:grade_list')
    })

@teacher_required
def grade_delete(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    if request.method == 'POST':
        grade.delete()
        messages.success(request, 'Оценка удалена')
        return redirect('medical:grade_list')
    return render(request, 'medical/confirm_delete.html', {
        'object': grade,
        'cancel_url': reverse('medical:grade_list')
    })

@login_required
def student_profile(request, pk=None):
    if pk:
        # Просмотр профиля другого студента (доступно только преподавателям)
        if not hasattr(request.user, 'teacher'):
            messages.error(request, 'Доступ запрещен')
            return redirect('medical:home')
        student = get_object_or_404(Student, pk=pk)
    else:
        # Просмотр своего профиля
        if not hasattr(request.user, 'student'):
            messages.error(request, 'Вы не являетесь студентом')
            return redirect('medical:home')
        student = request.user.student

    grades = Grade.objects.filter(student=student).order_by('-date')
    schedule = Schedule.objects.filter(group=student.group).order_by('day_of_week', 'start_time')
    
    return render(request, 'medical/student_profile.html', {
        'student': student,
        'grades': grades,
        'schedule': schedule
    })

@login_required
def student_schedule(request):
    if not hasattr(request.user, 'student'):
        messages.error(request, 'Вы не являетесь студентом')
        return redirect('medical:home')
    
    schedule = Schedule.objects.filter(
        group=request.user.student.group
    ).order_by('day_of_week', 'start_time')
    
    return render(request, 'medical/student_schedule.html', {
        'schedules': schedule
    })

@login_required
def student_grades(request):
    student = request.user.student
    grades = Grade.objects.filter(student=student).order_by('-date')
    
    # Вычисляем статистику
    total_grades = len(grades)
    if total_grades > 0:
        # Преобразуем строковые оценки в числа и считаем средне
        average_grade = sum(float(grade.grade) for grade in grades) / total_grades
        average_grade = "{:.2f}".format(average_grade)
    else:
        average_grade = "0.00"
    
    # Получаем количество уникальных курсов
    unique_courses = set(grade.course.id for grade in grades)
    unique_courses_count = len(unique_courses)
    
    return render(request, 'medical/student_grades.html', {
        'grades': grades,
        'average_grade': average_grade,
        'unique_courses_count': unique_courses_count
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_type = request.POST.get('user_type')
            
            if user_type == 'student':
                Student.objects.create(
                    user=user,
                    group=request.POST.get('group'),
                    student_id=request.POST.get('student_id'),
                    year_of_admission=request.POST.get('year_of_admission'),
                    phone=request.POST.get('phone')
                )
            else:
                Teacher.objects.create(
                    user=user,
                    department_id=request.POST.get('department'),
                    position=request.POST.get('position'),
                    academic_degree=request.POST.get('academic_degree'),
                    phone=request.POST.get('phone'),
                    photo=request.FILES.get('photo')
                )
            
            login(request, user)
            messages.success(request, 'Регистрация успешно завершена!')
            return redirect('medical:home')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {
        'form': form,
        'departments': Department.objects.all()
    })

def home(request):
    """Главная страница сайта с общей информацией"""
    courses = Course.objects.all()[:6]  # Ограничиваем до 6 курсов
    
    stats = {
        'total_teachers': Teacher.objects.count(),
        'total_students': Student.objects.count(),
        'total_courses': Course.objects.count(),
    }
    
    return render(request, 'medical/home.html', {
        'courses': courses,
        'stats': stats,
    }) 

def export_grades(request, format='json'):
    grades = Grade.objects.select_related('student', 'course', 'teacher').all()
    
    if format == 'json':
        data = [{
            'student': grade.student.user.get_full_name(),
            'course': grade.course.name,
            'grade': grade.get_grade_display(),
            'date': grade.date.strftime('%Y-%m-%d'),
            'teacher': grade.teacher.user.get_full_name()
        } for grade in grades]
        
        response = HttpResponse(
            json.dumps(data, indent=2, ensure_ascii=False).encode('utf-8'), 
            content_type='application/json; charset=utf-8'
        )
        response['Content-Disposition'] = 'attachment; filename="grades.json"'
        return response
        
    elif format == 'csv':
        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        response['Content-Disposition'] = 'attachment; filename="grades.csv"'
        
        # Используем точку с запятой как разделитель для Excel
        writer = csv.writer(response, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        
        # Записываем BOM для Excel
        response.write('\ufeff'.encode('utf-8'))
        
        # Заголовки
        writer.writerow(['Студент', 'Курс', 'Оценка', 'Дата', 'Преподаватель'])
        
        # Данные
        for grade in grades:
            writer.writerow([
                grade.student.user.get_full_name(),
                grade.course.name,
                grade.get_grade_display(),
                grade.date.strftime('%d.%m.%Y'),  # Форматируем дату
                grade.teacher.user.get_full_name()
            ])
        return response
        
    elif format == 'xlsx':
        wb = Workbook()
        ws = wb.active
        ws.title = "Оценки"
        
        # Заголовки
        headers = ['Студент', 'Курс', 'Оценка', 'Дата', 'Преподаватель']
        ws.append(headers)
        
        # Данные
        for grade in grades:
            ws.append([
                grade.student.user.get_full_name(),
                grade.course.name,
                grade.get_grade_display(),
                grade.date,
                grade.teacher.user.get_full_name()
            ])
            
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="grades.xlsx"'
        wb.save(response)
        return response
        
    elif format == 'pdf':
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="grades.pdf"'
        
        p = canvas.Canvas(response, pagesize=letter)
        # Поддержка кириллицы в PDF
        p.setFont('Helvetica', 12)
        y = 750
        
        # Заголовок
        p.drawString(50, y, "Отчет по оценкам")
        y -= 20
        
        for grade in grades:
            if y < 50:
                p.showPage()
                p.setFont('Helvetica', 12)
                y = 750
            
            text = f"{grade.student.user.get_full_name()} - {grade.course.name} - {grade.get_grade_display()}"
            p.drawString(50, y, text)
            y -= 15
            
        p.showPage()
        p.save()
        return response 