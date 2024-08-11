from django.contrib.auth.decorators import user_passes_test, login_required
from authentication.models import Parent
from django.contrib import messages
from django.db import models
from django.shortcuts import render, redirect,get_object_or_404
from .models import Creneau, RendezVous
from .forms import CreneauForm


@login_required
@user_passes_test(lambda user: user.is_superuser)
def manage_parents(request):
    """
    Affiche la page de gestion des parents pour les administrateurs.
    """
    user = request.user
    return render(request, 'admin_parent/manage_parents.html',{'user': user})
@login_required
@user_passes_test(lambda user: user.is_superuser)
def list_parents(request):
    """
    Affiche la liste des parents dans l'interface admin.
    """
    parents = Parent.objects.all()
    return render(request, 'admin_parent/list_parents.html', {'parents': parents})
@login_required
@user_passes_test(lambda user: user.is_superuser)
def parent_details(request, parent_id):
    """
    Affiche les détails d'un parent spécifique dans l'interface admin.
    """
    parent = get_object_or_404(Parent, id=parent_id)
    return render(request, 'admin_parent/parent_details.html', {'parent': parent})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def delete_parent(request, parent_id):
    """
    Supprime un parent après confirmation via un POST. Redirige vers la liste des parents.
    """
    parent = get_object_or_404(Parent, id=parent_id)
    user = parent.user
    if request.method == "POST":
        user.delete()
        messages.success(request, 'L\'étudiant a été supprimé avec succès.')
        return redirect('list-parents')
    return redirect('parent-details', parent_id=parent_id)

@login_required
@user_passes_test(lambda user: user.is_superuser)
def delete_confirm_parent(request, parent_id):
    """
    Affiche une confirmation avant de supprimer un parent.
    """
    parent = get_object_or_404(Parent, id=parent_id)
    return render(request, 'admin_parent/delete_confirm_parent.html', {'parent': parent})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def search_parents(request):
    """
    Permet de rechercher des parents par nom dans l'interface admin.
    """
    name = request.GET.get('recherche')
    if request.method == "GET":
        if name:
            parents = Parent.objects.filter(
                models.Q(user__first_name__icontains=name) | models.Q(user__last_name__icontains=name))
    else:
        parents = Parent.objects.all()
    return render(request, 'admin_parent/manage_parents.html', {'parents': parents})


@login_required
@user_passes_test(lambda user: user.is_superuser)
def gestion_creneaux(request):
    """
    Affiche les créneaux disponibles et non disponibles dans l'interface admin.
    """
    creneaux_disponibles = Creneau.objects.filter(disponible=True).order_by('date', 'heure')
    creneaux_non_disponibles = Creneau.objects.filter(disponible=False).order_by('date', 'heure')

    context = {
        'creneaux_disponibles': creneaux_disponibles,
        'creneaux_non_disponibles': creneaux_non_disponibles
    }

    return render(request, 'admin_parent/gestion_creneaux.html', context)
@login_required
@user_passes_test(lambda user: user.is_superuser)
def ajouter_creneau(request):
    """
    Affiche un formulaire pour ajouter un nouveau créneau. Enregistre le créneau si la requête est un POST.
    """
    if request.method == 'POST':
        form = CreneauForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion-creneaux')
    else:
        form = CreneauForm()
    return render(request, 'admin_parent/ajouter_creneau.html', {'form': form})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def supprimer_creneau(request, creneau_id):
    """
    Supprime un créneau après confirmation et redirige vers la gestion des créneaux.
    """
    creneau = get_object_or_404(Creneau, id=creneau_id)
    creneau.delete()
    return redirect('gestion-creneaux')


@login_required
@user_passes_test(lambda user: user.is_superuser)
def rendezvous_list(request):
    """
    Affiche la liste des rendez-vous avec les détails des parents, créneaux et motifs.
    """
    rendezvous = RendezVous.objects.select_related('parent', 'creneau', 'motif').all()
    context = {
        'rendezvous': rendezvous
    }
    return render(request, 'admin_parent/appointments.html', context)
