from authentication.models import Student
from administration.models import MATIERE_CHOICES, Note, Absence, Coefficient, Class, Subject
from django.contrib import messages
from administration.forms import NoteForm, AbsenceForm
from itertools import groupby
from django.db import models
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test


#------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------- GESTION ADMINISTRATEUR -------------------------------------------------------------

@login_required
@user_passes_test(lambda user: user.is_superuser)
def list_students_by_class(request, class_id):
    """
    Affiche la liste des étudiants pour une classe donnée.
    """
    classe = get_object_or_404(Class, pk=class_id)
    students = Student.objects.filter(classe=classe)
    return render(request, 'admin_student/students_by_class.html', {'students': students, 'classe': classe})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def student_details(request, student_id):
    """
    Affiche les détails d'un étudiant, y compris les notes, moyennes, les absences et le classement.
    """
    student = get_object_or_404(Student, id=student_id)
    notes = Note.objects.filter(student=student).order_by('subject__name', '-date')
    absences = student.absences.all()
    total_absence_hours = round(sum(absence.duration() for absence in absences),1)
    # Regrouper les notes par matière
    coefficients = {}
    grouped_notes = {}
    subject_averages = {}
    total_weighted_average = 0
    total_coefficients = 0
    for subject_name, group in groupby(notes, key=lambda note: note.subject.name):
        # Récupérer le nom complet de la matière à partir de MATIERE_CHOICES
        full_subject_name = next((name for code, name in MATIERE_CHOICES if code == subject_name), subject_name)
        grouped_notes[full_subject_name] = list(group)
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
    if student_rank == 1:
        print(f"{student_rank}ᵉʳ")
    else:
        print(f"{student_rank}ᵉᵐᵉ")
    return render(request, 'admin_student/student_details.html', {
        'student': student,
        'grouped_notes': grouped_notes,
        'subject_averages': subject_averages,
        'general_average': general_average,
        'coefficients': coefficients,
        'student_rank': student_rank,
        'total_absence_hours': total_absence_hours})


@login_required
@user_passes_test(lambda user: user.is_superuser)
def delete_student(request, student_id):
    """
    Supprime un étudiant après confirmation. Redirige vers la liste des classes.
    """
    student = get_object_or_404(Student, id=student_id)
    user = student.user
    if request.method == "POST":
        user.delete()
        messages.success(request, 'L\'étudiant a été supprimé avec succès.')
        return redirect('list-classes')
    return redirect('student-details', student_id=student_id)

@login_required
@user_passes_test(lambda user: user.is_superuser)
def delete_confirm_student(request, student_id):
    """
    Affiche une confirmation avant de supprimer un étudiant.
    """
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'admin_student/delete_confirm_student.html', {'student': student})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def notes_classes(request):
    """
    Affiche la liste des classes pour la gestion des notes.
    """
    classes = Class.objects.all()
    return render(request, 'admin_student/notes_classes.html', {'classes': classes})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def add_note(request, student_id):
    """
    Affiche un formulaire pour ajouter une note à un étudiant. Enregistre la note si la requête est un POST.
    """
    student = get_object_or_404(Student, id=student_id)
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.student = student
            note.save()
            messages.success(request, 'La note a été ajoutée avec succès.')
            return redirect('add-note', student_id=student.id)
    else:
        form = NoteForm()
    return render(request, 'admin_student/add_note.html', {'form': form, 'student': student})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def edit_note(request, note_id):
    """
    Affiche un formulaire pour modifier une note existante. Enregistre les modifications si la requête est un POST.
    """
    note = get_object_or_404(Note, pk=note_id)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('student-details', student_id=note.student.id)
    else:
        form = NoteForm(instance=note)

    return render(request, 'admin_student/edit_note.html', {'form': form, 'note': note})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def delete_note(request, note_id):
    """
    Supprime une note après confirmation. Redirige vers les détails de l'étudiant.
    """
    note = get_object_or_404(Note, pk=note_id)
    student_id = note.student.id
    if request.method == 'POST':
        note.delete()
        return redirect('student-details', student_id=student_id)
    return render(request, 'admin_student/delete_note.html', {'note': note})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def manage_students(request):
    """
    Affiche la page de gestion des étudiants pour les administrateurs.
    """
    user = request.user
    return render(request, 'admin_student/manage_students.html',{'user': user})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def search_students(request):
    """
    Permet de rechercher des étudiants par nom dans l'interface admin.
    """
    name = request.GET.get('recherche')
    if request.method == "GET":
        if name:
            students = Student.objects.filter(
                models.Q(user__first_name__icontains=name) | models.Q(user__last_name__icontains=name))
    else:
        students = Student.objects.all()
    return render(request, 'admin_student/manage_students.html', {'students': students})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def add_absence(request, student_id):
    """
    Affiche un formulaire pour ajouter une absence à un étudiant. Enregistre l'absence si la requête est un POST.
    """
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = AbsenceForm(request.POST)
        if form.is_valid():
            absence = form.save(commit=False)
            absence.student = student
            absence.save()
            return redirect('student-details', student_id=student.id)
    else:
        form = AbsenceForm(initial={'start_time': timezone.now(), 'end_time': timezone.now()})
    return render(request, 'admin_student/add_absence.html', {'form': form, 'student': student})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def delete_absence(request, absence_id):
    """
    Supprime une absence après confirmation. Redirige vers les détails de l'étudiant.
    """
    absence = get_object_or_404(Absence, id=absence_id)
    student_id = absence.student.id
    if request.method == 'POST':
        absence.delete()
        return redirect('student-details', student_id=student_id)
    return render(request, 'admin_student/confirm_delete_absence.html', {'absence': absence})


@login_required
@user_passes_test(lambda user: user.is_superuser)
def add_notes_to_class(request, class_id):
    """
    Affiche un formulaire pour ajouter des notes pour tous les étudiants d'une classe. Enregistre les notes si la requête est un POST.
    """
    classe = get_object_or_404(Class, pk=class_id)
    students = Student.objects.filter(classe=classe).order_by('user__last_name', 'user__first_name')

    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        date = request.POST.get('date')
        notes = request.POST.getlist('notes')

        if not subject_id or not date:
            messages.error(request, "La matière et la date sont obligatoires.")
            return render(request, 'admin_student/add_notes.html', {'classe': classe, 'students': students})

        subject = get_object_or_404(Subject, pk=subject_id)

        for student in students:
            score = request.POST.get(f'note_{student.id}')
            if score:
                Note.objects.update_or_create(
                    student=student,
                    subject=subject,
                    date=date,
                    defaults={'score': score}
                )

        messages.success(request, "Les notes ont été ajoutées avec succès.")
        return redirect('add-notes-to-class', class_id=class_id)

    subjects = Subject.objects.all()
    return render(request, 'admin_student/add_notes.html', {'classe': classe, 'students': students, 'subjects': subjects})

