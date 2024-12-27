import django_filters
from .models import Teacher, Student, Course, Schedule, Grade

class TeacherFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='search_filter', label='Поиск')

    class Meta:
        model = Teacher
        fields = ['search']

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            user__first_name__icontains=value) | queryset.filter(
            user__last_name__icontains=value) | queryset.filter(
            department__name__icontains=value)

class StudentFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='search_filter', label='Поиск')

    class Meta:
        model = Student
        fields = ['search']

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            user__first_name__icontains=value) | queryset.filter(
            user__last_name__icontains=value) | queryset.filter(
            group__icontains=value)

class CourseFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='search_filter', label='Поиск')

    class Meta:
        model = Course
        fields = ['search']

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            name__icontains=value) | queryset.filter(
            department__name__icontains=value)

class ScheduleFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='search_filter', label='Поиск')
    day_of_week = django_filters.ChoiceFilter(choices=Schedule.DAY_CHOICES)

    class Meta:
        model = Schedule
        fields = ['search', 'day_of_week']

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            course__name__icontains=value) | queryset.filter(
            teacher__user__last_name__icontains=value) | queryset.filter(
            room__icontains=value)

class GradeFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='search_filter', label='Поиск')
    date_from = django_filters.DateFilter(field_name='date', lookup_expr='gte', label='Дата с')
    date_to = django_filters.DateFilter(field_name='date', lookup_expr='lte', label='Дата по')

    class Meta:
        model = Grade
        fields = ['search', 'date_from', 'date_to']

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            student__user__last_name__icontains=value) | queryset.filter(
            course__name__icontains=value) | queryset.filter(
            teacher__user__last_name__icontains=value) 