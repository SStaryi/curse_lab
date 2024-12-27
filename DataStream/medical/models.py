from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название кафедры")
    description = models.TextField(blank=True, verbose_name="Описание")
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Кафедра"
        verbose_name_plural = "Кафедры"

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="Кафедра")
    position = models.CharField(max_length=100, verbose_name="Должность")
    academic_degree = models.CharField(max_length=100, verbose_name="Ученая степень")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    photo = models.ImageField(upload_to='teachers/', blank=True, verbose_name="Фото")
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.position}"

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.CharField(max_length=20, verbose_name="Группа")
    student_id = models.CharField(max_length=20, unique=True, verbose_name="Номер студенческого")
    year_of_admission = models.IntegerField(verbose_name="Год поступления")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.group}"

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"

class Course(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название курса")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="Кафедра")
    description = models.TextField(verbose_name="Описание")
    credits = models.IntegerField(verbose_name="Количество кредитов")
    semester = models.IntegerField(verbose_name="Семестр")
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

class Schedule(models.Model):
    DAY_CHOICES = [
        ('1', 'Понедельник'),
        ('2', 'Вторник'),
        ('3', 'Среда'),
        ('4', 'Четверг'),
        ('5', 'Пятница'),
        ('6', 'Суббота'),
        ('7', 'Воскресенье'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='Преподаватель')
    day_of_week = models.CharField(max_length=1, choices=DAY_CHOICES, verbose_name='День недели')
    start_time = models.TimeField(verbose_name='Время начала')
    end_time = models.TimeField(verbose_name='Время окончания')
    room = models.CharField(max_length=50, verbose_name='Аудитория')
    lesson_type = models.CharField(max_length=20, choices=[
        ('LECTURE', 'Лекция'),
        ('PRACTICE', 'Практика'),
        ('LAB', 'Лабораторная'),
    ], verbose_name='Тип занятия')
    group = models.CharField(max_length=50, verbose_name='Группа')

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписание'
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return f'{self.get_day_of_week_display()} {self.start_time}-{self.end_time} {self.course.name}'

class Grade(models.Model):
    GRADE_CHOICES = [
        ('5', 'Отлично'),
        ('4', 'Хорошо'),
        ('3', 'Удовлетворительно'),
        ('2', 'Неудовлетворительно'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Студент")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES, verbose_name="Оценка")
    date = models.DateField(verbose_name="Дата")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="Преподаватель")
    comments = models.TextField(blank=True, verbose_name="Комментарии")
    
    def __str__(self):
        return f"{self.student} - {self.course} - {self.grade}"

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки" 