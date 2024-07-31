from authentication.models import Parent, Student
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404
from administration.models import Note, MATIERE_CHOICES, Coefficient, Information, Schedule
from messagerie.models import Message
from itertools import groupby
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import JsonResponse
from admin_parent.forms import ChoixCreneauForm, ChoixMotifForm
from admin_parent.models import Motif, RendezVous, Creneau



@login_required
@user_passes_test(lambda user: user.is_parent)
def parent_dashboard(request):
    parent = Parent.objects.get(user=request.user)
    informations = Information.objects.all().order_by('-created_at')
    return render(request, 'parent/parent_dashboard.html', {'parent': parent, 'informations': informations})

@login_required
@user_passes_test(lambda user: user.is_parent)
def parent_notifications(request):
    parent = get_object_or_404(Parent, user=request.user)
    received_messages = parent.user.received_messages.order_by('-timestamp')
    unread_notifications_count = received_messages.filter(is_read=False).count()
    received_messages.filter(is_read=False).update(is_read=True)
    return render(request, 'parent/parent_notifications.html', {'received_messages': received_messages, 'unread_notifications_count': unread_notifications_count})

@login_required
@user_passes_test(lambda user: user.is_parent)
def unread_notifications_count_parent(request):
    parent = get_object_or_404(Parent, user=request.user)
    count = Message.objects.filter(recipients=parent.user, is_read=False).count()
    return JsonResponse({'unread_notifications_count': count})

@login_required
@user_passes_test(lambda user: user.is_parent)
def parent_change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Met à jour la session de l'utilisateur pour éviter la déconnexion
            messages.success(request, 'Votre mot de passe a été mis à jour avec succès.')
            return redirect('parent-change-password')  # Fonction de redirection en fonction de l'utilisateur
        else:
            messages.error(request, 'Echec ! Mot de passe inchangé.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'parent/parent_change_password.html', {'form': form})

@login_required
@user_passes_test(lambda user: user.is_parent)
def children_details(request):
    parent = get_object_or_404(Parent, user=request.user)
    notes = []
    absences = []
    student = None
    general_average = 0
    if parent.id_children:
        student = get_object_or_404(Student, id_student=parent.id_children)
        notes = Note.objects.filter(student=student).order_by('subject__name', '-date')
        absences = student.absences.all()
        total_absence_hours = round(sum(absence.duration() for absence in absences), 1)
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

        return render(request, 'parent/children_details.html',
                      {
                          'parent': parent,
                          'student': student,
                          'grouped_notes': grouped_notes,
                          'total_absence_hours': total_absence_hours,
                          'subject_averages': subject_averages,
                          'general_average': general_average,
                          'coefficients': coefficients,
                          'student_rank': student_rank,  # Passer le rang à la template
                      })

    return render(request, 'parent/children_details.html', {'student': student, 'notes': notes, 'absences': absences})



@login_required
@user_passes_test(lambda user: user.is_parent)
def children_schedule(request):
    parent = get_object_or_404(Parent, user=request.user)
    student = get_object_or_404(Student, id_student=parent.id_children)
    class_instance = student.classe
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
        'student': student,
        'class_instance': class_instance,
        'schedule_matrix': schedule_matrix,
        'days': days,
    }
    return render(request, 'parent/children_schedule.html', context)


@login_required
@user_passes_test(lambda user: user.is_parent)
def children_performance(request):
    parent = get_object_or_404(Parent, user=request.user)
    student = get_object_or_404(Student, id_student=parent.id_children)

    # Récupérer toutes les notes de l'élève, triées par date décroissante
    notes = Note.objects.filter(student=student).order_by('-date')

    # Obtenir les 10 dernières notes
    last_10_notes = notes[:10]

    if len(last_10_notes) >= 2:
        # Convertir last_10_notes en liste pour accéder à last() et first() sans problème
        last_10_notes_list = list(last_10_notes)
        # Diviser les notes en deux groupes
        midpoint = len(last_10_notes_list) // 2
        older_notes = last_10_notes_list[midpoint:]
        print(older_notes)
        recent_notes = last_10_notes_list[:midpoint]
        print(recent_notes)
        # Calculer les moyennes des groupes
        average_older = sum(note.score for note in older_notes) / len(older_notes)
        average_recent = sum(note.score for note in recent_notes) / len(recent_notes)

        # Calculer la marge de progression
        if average_older > 0:  # Éviter la division par zéro
            margin_of_progress = ((average_recent - average_older) / average_older) * 100
        else:
            margin_of_progress = None
    else:
        margin_of_progress = None  # Pas assez de notes pour calculer la marge de progrès

    # Les autres statistiques
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
                coefficient = Coefficient.objects.get(school_class=school_class, subject__name=subject_name).coefficient
                total_student_weighted_average += average * coefficient
                student_coefficients += coefficient
        student_average = total_student_weighted_average / student_coefficients if student_coefficients > 0 else 0
        student_averages.append((st, student_average))

    student_averages.sort(key=lambda x: x[1], reverse=True)

    # Calculer la moyenne de l'enfant
    student_average = next((avg for st, avg in student_averages if st == student), None)

    # La différence avec les plus fortes et faibles moyennes
    highest_average = student_averages[0][1] if student_averages else None
    lowest_average = student_averages[-1][1] if student_averages else None
    diff_highest = highest_average - student_average if student_average is not None else None
    diff_lowest = student_average - lowest_average if student_average is not None else None

    # Comparaison moyenne de l'enfant avec celle de la classe
    average_class = sum(avg for st, avg in student_averages) / len(student_averages) if student_averages else None
    diff_with_class = student_average - average_class if student_average is not None and average_class is not None else None
    print(average_class)
    # Les matières avec les moyennes les plus hautes et les plus basses
    grouped_notes = {}
    for subject_name, group in groupby(notes, key=lambda note: note.subject.name):
        subject_notes = list(group)
        if subject_notes:
            average = sum(note.score for note in subject_notes) / len(subject_notes)
            grouped_notes[subject_name] = average

    sorted_subjects = sorted(grouped_notes.items(), key=lambda x: x[1], reverse=True)

    top_3_subjects = sorted_subjects[:3]
    bottom_3_subjects = sorted_subjects[-3:]

    context = {
        'margin_of_progress': margin_of_progress,
        'diff_highest': diff_highest,
        'diff_lowest': diff_lowest,
        'diff_with_class': diff_with_class,
        'top_3_subjects': top_3_subjects,
        'bottom_3_subjects': bottom_3_subjects,
    }

    return render(request, 'parent/children_performance.html', context)


@login_required
@user_passes_test(lambda user: user.is_parent)
def choisir_motif(request):
    if request.method == 'POST':
        form = ChoixMotifForm(request.POST)
        if form.is_valid():
            motif = form.cleaned_data['motif']
            autre_motif = form.cleaned_data['autre_motif']
            request.session['motif'] = motif.id if motif else None
            request.session['autre_motif'] = autre_motif
            return redirect('choisir-creneau')
    else:
        form = ChoixMotifForm()
    return render(request, 'parent/choisir_motif.html', {'form': form})

@login_required
@user_passes_test(lambda user: user.is_parent)
def choisir_creneau(request):
    creneaux_disponibles = Creneau.objects.filter(disponible=True)
    if request.method == 'POST':
        form = ChoixCreneauForm(request.POST)
        if form.is_valid():
            parent = Parent.objects.get(user=request.user)
            creneau = form.cleaned_data['creneau']
            motif_id = request.session.get('motif')
            autre_motif = request.session.get('autre_motif')

            rendezvous = RendezVous(
                parent=parent,
                creneau=creneau,
                motif=Motif.objects.get(id=motif_id) if motif_id else None,
                autre_motif=autre_motif,
            )
            rendezvous.save()
            creneau.disponible = False
            creneau.save()
            return JsonResponse({
                'success': True,
                'date': creneau.date.strftime('%Y-%m-%d'),
                'heure': creneau.heure.strftime('%H:%M'),  # Format hour and minute
                'motif': rendezvous.motif.nom if rendezvous.motif else rendezvous.autre_motif
            })
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ChoixCreneauForm()

    return render(request, 'parent/choisir_creneau.html', {'form': form, 'creneaux_disponibles': creneaux_disponibles})