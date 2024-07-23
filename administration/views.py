from django.shortcuts import redirect,get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import Subject, Coefficient, Class, Schedule,TeacherSchedule
from authentication.models import Teacher
from messagerie.models import Message
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render
from .forms import CoefficientForm, ClassSelectionForm, ScheduleStudentForm, ScheduleTeacherForm

@staff_member_required
def admin_profile(request):
    user = request.user
    return render(request, 'administration/admin_profile.html',{'user': user})

@staff_member_required
def admin_notifications(request):
    received_messages = Message.objects.filter(recipients=request.user).order_by('-timestamp')
    received_messages.filter(is_read=False).update(is_read=True)
    return render(request, 'administration/admin_notifications.html', {'received_messages': received_messages})

@staff_member_required
def admin_sent_messages(request):
    sent_messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
    return render(request, 'administration/admin_sent_messages.html', {'sent_messages': sent_messages})

@staff_member_required
def admin_change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Votre mot de passe a été mis à jour avec succès.')
            return redirect('admin-profile')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'administration/admin_change_password.html', {'form': form})

@staff_member_required
def list_classes(request):
    classes = Class.objects.all()
    return render(request, 'administration/list_classes.html', {'classes': classes})

@staff_member_required
def list_subjects(request):
    matieres = Subject.objects.all()
    return render(request, 'administration/list_subjects.html', {'matieres': matieres})

@staff_member_required
def configuration(request):
    return render(request, 'administration/configuration.html')

@staff_member_required
def coefficients_matieres(request):
    if request.method == 'POST':
        form = ClassSelectionForm(request.POST)
        if form.is_valid():
            selected_class = form.cleaned_data['school_class']
            return redirect('manage-coefficients', class_id=selected_class.id)
    else:
        form = ClassSelectionForm()

    return render(request, 'administration/coefficients_matieres.html', {'form': form})
@staff_member_required
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
@staff_member_required
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
@staff_member_required
def schedule_class_list(request):
    classes = Class.objects.all()
    return render(request, 'administration/schedule_list_classes.html', {'classes': classes})
@staff_member_required
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

@staff_member_required
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

@staff_member_required
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


@staff_member_required
def schedule_teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'administration/schedule_list_teachers.html', {'teachers': teachers})

@staff_member_required
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

@staff_member_required
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

@staff_member_required
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

