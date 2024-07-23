from django.shortcuts import redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from authentication.models import Student, User
from administration.models import MATIERE_CHOICES, Note, Absence, Coefficient
from administration.models import Class
from django.contrib import messages
from authentication.forms import StudentSignUpForm
from administration.forms import NoteForm, AbsenceForm
from itertools import groupby
from django.shortcuts import render
from django.db import models
from django.utils import timezone



#------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------- GESTION ADMINISTRATEUR -------------------------------------------------------------

@staff_member_required
def list_students_by_class(request, class_id):
    classe = get_object_or_404(Class, pk=class_id)
    students = Student.objects.filter(classe=classe)
    return render(request, 'admin_student/students_by_class.html', {'students': students, 'classe': classe})

@staff_member_required
def student_details(request, student_id):
    """
    Ce qui est normal
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

    return render(request, 'admin_student/student_details.html', {
        'student': student,
        'grouped_notes': grouped_notes,
        'subject_averages': subject_averages,
        'general_average': general_average,
        'coefficients': coefficients,
        'total_absence_hours': total_absence_hours})

@staff_member_required
def student_details2(request, student_id):
    """
    Pour la recherche dans les informations
    """
    user = get_object_or_404(User, id=student_id, is_student=True)
    student = get_object_or_404(Student, user=user)
    notes = Note.objects.filter(student=student).order_by('subject__name', '-date')
    absences = student.absences.all()
    total_absence_hours = round(sum(absence.duration() for absence in absences), 1)
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

    return render(request, 'admin_student/student_details.html', {
        'student': student,
        'grouped_notes': grouped_notes,
        'subject_averages': subject_averages,
        'general_average': general_average,
        'coefficients': coefficients,
        'total_absence_hours': total_absence_hours})


@staff_member_required
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == "POST":
        form = StudentSignUpForm(request.POST, request.FILES, instance=student.user)
        if form.is_valid():
            form.save()
            return redirect('student-details', student_id=student.id)
    else:
        form = StudentSignUpForm(instance=student.user)
    return render(request, 'admin_student/edit_student.html', {'form': form, 'student': student})

@staff_member_required
def delete_confirm_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'admin_student/delete_confirm_student.html', {'student': student})

@staff_member_required
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    user = student.user
    if request.method == "POST":
        user.delete()
        messages.success(request, 'L\'étudiant a été supprimé avec succès.')
        return redirect('list-classes')
    return redirect('student-details', student_id=student_id)

@staff_member_required
def add_note(request, student_id):
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

@staff_member_required
def edit_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('student-details', student_id=note.student.id)
    else:
        form = NoteForm(instance=note)

    return render(request, 'admin_student/edit_note.html', {'form': form, 'note': note})

@staff_member_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    student_id = note.student.id
    if request.method == 'POST':
        note.delete()
        return redirect('student-details', student_id=student_id)
    return render(request, 'admin_student/delete_note.html', {'note': note})

@staff_member_required
def manage_students(request):
    user = request.user
    return render(request, 'admin_student/manage_students.html',{'user': user})

@staff_member_required
def search_students(request):
    students = User.objects.filter(is_student=True)
    if request.method == "GET":
        name = request.GET.get('recherche')
        if name:
            students = students.filter(
                models.Q(first_name__icontains=name) | models.Q(last_name__icontains=name))
    return render(request, 'admin_student/manage_students.html', {'students': students})

@staff_member_required
def add_absence(request, student_id):
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

@staff_member_required
def delete_absence(request, absence_id):
    absence = get_object_or_404(Absence, id=absence_id)
    student_id = absence.student.id
    if request.method == 'POST':
        absence.delete()
        return redirect('student-details', student_id=student_id)
    return render(request, 'admin_student/confirm_delete_absence.html', {'absence': absence})

