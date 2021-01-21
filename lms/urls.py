from django.urls import path
from . import views

app_name = 'lms'
urlpatterns = [
    path('', views.index, name='index'),
    path('studentes/', views.Studentes.as_view(), name='studentes'),
    path('courses/', views.Courses.as_view(), name='courses'),
    path('graids/', views.Graids.as_view(), name='graids'),
    path('register/', views.register, name='register'),
    path('detail/<int:pk>/', views.Detail.as_view(), name='detail'),
    path('student-cours-graid/', views.student_cours_graid, name='student_cours_graid'),
    path('new-student-cours-graid/', views.new_student_cours_graid, name='new_student_cours_graid'),
    path('edit-student-detail/<int:id>/', views.edit_student_detail, name='edit_student_detail')
]
