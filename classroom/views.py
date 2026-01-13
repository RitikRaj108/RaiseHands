"""
Views for RaiseHand Lite

This module provides simple views to render the student and teacher interfaces.
Each view:
1. Receives a room_name parameter from the URL
2. Passes the room_name to the template for WebSocket connection
"""

from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    """
    Landing page with links to create/join rooms.
    """
    return render(request, 'classroom/index.html')


def student_room(request, room_name):
    """
    Render the Student Room interface.
    
    Students see:
    - A big "Raise Hand" button
    - Their current status (Hand Raised / Hand Down)
    - Notification when teacher acknowledges
    
    Args:
        request: HTTP request object
        room_name: Classroom identifier from URL
    """
    # Get student name from query params or session
    student_name = request.GET.get('name', '')
    
    return render(request, 'classroom/student.html', {
        'room_name': room_name,
        'student_name': student_name
    })


def teacher_dashboard(request, room_name):
    """
    Render the Teacher Dashboard interface.
    
    Teachers see:
    - Real-time list of students with raised hands
    - Count of currently raised hands
    - Button to dismiss/acknowledge each hand
    
    Args:
        request: HTTP request object
        room_name: Classroom identifier from URL
    """
    teacher_name = request.GET.get('name', 'Teacher')
    
    return render(request, 'classroom/teacher.html', {
        'room_name': room_name,
        'teacher_name': teacher_name
    })
