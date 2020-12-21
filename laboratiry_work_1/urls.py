"""laboratiry_work_1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from final_project import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main_page),
    path('student/', views.student_main_page),
    path('subjectexam/<int:id>/', views.subject_page),
    path('teacher/', views.teacher_main_page),
    path('exams/<int:id>/edit/', views.edit_exam),
    path('exams/<int:id>/delete/', views.delete_exam),
    path('exams/<int:id>/', views.exam_page),
    path('exams/', views.new_exam),
    path('marks/<int:id>/', views.mark),
    path('marks/', views.new_mark),
    path('rector/', views.rector_main_page),
    path('teachers/', views.new_teacher),
    path('subjects/', views.new_subject),
    path('students/', views.new_student),
    path('groups/', views.new_group),
    path('groups/<int:id>/', views.group),
    path('groups/<int:group_id>/student/', views.add_student_to_group),
    path('groups/<int:group_id>/student/delete/', views.delete_student_from_group),
    path('groups/<int:group_id>/subject/', views.add_subject_to_group),
    path('groups/<int:group_id>/subject/delete/', views.delete_subject_from_group),
    path('', include('django.contrib.auth.urls'))
]
