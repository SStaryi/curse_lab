from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from medical.models import Department, Teacher, Student, Course
import random

class Command(BaseCommand):
    help = 'Populates the database with initial data'

    def handle(self, *args, **kwargs):
        # Очищаем существующие данные
        User.objects.all().delete()
        Department.objects.all().delete()
        Teacher.objects.all().delete()
        Student.objects.all().delete()
        Course.objects.all().delete()

        # Создаем кафедру
        department = Department.objects.create(
            name='ПОВТАС',
            description='Подготовка специалистов в области IT'
        )

        # Создаем преподавателей
        teachers_data = [
            ('Панченко', 'М.', 'В.', 'БД', 'Доцент'),
            ('Островский', 'А.', 'М.', 'ОС', 'Профессор'),
            ('Гаврющенко', 'А.', 'П.', 'Основы ИБ', 'Доцент'),
            ('Осипов', 'О.', 'В.', 'Комп. графика', 'Доцент'),
            ('Балабанова', 'Г.', 'Г.', 'Экономика', 'Доцент'),
            ('Рязанов', 'Ю.', 'Д.', 'ТАиФЯ', 'Профессор'),
            ('Груздева', 'Н.', 'А.', 'Физическая культура', 'Старший преподаватель'),
        ]

        for last_name, first_name, middle_name, subject, position in teachers_data:
            username = f"{last_name.lower()}"
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=f"{username}@example.com",
                password="1"
            )
            Teacher.objects.create(
                user=user,
                department=department,
                position=position,
                academic_degree='Кандидат наук',
                phone=f'+7900{random.randint(1000000,9999999)}'
            )
            # Создаем курс для преподавателя
            Course.objects.create(
                name=subject,
                department=department,
                description=f'Курс {subject}',
                credits=5,
                semester=1
            )

        # Создаем группы студентов
        groups = ['КБ-221', 'КБ-222', 'ВТ-221', 'ВТ-222', 'ПВ-221', 'ПВ-222']
        
        # Добавляем по одному случайному студенту в каждую группу
        for group in groups:
            username = f"student_{group.lower()}"
            user = User.objects.create_user(
                username=username,
                first_name=f"Студент",
                last_name=group,
                email=f"{username}@example.com",
                password="1"
            )
            Student.objects.create(
                user=user,
                group=group,
                student_id=f'STD-{random.randint(10000,99999)}',
                year_of_admission=2022,
                phone=f'+7900{random.randint(1000000,9999999)}'
            )

        # Создаем группу ПВ-223 с реальными студентами
        pv223_students = [
            ('Голуцкий', 'Георгий', 'Заместитель старосты'),
            ('Дмитриев', 'Андрей', ''),
            ('Игнатьев', 'Артур', ''),
            ('Ковалëв', 'Павел', ''),
            ('Лебедев', 'Максим', ''),
            ('Мелехов', 'Артём', 'Староста'),
            ('Паршин', 'Максим', ''),
            ('Пахомов', 'Владислав', ''),
            ('Романов', 'Максим', ''),
            ('Синëв', 'Иван', ''),
            ('Степанов', 'Дмитрий', ''),
            ('Тухтаров', 'Александр', ''),
            ('Чечин', 'Александр', ''),
        ]

        for last_name, first_name, role in pv223_students:
            username = f"{last_name.lower()}_{first_name.lower()}"
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=f"{username}@example.com",
                password="1"
            )
            Student.objects.create(
                user=user,
                group='ПВ-223',
                student_id=f'STD-{random.randint(10000,99999)}',
                year_of_admission=2022,
                phone=f'+7900{random.randint(1000000,9999999)}'
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated database')) 