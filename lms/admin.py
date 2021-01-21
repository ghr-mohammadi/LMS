from django.contrib import admin
from .models import *


class StudentCourseInline(admin.TabularInline):
    model = StudentCourse
    model.__str__ = lambda self: ''
    extra = 1


class RoomInline(admin.TabularInline):
    model = Room
    # model.__str__ = lambda self: ''
    extra = 1


def make_graduate(modeladmin, request, queryset):
    queryset.update(graduated=True)


make_graduate.short_description = 'اعمال فارغ التحصیلی'


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'first_name', 'last_name', 'get_courses', 'graduated']
    inlines = [StudentCourseInline]
    readonly_fields = ['student_id']
    search_fields = ['first_name', 'last_name']
    actions = [make_graduate]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_name', 'day_of_week', 'from_time', 'to_time', 'faculty', 'professor', 'room']
    list_filter = ['faculty']


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'website', 'professor_courses']


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'faculty_courses']
    inlines = [RoomInline]


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'room_faculty']


@admin.register(StudentCourse)
class StudentCourseAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'grade']
