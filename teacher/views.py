from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import update_session_auth_hash
from authentication.models import Teacher, Class, Student
from administration.models import Note, Subject, TeacherSchedule
from messagerie.models import Message
from administration.forms import NoteFormForTeacher, AbsenceForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Avg



@login_required
def teacher_profile(request):
    teacher = Teacher.objects.get(user=request.user)
    return render(request, 'teacher/teacher_profile.html', {'teacher': teacher})

@login_required
def teacher_classes_view(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    classes = teacher.classes.all()
    return render(request, 'teacher/teacher_classes.html', {'classes': classes})


@login_required
def class_students_view(request, class_id):
    teacher = get_object_or_404(Teacher, user=request.user)
    classe = get_object_or_404(Class, id=class_id)
    students = Student.objects.filter(classe=classe)
    selected_student = None
    notes = None
    subject = None
    average_score = None  # Ajouter une variable pour la moyenne

    if 'student_id' in request.GET:
        selected_student = get_object_or_404(Student, id=request.GET['student_id'])
        subject = teacher.matiere
        if subject:
            notes = Note.objects.filter(student=selected_student, subject=subject)
            # Calculer la moyenne des notes
            if notes.exists():
                average_score = notes.aggregate(Avg('score'))['score__avg']

    return render(request, 'teacher/teacher_class_students.html', {
        'classe': classe,
        'students': students,
        'selected_student': selected_student,
        'notes': notes,
        'subject': subject,
        'average_score': average_score,
    })



@login_required
def add_note_view(request, student_id, subject_id):
    student = get_object_or_404(Student, id=student_id)
    subject = get_object_or_404(Subject, id=subject_id)
    teacher = get_object_or_404(Teacher, user=request.user)
    if request.method == 'POST':
        form = NoteFormForTeacher(request.POST, user=request.user)
        if form.is_valid():
            note = form.save(commit=False)
            note.student = student
            note.subject = teacher.matiere  # Utiliser la matière de l'enseignant
            note.save()
            return redirect('teacher-class-students', class_id=student.classe.id)
    else:
        form = NoteFormForTeacher(user=request.user)

    return render(request, 'teacher/teacher_add_note.html', {'form': form})


@login_required
def edit_note_view(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if request.method == 'POST':
        form = NoteFormForTeacher(request.POST, instance=note, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('teacher-class-students', class_id=note.student.classe.id)
    else:
        form = NoteFormForTeacher(instance=note, user=request.user)
    return render(request, 'teacher/teacher_edit_note.html', {'form': form, 'note': note})


@login_required
def delete_note_view(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    student_id = note.student.id
    if request.method == 'POST':
        note.delete()
        return redirect('teacher-class-students', class_id=note.student.classe.id)
    return render(request, 'teacher/teacher_delete_note.html', {'note': note})


@login_required
def teacher_change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Met à jour la session de l'utilisateur pour éviter la déconnexion
            messages.success(request, 'Votre mot de passe a été mis à jour avec succès.')
            return redirect('teacher-profile')  # Fonction de redirection en fonction de l'utilisateur
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'teacher/teacher_change_password.html', {'form': form})


@login_required
def add_absence_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = AbsenceForm(request.POST)
        if form.is_valid():
            absence = form.save(commit=False)
            absence.student = student
            absence.save()
            return redirect('teacher-class-students', class_id=student.classe.id)
    else:
        form = AbsenceForm(initial={'start_time': timezone.now(), 'end_time': timezone.now()})
    return render(request, 'teacher/teacher_add_absence.html', {'form': form, 'student': student})

@login_required
def teacher_notifications(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    received_messages = teacher.user.received_messages.order_by('-timestamp')
    received_messages.filter(is_read=False).update(is_read=True)
    return render(request, 'teacher/teacher_notifications.html', {'received_messages': received_messages})


@login_required
def teacher_sent_messages(request):
    sent_messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
    return render(request, 'teacher/teacher_sent_messages.html', {'sent_messages': sent_messages})

@login_required
def teacher_schedule(request):
    teacher = request.user.teacher
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
    return render(request, 'teacher/teacher_schedule.html', context)