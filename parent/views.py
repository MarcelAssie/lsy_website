from authentication.models import Parent, Student
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404
from .forms import StudentIDForm
from administration.models import Note, MATIERE_CHOICES, Coefficient
from itertools import groupby
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from admin_parent.forms import ChoixCreneauForm, ChoixMotifForm
from admin_parent.models import Motif, RendezVous, Creneau



@login_required
def parent_dashboard(request):
    parent = Parent.objects.get(user=request.user)
    return render(request, 'parent/parent_dashboard.html', {'parent': parent})

@login_required
def parent_profile(request):
    parent = Parent.objects.get(user=request.user)
    return render(request, 'parent/parent_profile.html', {'parent': parent})

@login_required
def parent_notifications(request):
    parent = get_object_or_404(Parent, user=request.user)
    received_messages = parent.user.received_messages.order_by('-timestamp')
    received_messages.filter(is_read=False).update(is_read=True)
    return render(request, 'parent/parent_notifications.html', {'received_messages': received_messages})

@login_required
def parent_change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Met à jour la session de l'utilisateur pour éviter la déconnexion
            messages.success(request, 'Votre mot de passe a été mis à jour avec succès.')
            return redirect('parent-dashboard')  # Fonction de redirection en fonction de l'utilisateur
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'parent/parent_change_password.html', {'form': form})

@login_required
def children_details(request):
    student = None
    notes = []
    absences = []
    if request.method == 'POST':
        form = StudentIDForm(request.POST)
        if form.is_valid():
            student_id = form.cleaned_data['student_id']
            student = get_object_or_404(Student, student_id=student_id)
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
            return render(request, 'parent/children_details.html',
                          {
                            'student': student,
                            'grouped_notes': grouped_notes,
                            'total_absence_hours': total_absence_hours,
                            'subject_averages': subject_averages,
                            'general_average': general_average,
                            'coefficients': coefficients,})
    else:
        form = StudentIDForm()
    return render(request, 'parent/parent_details.html', {'form': form,'student': student, 'notes': notes,'absences': absences})

@login_required
def children_performance(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    notes = Note.objects.filter(student=student).order_by('date')

    # Préparer les données pour le graphique
    dates = [note.date.strftime("%Y-%m-%d") for note in notes]
    scores = [float(note.score) for note in notes]

    context = {
        'student': student,
        'dates': json.dumps(dates, cls=DjangoJSONEncoder),
        'scores': json.dumps(scores, cls=DjangoJSONEncoder)
    }
    return render(request, 'parent/children_perfomance.html', context)




@login_required
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