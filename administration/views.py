from django.shortcuts import redirect,get_object_or_404, render
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import Subject, Coefficient, Class, Schedule,TeacherSchedule, Information
from authentication.models import Student, Parent, Teacher
from messagerie.models import Message
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Count
from django.http import JsonResponse
from .forms import (CoefficientForm, ClassSelectionForm, ScheduleStudentForm,
                    ScheduleTeacherForm, ClassForm, SubjectForm, InformationForm)

@login_required
@user_passes_test(lambda user: user.is_superuser)
def admin_dashboard(request):
    # Statistiques sur les élèves par classe
    students_per_class = Student.objects.values('classe__name').annotate(count=Count('id')).order_by('classe__name')

    # Statistiques sur les enseignants par matière
    teachers_per_subject = Teacher.objects.values('matiere__name').annotate(count=Count('id')).order_by('matiere__name')

    # Nombre total d'enseignants
    total_teachers = Teacher.objects.count()

    # Nombre total de parents
    total_parents = Parent.objects.count()

    # Nombre total d'élèves
    total_students = Student.objects.count()

    # Passer les données au template
    context = {
        'students_per_class': students_per_class,
        'teachers_per_subject': teachers_per_subject,
        'total_teachers': total_teachers,
        'total_parents': total_parents,
        'total_students': total_students,
    }
    return render(request, 'administration/admin_dashboard.html', context)


@login_required
@user_passes_test(lambda user: user.is_superuser)
def admin_notifications(request):
    received_messages = Message.objects.filter(recipients=request.user).order_by('-timestamp')
    unread_notifications_count = received_messages.filter(is_read=False).count()
    received_messages.filter(is_read=False).update(is_read=True)
    return render(request, 'administration/admin_notifications.html', {
        'received_messages': received_messages,
        'unread_notifications_count': unread_notifications_count
    })
@login_required
@user_passes_test(lambda user: user.is_superuser)
def unread_notifications_count(request):
    count = Message.objects.filter(recipients=request.user, is_read=False).count()
    return JsonResponse({'unread_notifications_count': count})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def admin_sent_messages(request):
    sent_messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
    return render(request, 'administration/admin_sent_messages.html', {'sent_messages': sent_messages})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def admin_change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Votre mot de passe a été mis à jour avec succès.')
            return redirect('admin-change-password')
        else:
            messages.error(request, 'Echec ! Mot de passe inchangé.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'administration/admin_change_password.html', {'form': form})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def list_classes_subjects(request):
    classes = Class.objects.all()
    subjects = Subject.objects.all()
    if request.method == 'POST':
        # Handle the deletion confirmation via POST
        if 'delete_class' in request.POST:
            class_id = request.POST.get('delete_class')
            class_to_delete = get_object_or_404(Class, id=class_id)
            class_to_delete.delete()
        elif 'delete_subject' in request.POST:
            subject_id = request.POST.get('delete_subject')
            subject_to_delete = get_object_or_404(Subject, id=subject_id)
            subject_to_delete.delete()
        return redirect('list-classes-subjects')

    return render(request, 'administration/list_classes_subjects.html', {'classes': classes, 'subjects': subjects})
@login_required
@user_passes_test(lambda user: user.is_superuser)
def add_class(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            class_name = form.cleaned_data['name']
            if Class.objects.filter(name=class_name).exists():
                messages.error(request, "Cette classe existe déjà.")
            else:
                form.save()
                messages.success(request, "Classe ajoutée avec succès.")
                return redirect('add-class')
    else:
        form = ClassForm()
    return render(request, 'administration/add_class.html', {'form': form})
@login_required
@user_passes_test(lambda user: user.is_superuser)
def add_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject_name = form.cleaned_data['name']
            if Subject.objects.filter(name=subject_name).exists():
                messages.error(request, "Cette matière existe déjà.")
            else:
                form.save()
                messages.success(request, "Matière ajoutée avec succès.")
                return redirect('add-subject')
    else:
        form = SubjectForm()
    return render(request, 'administration/add_subject.html', {'form': form})
@login_required
@user_passes_test(lambda user: user.is_superuser)
def delete_class(request, id):
    if request.method == 'POST':
        class_to_delete = get_object_or_404(Class, id=id)
        class_to_delete.delete()
        return redirect('list-classes-subjects')
@login_required
@user_passes_test(lambda user: user.is_superuser)
def delete_subject(request, id):
    if request.method == 'POST':
        subject_to_delete = get_object_or_404(Subject, id=id)
        subject_to_delete.delete()
        return redirect('list-classes-subjects')

@login_required
@user_passes_test(lambda user: user.is_superuser)
def list_classes(request):
    classes = Class.objects.all()
    return render(request, 'administration/list_classes.html', {'classes': classes})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def list_subjects(request):
    matieres = Subject.objects.all()
    return render(request, 'administration/list_subjects.html', {'matieres': matieres})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def configuration(request):
    return render(request, 'administration/configuration.html')

@login_required
@user_passes_test(lambda user: user.is_superuser)
def coefficients_matieres(request):
    if request.method == 'POST':
        form = ClassSelectionForm(request.POST)
        if form.is_valid():
            selected_class = form.cleaned_data['school_class']
            return redirect('manage-coefficients', class_id=selected_class.id)
    else:
        form = ClassSelectionForm()

    return render(request, 'administration/coefficients_matieres.html', {'form': form})
@login_required
@user_passes_test(lambda user: user.is_superuser)
def manage_coefficients(request, class_id):
    school_class = Class.objects.get(id=class_id)
    subjects = Subject.objects.all()

    if request.method == 'POST':
        form = CoefficientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage-coefficients', class_id=class_id)
    else:
        form = CoefficientForm(initial={'school_class': school_class})

    coefficients = Coefficient.objects.filter(school_class=school_class)

    return render(request, 'administration/manage_coefficients.html', {
        'school_class': school_class,
        'subjects': subjects,
        'coefficients': coefficients,
        'form': form
    })
@login_required
@user_passes_test(lambda user: user.is_superuser)
def edit_coefficients(request, coefficient_id):
    coefficient = get_object_or_404(Coefficient, id=coefficient_id)
    if request.method == 'POST':
        form = CoefficientForm(request.POST, instance=coefficient)
        if form.is_valid():
            form.save()
            return redirect('manage-coefficients', class_id=coefficient.school_class.id)
    else:
        form = CoefficientForm(instance=coefficient)
    return render(request, 'administration/edit_coefficients.html', {
        'form': form,
        'coefficient': coefficient
    })
@login_required
@user_passes_test(lambda user: user.is_superuser)
def schedule_class_list(request):
    classes = Class.objects.all()
    return render(request, 'administration/schedule_list_classes.html', {'classes': classes})
@login_required
@user_passes_test(lambda user: user.is_superuser)
def schedule_students_create(request, class_id):
    class_instance = get_object_or_404(Class, id=class_id)
    if request.method == 'POST':
        form = ScheduleStudentForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.class_name = class_instance
            schedule.save()
            return redirect('schedule-students-create', class_id=class_instance.id)  # Redirige vers la même page
    else:
        form = ScheduleStudentForm(initial={'class_name': class_instance})
    return render(request, 'administration/students_schedule_form.html', {'form': form, 'class_instance': class_instance})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def schedule_students_view(request, class_id):
    class_instance = get_object_or_404(Class, id=class_id)
    schedules = Schedule.objects.filter(class_name=class_instance).order_by('start_time')

    days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi']
    time_slots = sorted(set((s.start_time, s.end_time) for s in schedules))

    # Créer une liste de listes pour stocker les emplois du temps
    schedule_matrix = []
    for start_time, end_time in time_slots:
        row = {'time_slot': f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"}
        for day in days:
            row[day] = None
        schedule_matrix.append(row)

    for schedule in schedules:
        time_slot = f"{schedule.start_time.strftime('%H:%M')} - {schedule.end_time.strftime('%H:%M')}"
        for row in schedule_matrix:
            if row['time_slot'] == time_slot:
                row[schedule.day_of_week] = schedule
    context = {
        'class_instance': class_instance,
        'schedule_matrix': schedule_matrix,
        'days': days,
    }
    return render(request, 'administration/students_schedule_view.html', context)

@login_required
@user_passes_test(lambda user: user.is_superuser)
def schedule_students_edit(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)
    class_instance = schedule.class_name  # Récupère l'instance de la classe associée
    if request.method == 'POST':
        form = ScheduleStudentForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            return redirect('schedule-students-edit', schedule_id=schedule.id)  # Redirige vers la même page
    else:
        form = ScheduleStudentForm(instance=schedule)
    return render(request, 'administration/students_schedule_form.html', {'form': form, 'schedule': schedule, 'class_instance': class_instance})


@login_required
@user_passes_test(lambda user: user.is_superuser)
def schedule_teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'administration/schedule_list_teachers.html', {'teachers': teachers})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def schedule_teacher_view(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    schedules = TeacherSchedule.objects.filter(teacher=teacher).order_by('start_time')

    days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi']
    time_slots = sorted(set((s.start_time, s.end_time) for s in schedules))

    # Créer une liste de listes pour stocker les emplois du temps
    schedule_matrix = []
    for start_time, end_time in time_slots:
        row = {'time_slot': f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"}
        for day in days:
            row[day] = None
        schedule_matrix.append(row)

    for schedule in schedules:
        time_slot = f"{schedule.start_time.strftime('%H:%M')} - {schedule.end_time.strftime('%H:%M')}"
        for row in schedule_matrix:
            if row['time_slot'] == time_slot:
                row[schedule.day_of_week] = schedule
    context = {
        'teacher': teacher,
        'schedule_matrix': schedule_matrix,
        'days': days,
    }
    return render(request, 'administration/teacher_schedule_view.html', context)

@login_required
@user_passes_test(lambda user: user.is_superuser)
def schedule_teacher_create(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    if request.method == 'POST':
        form = ScheduleTeacherForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.teacher = teacher
            schedule.save()
            return redirect('schedule-teacher-view', teacher_id=teacher.id)
    else:
        form = ScheduleTeacherForm(initial={'teacher': teacher})
    return render(request, 'administration/teacher_schedule_form.html', {'form': form, 'teacher': teacher})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def schedule_teacher_edit(request, schedule_id):
    schedule = get_object_or_404(TeacherSchedule, id=schedule_id)
    teacher = schedule.teacher
    if request.method == 'POST':
        form = ScheduleTeacherForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            return redirect('schedule-teacher-view', teacher_id=teacher.id)
    else:
        form = ScheduleTeacherForm(instance=schedule)
    return render(request, 'administration/teacher_schedule_form.html', {'form': form, 'teacher': teacher})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def information_list(request):
    informations = Information.objects.all().order_by('-created_at')
    return render(request, 'administration/list_informations.html', {'informations': informations})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def information_add(request):
    if request.method == 'POST':
        form = InformationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('information-list')
    else:
        form = InformationForm()
    return render(request, 'administration/add_information.html', {'form': form})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def information_edit(request, pk):
    information = get_object_or_404(Information, pk=pk)
    if request.method == 'POST':
        form = InformationForm(request.POST, instance=information)
        if form.is_valid():
            form.save()
            return redirect('information-list')
    else:
        form = InformationForm(instance=information)
    return render(request, 'administration/add_information.html', {'form': form})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def information_delete(request, pk):
    information = get_object_or_404(Information, pk=pk)
    if request.method == 'POST':
        information.delete()
        return redirect('information-list')
    return redirect('information-list')