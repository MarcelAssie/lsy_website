from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from authentication.models import User, Teacher
from administration.models import Subject
from django.shortcuts import render
from django.db import models

#------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------- GESTION ENSEIGNANTS ----------------------------------------------------------------
@staff_member_required
def manage_teachers(request):
    user = request.user
    return render(request, 'admin_teacher/manage_teachers.html',{'user': user})
@staff_member_required
def teachers_by_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    teachers = Teacher.objects.filter(matiere=subject)
    return render(request, 'admin_teacher/teachers_by_subject.html', {'subject': subject, 'teachers': teachers})
@staff_member_required
def teacher_details(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    return render(request, 'admin_teacher/teacher_details.html', {'teacher': teacher})

@staff_member_required
def search_teachers(request):
    teachers = User.objects.filter(is_teacher=True)
    if request.method == "GET":
        name = request.GET.get('recherche')
        if name:
            teachers = teachers.filter(
                models.Q(first_name__icontains=name) | models.Q(last_name__icontains=name))
    return render(request, 'admin_teacher/manage_teachers.html', {'teachers': teachers})

@staff_member_required
def teacher_details2(request, teacher_id):
    user = get_object_or_404(User, id=teacher_id, is_teacher=True)
    teacher = get_object_or_404(Teacher, user=user)
    return render(request, 'admin_teacher/teacher_details.html', {'teacher': teacher})