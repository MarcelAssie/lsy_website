from django.contrib.auth.decorators import user_passes_test, login_required
from authentication.models import Teacher
from administration.models import Subject
from django.shortcuts import render, get_object_or_404, redirect
from django.db import models
from django.contrib import messages

#------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------- GESTION ENSEIGNANTS ----------------------------------------------------------------
@login_required
@user_passes_test(lambda user: user.is_superuser)
def manage_teachers(request):
    user = request.user
    return render(request, 'admin_teacher/manage_teachers.html',{'user': user})
@login_required
@user_passes_test(lambda user: user.is_superuser)
def teachers_by_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    teachers = Teacher.objects.filter(matiere=subject)
    return render(request, 'admin_teacher/teachers_by_subject.html', {'subject': subject, 'teachers': teachers})
@login_required
@user_passes_test(lambda user: user.is_superuser)
def teacher_details(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    return render(request, 'admin_teacher/teacher_details.html', {'teacher': teacher})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def search_teachers(request):
    name = request.GET.get('recherche')
    if request.method == "GET":
        if name:
            teachers = Teacher.objects.filter(
                models.Q(user__first_name__icontains=name) | models.Q(user__last_name__icontains=name))
    else:
        teachers = Teacher.objects.all()
    return render(request, 'admin_teacher/manage_teachers.html', {'teachers': teachers})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def delete_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    user = teacher.user
    if request.method == "POST":
        user.delete()
        messages.success(request, 'L\'enseignant a été supprimé avec succès.')
        return redirect('list-subjects')
    return redirect('teacher-details', teacher_id=teacher_id)
@login_required
@user_passes_test(lambda user: user.is_superuser)
def delete_confirm_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    return render(request, 'admin_teacher/delete_confirm_teacher.html', {'teacher': teacher})

