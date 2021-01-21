from django import forms
from .models import StudentCourse, Student
from django.core.exceptions import ValidationError


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name']


class StudentCourseForm(forms.Form):
    first_name = forms.CharField(label='نام', max_length=40)
    last_name = forms.CharField(label='نام خانوداگی', max_length=40)
    course_name = forms.CharField(label='نام درس', max_length=40)
    grade = forms.FloatField(label="نمره", min_value=0.0, max_value=20.0)


class NewStudentCourseForm(forms.ModelForm):
    class Meta:
        model = StudentCourse
        fields = ['student', 'course', 'grade']


class NewStudentCourseForm_2(forms.ModelForm):
    class Meta:
        model = StudentCourse
        fields = ['course', 'grade']

    def clean_grade(self):
        grade = self.cleaned_data['grade']
        if grade < 0 or grade > 20:
            raise ValidationError("نمره نامناسب!")
        else:
            return grade


NewStudentCourseFormset = forms.formset_factory(NewStudentCourseForm_2, extra=4)
