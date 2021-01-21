from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Count
from django.urls import reverse
from django.views import generic
from django.forms import formset_factory
from .models import Course, Student, StudentCourse
from .forms import StudentCourseForm, NewStudentCourseForm, NewStudentCourseFormset, StudentForm


def index(request):
    return render(request, 'lms/base_page.html')


# def studentes(request):
#     studentes = Student.objects.all()
#     return render(request, 'lms/studentes.html', {'studentes': studentes})

class Studentes(generic.ListView):
    template_name = 'lms/studentes.html'
    context_object_name = 'student_list'

    def get_queryset(self):
        return Student.objects.all()


# def courses(request):
#     student_num_per_course = StudentCourse.objects.values('course').annotate(num=Count('course')).values_list(
#         'course__course_name', 'num').order_by('course__course_name')
#     return render(request, 'lms/courses.html', {'student_num_per_course': student_num_per_course})

class Courses(generic.ListView):
    template_name = 'lms/courses.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        return StudentCourse.objects.values('course').annotate(num=Count('course')).values_list(
            'course__course_name', 'num').order_by('course__course_name')


# def student_course(request):
#     course_num = StudentCourse.objects.values('course').annotate(num=Count('course')).values_list(
#         'num', 'course__course_name').order_by('course__course_name')
#     student_course = StudentCourse.objects.values('course').values_list(
#         'course__course_name',
#         'student__first_name',
#         'student__last_name',
#         'grade'
#     ).order_by(
#         'course__course_name',
#         'student__first_name'
#     )
#     student_course_dict = {c_n[1]: [(x[1] + ' ' + x[2], x[3]) for x in student_course if x[0] == c_n[1]] for c_n in
#                            course_num}
#     return render(request, 'lms/student_course.html', {'student_course_dict': student_course_dict})


class Graids(generic.ListView):
    template_name = 'lms/student_course.html'
    context_object_name = 'graids'

    def get_queryset(self):
        course_num = StudentCourse.objects.values('course').annotate(num=Count('course')).values_list(
            'num', 'course__course_name').order_by('course__course_name')
        student_course = StudentCourse.objects.values('course').values_list(
            'course__course_name',
            'student__first_name',
            'student__last_name',
            'grade'
        ).order_by(
            'course__course_name',
            'student__first_name'
        )
        graids_dict = {c_n[1]: [(x[1] + ' ' + x[2], x[3]) for x in student_course if x[0] == c_n[1]] for c_n in
                       course_num}
        return graids_dict


# def register(request):
#     if request.method == 'GET':
#         return render(request, 'lms/register_form.html')
#     elif request.method == 'POST':
#         student = Student.objects.filter(first_name=request.POST['name'], last_name=request.POST['family'])
#         if not student:
#             student = Student.objects.create(first_name=request.POST['name'], last_name=request.POST['family'])
#         else:
#             student = student[0]
#         return HttpResponseRedirect(reverse('lms:detail', args=(student.id,)))


def register(request):
    if request.method == 'POST':
        student_form = StudentForm(request.POST)
        student_course_form_set = NewStudentCourseFormset(request.POST)

        if student_course_form_set.is_valid():
            tmp_set = set()
            for student_course_form in student_course_form_set:
                if student_course_form.cleaned_data.get("grade"):
                    if student_course_form.cleaned_data['course'] in tmp_set:
                        student_course_form.add_error(None, 'درس تکراری!')
                    else:
                        tmp_set.add(student_course_form.cleaned_data['course'])

        if student_form.is_valid() and student_course_form_set.is_valid():
            student = student_form.save()
            for student_course_form in student_course_form_set:
                if student_course_form.cleaned_data.get("grade"):
                    std_course_form = student_course_form.save(commit=False)
                    std_course_form.student = student
                    std_course_form.save()
                    student_course_form.save_m2m()
            return HttpResponseRedirect(reverse('lms:graids'))
    else:
        student_form = StudentForm()
        student_course_form_set = NewStudentCourseFormset()

    return render(request, 'lms/register_form.html',
                  {'student_form': student_form, 'formset': student_course_form_set})


class Detail(generic.DetailView):
    model = Student
    template_name = 'lms/detail.html'


def student_cours_graid(request):
    StudentCourseFormset = formset_factory(StudentCourseForm, extra=4)
    if request.method == 'POST':
        formset = StudentCourseFormset(request.POST, request.FILES)

        if formset.is_valid():

            for form in formset:
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                course_name = form.cleaned_data['course_name']
                grade = form.cleaned_data['grade']

                student = Student.objects.filter(first_name=first_name, last_name=last_name)
                course = Course.objects.filter(course_name=course_name)

                if not student:
                    student = Student.objects.create(first_name=first_name, last_name=last_name)
                else:
                    student = student[0]

                if not course:
                    course = Course.objects.create(course_name=course_name)
                else:
                    course = course[0]

                student_course = StudentCourse.objects.filter(student=student, course=course)
                if not student_course:
                    student_course = StudentCourse.objects.create(student=student, course=course, grade=grade)
                else:
                    student_course.update(grade=grade)

            return HttpResponseRedirect(reverse('lms:graids'))
    else:
        formset = StudentCourseFormset()

    return render(request, 'lms/student_cours_graid.html', {'formset': formset})


def new_student_cours_graid(request):
    if request.method == 'POST':
        form = NewStudentCourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('lms:graids'))
    else:
        form = NewStudentCourseForm()
    return render(request, 'lms/new_student_cours_graid.html', {'form': form})


def edit_student_detail(request, id):
    return render(request, 'lms/edit_student_detail.html', {'id': id})
