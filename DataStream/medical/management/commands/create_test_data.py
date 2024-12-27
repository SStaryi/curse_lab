from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from medical.models import Department, Teacher, Student, Course, Schedule, Grade
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Creates test data for the application'

    def handle(self, *args, **kwargs):
        # Создаем суперпользователя
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', '1')
            self.stdout.write(self.style.SUCCESS('Superuser created'))

        # Создаем кафедры
        departments = [
            Department.objects.create(
                name='ПОВТАС',
                description='Подготовка специалистов в области IT'
            ),
            Department.objects.create(
                name='Кафедра математики',
                description='Фундаментальная математическая подготовка'
            ),
            Department.objects.create(
                name='Кафедра физики',
                description='Изучение физических явлений и законов'
            ),
        ]

        # Создаем преподавателей
        teachers_data = [
            {
                'username': 'ivanov',
                'first_name': 'Иван',
                'last_name': 'Иванов',
                'email': 'ivanov@example.com',
                'position': 'Профессор',
                'academic_degree': 'Доктор наук',
                'department': departments[0],
            },
            {
                'username': 'petrov',
                'first_name': 'Петр',
                'last_name': 'Петров',
                'email': 'petrov@example.com',
                'position': 'Доцент',
                'academic_degree': 'Кандидат наук',
                'department': departments[1],
            },
            {
                'username': 'sidorov',
                'first_name': 'Сидор',
                'last_name': 'Сидоров',
                'email': 'sidorov@example.com',
                'position': 'Старший преподаватель',
                'academic_degree': 'Кандидат наук',
                'department': departments[2],
            },
        ]

        teachers = []
        for teacher_data in teachers_data:
            user = User.objects.create_user(
                username=teacher_data['username'],
                email=teacher_data['email'],
                password='1',
                first_name=teacher_data['first_name'],
                last_name=teacher_data['last_name']
            )
            teacher = Teacher.objects.create(
                user=user,
                department=teacher_data['department'],
                position=teacher_data['position'],
                academic_degree=teacher_data['academic_degree'],
                phone=f'+7900{random.randint(1000000,9999999)}'
            )
            teachers.append(teacher)

        # Создаем студентов
        groups = ['ИТ-201', 'ИТ-202', 'МТ-201', 'ФЗ-201']
        students = []
        for i in range(20):
            username = f'student{i+1}'
            first_name = random.choice(['Александр', 'Михаил', 'Дмитрий', 'Анна', 'Елена', 'Мария'])
            last_name = random.choice(['Смирнов', 'Кузнецов', 'Попов', 'Соколов', 'Лебедев', 'Козлов'])
            group = random.choice(groups)
            
            user = User.objects.create_user(
                username=username,
                email=f'{username}@example.com',
                password='1',
                first_name=first_name,
                last_name=last_name
            )
            
            student = Student.objects.create(
                user=user,
                group=group,
                student_id=f'STD-{random.randint(10000,99999)}',
                year_of_admission=random.choice([2021, 2022, 2023]),
                phone=f'+7900{random.randint(1000000,9999999)}'
            )
            students.append(student)

        # Создаем курсы
        courses_data = [
            ('Программирование', departments[0], 'Основы программирования', 5),
            ('Базы данных', departments[0], 'Проектирование и разработка БД', 4),
            ('Высшая математика', departments[1], 'Математический анализ', 6),
            ('Алгебра', departments[1], 'Линейная алгебра', 4),
            ('Физика', departments[2], 'Общая физика', 5),
            ('Механика', departments[2], 'Теоретическая механика', 4),
        ]

        courses = []
        for name, dept, desc, credits in courses_data:
            course = Course.objects.create(
                name=name,
                department=dept,
                description=desc,
                credits=credits,
                semester=random.randint(1, 8)
            )
            courses.append(course)

        # Создаем расписание
        for course in courses:
            for _ in range(2):  # 2 занятия в неделю для каждого курса
                Schedule.objects.create(
                    course=course,
                    teacher=random.choice(teachers),
                    day_of_week=str(random.randint(1, 6)),
                    start_time=f'{random.randint(8,17):02d}:00',
                    end_time=f'{random.randint(9,18):02d}:00',
                    room=f'{random.randint(100,999)}',
                    lesson_type=random.choice(['LECTURE', 'PRACTICE', 'LAB']),
                    group=random.choice(groups)
                )

        # Создаем оценки
        for student in students:
            for course in random.sample(courses, k=random.randint(2, 5)):
                Grade.objects.create(
                    student=student,
                    course=course,
                    grade=random.choice(['5', '4', '3', '2']),
                    date=datetime.now().date() - timedelta(days=random.randint(0, 60)),
                    teacher=random.choice(teachers),
                    comments=random.choice(['Отлично!', 'Хорошая работа', 'Нужно больше стараться', ''])
                )

        self.stdout.write(self.style.SUCCESS('Successfully created test data')) 