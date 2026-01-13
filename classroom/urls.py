"""
URL patterns for the Classroom app.

Routes:
- /: Landing page
- /student/<room_name>/: Student interface
- /teacher/<room_name>/: Teacher dashboard
"""

from django.urls import path
from . import views

app_name = 'classroom'

urlpatterns = [
    # Landing page
    path('', views.index, name='index'),
    
    # Student room - where students join and raise hands
    # URL: /student/room1/?name=Ritik
    path('student/<str:room_name>/', views.student_room, name='student_room'),
    
    # Teacher dashboard - where teachers see and manage raised hands
    # URL: /teacher/room1/?name=Teacher
    path('teacher/<str:room_name>/', views.teacher_dashboard, name='teacher_dashboard'),
]
