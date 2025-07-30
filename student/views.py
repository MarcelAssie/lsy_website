from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import user_passes_test, login_required
from administration.models import Note, MATIERE_CHOICES, Coefficient, Schedule, Information
from messagerie.models import Message
from itertools import groupby
from django.shortcuts import render, get_object_or_404, redirect
from authentication.models import Student
from django.http import JsonResponse
from django.db import connections
import json

@login_required
@user_passes_test(lambda user: user.is_student)
def student_profile(request):
    student = Student.objects.get(user=request.user)
    informations = Information.objects.all().order_by('-created_at')
    return render(request, 'student/student_profile.html', {'student': student, 'informations': informations})

@login_required
@user_passes_test(lambda user: user.is_student)
def student_absences(request):
    student = Student.objects.get(user=request.user)
    absences = student.absences.all()
    total_absence_hours = round(sum(absence.duration() for absence in absences), 1)
    return render(request, 'student/student_absences.html', {'student': student, 'total_absence_hours': total_absence_hours})

@login_required
@user_passes_test(lambda user: user.is_student)
def student_schedule(request):
    student = request.user.student
    class_instance = student.classe  # Supposons que chaque étudiant a une classe associée

    # Récupération de l'emploi du temps de la classe de l'élève
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
    return render(request, 'student/student_schedule.html', context)


@login_required
@user_passes_test(lambda user: user.is_student)
def student_notes(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    notes = Note.objects.filter(student=student).order_by('subject__name', '-date')

    # Regrouper les notes par matière
    coefficients = {}
    grouped_notes = {}
    subject_averages = {}
    total_weighted_average = 0
    total_coefficients = 0

    for subject_name, group in groupby(notes, key=lambda note: note.subject.name):
        full_subject_name = next((name for code, name in MATIERE_CHOICES if code == subject_name), subject_name)
        grouped_notes[full_subject_name] = list(group)

        # Calculer la moyenne des notes pour la matière
        subject_notes = grouped_notes[full_subject_name]
        if subject_notes:
            average = sum(note.score for note in subject_notes) / len(subject_notes)
            subject_averages[full_subject_name] = average

            # Calculer la moyenne pondérée pour la moyenne générale
            school_class = student.classe
            coefficient = Coefficient.objects.get(school_class=school_class, subject__name=subject_name).coefficient
            total_weighted_average += average * coefficient
            total_coefficients += coefficient
            coefficients[full_subject_name] = coefficient

    # Calculer la moyenne générale
    general_average = total_weighted_average / total_coefficients if total_coefficients > 0 else 0
    # Calculer le rang de l'élève
    all_students = Student.objects.filter(classe=student.classe)
    student_averages = []
    for st in all_students:
        notes_for_student = Note.objects.filter(student=st)
        total_student_weighted_average = 0
        student_coefficients = 0
        for subject_name, group in groupby(notes_for_student, key=lambda note: note.subject.name):
            subject_notes = list(group)
            if subject_notes:
                average = sum(note.score for note in subject_notes) / len(subject_notes)
                school_class = st.classe
                coefficient = Coefficient.objects.get(school_class=school_class,
                                                      subject__name=subject_name).coefficient
                total_student_weighted_average += average * coefficient
                student_coefficients += coefficient
        student_average = total_student_weighted_average / student_coefficients if student_coefficients > 0 else 0
        student_averages.append((st, student_average))
    student_averages.sort(key=lambda x: x[1], reverse=True)
    student_rank = next((index for index, (st, avg) in enumerate(student_averages) if st == student), None) + 1

    # Récupérer les recommendations de l'IA
    db_connection = connections["default"]
    with db_connection.cursor() as cursor:
        cursor.execute("""
            SELECT summary, recommendations, recommandations_generales
            FROM students_performances
            WHERE id_student = %s
        """, [student.id_student])
        row = cursor.fetchone()

    ai_feedback = None
    if row:
        ai_feedback = {
            'summary': row[0],
            'recommendations': json.loads(row[1]),
            'recommandations_generales': row[2]
        }
    return render(request, 'student/student_notes.html', {
        'student': student,
        'grouped_notes': grouped_notes,
        'subject_averages': subject_averages,
        'general_average': general_average,
        'coefficients': coefficients,
        'student_rank': student_rank,
        "ai_feedback": ai_feedback,
    })


@login_required
@user_passes_test(lambda user: user.is_student)
def student_change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Met à jour la session de l'utilisateur pour éviter la déconnexion
            messages.success(request, 'Votre mot de passe a été mis à jour avec succès.')
            return redirect('student-change-password')  # Fonction de redirection en fonction de l'utilisateur
        else:
            messages.error(request, 'Echec ! Mot de passe inchangé.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'student/student_change_password.html', {'form': form})

@login_required
@user_passes_test(lambda user: user.is_student)
def student_notifications(request):
    student = get_object_or_404(Student, user=request.user)
    received_messages = student.user.received_messages.order_by('-timestamp')
    unread_notifications_count = received_messages.filter(is_read=False).count()
    received_messages.filter(is_read=False).update(is_read=True)
    return render(request, 'student/student_notifications.html', {'received_messages': received_messages, 'unread_notifications_count': unread_notifications_count})


@login_required
@user_passes_test(lambda user: user.is_student)
def unread_notifications_count_student(request):
    student = get_object_or_404(Student, user=request.user)
    count = Message.objects.filter(recipients=student.user,is_read=False).count()
    return JsonResponse({'unread_notifications_count': count})