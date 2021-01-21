from django.db import models
from random import randint


class Student(models.Model):
    first_name = models.CharField(max_length=40, verbose_name='نام')
    last_name = models.CharField(max_length=40, verbose_name='نام خانوادگی')
    student_id = models.CharField(max_length=8, default='-', blank=True, verbose_name='شماره دانشجویی')
    courses = models.ManyToManyField('Course', through='StudentCourse')
    graduated = models.BooleanField(verbose_name='فارغ التحصیل', default=False)

    class Meta:
        verbose_name = "دانشجو"
        verbose_name_plural = "دانشجویان"

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def get_courses(self):
        return ' - '.join(self.courses.values_list('course_name', flat=True))

    get_courses.short_description = 'درس‌ها'

    def save(self, *args, **kwargs):
        self.student_id = randint(10**7, 10**8)
        super().save(*args, **kwargs)


class Course(models.Model):
    week = [
        ('Saturday', 'شنبه'),
        ('Sunday', 'یک شنبه'),
        ('Monday', 'دو شنبه'),
        ('Tuesday', 'سه شنبه'),
        ('Wednesday', 'چهار شنبه'),
        ('Thursday', 'پنج شنبه'),
        ('Friday', 'جمعه')
    ]
    course_name = models.CharField(max_length=40, verbose_name='نام درس')
    from_time = models.TimeField(verbose_name='از ساعت', null=True)
    to_time = models.TimeField(verbose_name='تا ساعت', null=True)
    day_of_week = models.CharField(verbose_name='روز هفته', max_length=10, choices=week, default=week[0][0])
    professor = models.ForeignKey('Professor', null=True, on_delete=models.SET_NULL, verbose_name='استاد')
    faculty = models.ForeignKey('Faculty', null=True, on_delete=models.CASCADE, verbose_name='دانشکده')
    room = models.ForeignKey('Room', null=True, on_delete=models.SET_NULL, verbose_name='اتاق')

    class Meta:
        verbose_name = "درس"
        verbose_name_plural = "دروس"

    def __str__(self):
        return self.course_name


class Professor(models.Model):
    first_name = models.CharField(max_length=40, verbose_name='نام')
    last_name = models.CharField(max_length=40, verbose_name='نام خانوادگی')
    email = models.EmailField(max_length=80, verbose_name='ایمیل')
    website = models.URLField(max_length=80, verbose_name='وب سایت')

    class Meta:
        verbose_name = "استاد"
        verbose_name_plural = "اساتید"

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def full_name(self):
        return self.__str__()

    full_name.short_description = 'نام و نام خانوادگی'

    def professor_courses(self):
        return ' - '.join(self.course_set.values_list('course_name', flat=True))

    professor_courses.short_description = 'دروس ارائه شده توسط استاد'


class Faculty(models.Model):
    name = models.CharField(max_length=40, verbose_name='دانشکده')

    class Meta:
        verbose_name = "دانشکده"
        verbose_name_plural = "دانشکده‌ها"

    def __str__(self):
        return 'دانشکده ' + self.name

    def faculty_courses(self):
        return ' - '.join(self.course_set.values_list('course_name', flat=True))

    faculty_courses.short_description = 'دروس ارائه شده در دانشکده'


class Room(models.Model):
    name = models.CharField(max_length=40, verbose_name='اتاق')
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, verbose_name='دانشکده')

    class Meta:
        verbose_name = "اتاق"
        verbose_name_plural = "اتاق‌ها"

    def __str__(self):
        return 'اتاق ' + self.name + ': ' + self.faculty.name

    def room_faculty(self):
        return self.faculty.name

    room_faculty.short_description = 'دانشکده'


class StudentCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='نام دانشجو')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='نام درس')
    grade = models.FloatField(verbose_name='نمره درس')

    class Meta:
        verbose_name = "دانشجو-درس"
        verbose_name_plural = "دانشجویان-دروس"

    def __str__(self):
        return str(self.student) + ': ' + str(self.course) + ' = ' + str(self.grade)
