# Generated by Django 5.1.4 on 2024-12-24 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medical', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='schedule',
            options={'ordering': ['day_of_week', 'start_time'], 'verbose_name': 'Расписание', 'verbose_name_plural': 'Расписание'},
        ),
        migrations.AlterField(
            model_name='schedule',
            name='day_of_week',
            field=models.CharField(choices=[('1', 'Понедельник'), ('2', 'Вторник'), ('3', 'Среда'), ('4', 'Четверг'), ('5', 'Пятница'), ('6', 'Суббота'), ('7', 'Воскресенье')], max_length=1, verbose_name='День недели'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='group',
            field=models.CharField(max_length=50, verbose_name='Группа'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='lesson_type',
            field=models.CharField(choices=[('LECTURE', 'Лекция'), ('PRACTICE', 'Практика'), ('LAB', 'Лабораторная')], max_length=20, verbose_name='Тип занятия'),
        ),
    ]
