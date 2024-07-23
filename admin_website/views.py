from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Actualite, Evenement
from .forms import ActualiteForm, EvenementForm
from django.contrib import messages
from .models import Annale
from .forms import AnnaleForm
from django.contrib.admin.views.decorators import staff_member_required


def actualites(request):
    actualites = Actualite.objects.all().order_by('-date_publiée')
    return render(request, 'admin_website/actualites.html', {'actualites': actualites})

def evenements(request):
    evenements = Evenement.objects.all().order_by('-date')
    return render(request, 'admin_website/evenements.html', {'evenements': evenements})

def actualite_detail(request, pk):
    actualite = get_object_or_404(Actualite, pk=pk)
    return render(request, 'admin_website/actualite_detail.html', {'actualite': actualite})

def evenement_detail(request, pk):
    evenement = get_object_or_404(Evenement, pk=pk)
    return render(request, 'admin_website/evenement_detail.html', {'evenement': evenement})

@staff_member_required
def ajouter_actualite(request):
    if request.method == 'POST':
        form = ActualiteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('actualites')
    else:
        form = ActualiteForm()
    return render(request, 'admin_website/ajouter_actualite.html', {'form': form})
@staff_member_required
def ajouter_evenement(request):
    if request.method == 'POST':
        form = EvenementForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('evenements')
    else:
        form = EvenementForm()
    return render(request, 'admin_website/ajouter_evenement.html', {'form': form})
@staff_member_required
def modifier_actualite(request, pk):
    actualite = get_object_or_404(Actualite, pk=pk)
    if request.method == 'POST':
        form = ActualiteForm(request.POST, request.FILES, instance=actualite)
        if form.is_valid():
            form.save()
            return redirect('actualites')
    else:
        form = ActualiteForm(instance=actualite)
    return render(request, 'admin_website/ajouter_actualite.html', {'form': form})
@staff_member_required
def modifier_evenement(request, pk):
    evenement = get_object_or_404(Evenement, pk=pk)
    if request.method == 'POST':
        form = EvenementForm(request.POST, request.FILES, instance=evenement)
        if form.is_valid():
            form.save()
            return redirect('evenements')
    else:
        form = EvenementForm(instance=evenement)
    return render(request, 'admin_website/ajouter_evenement.html', {'form': form})
@staff_member_required
def supprimer_actualite(request, pk):
    actualite = get_object_or_404(Actualite, pk=pk)
    if request.method == 'POST':
        actualite.delete()
        messages.success(request, 'L\'actualité a été supprimée avec succès.')
        return redirect('actualites')
    return render(request, 'admin_website/confirmer_suppression.html', {
        'obj': actualite,
        'type_obj': 'actualité',
        'cancel_url': reverse('actualites')  # URL de retour pour les actualités
    })

def supprimer_evenement(request, pk):
    evenement = get_object_or_404(Evenement, pk=pk)
    if request.method == 'POST':
        evenement.delete()
        messages.success(request, 'L\'événement a été supprimé avec succès.')
        return redirect('evenements')
    return render(request, 'admin_website/confirmer_suppression.html', {
        'obj': evenement,
        'type_obj': 'événement',
        'cancel_url': reverse('evenements')  # URL de retour pour les événements
    })



@staff_member_required
def add_annale(request):
    if request.method == 'POST':
        form = AnnaleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('add-annale')
    else:
        form = AnnaleForm()
    return render(request, 'admin_website/add_annale.html', {'form': form})

@staff_member_required
def admin_annales_manage(request):
    query = request.GET.get('recherche', '')
    if query:
        annales = Annale.objects.filter(title__icontains=query) | Annale.objects.filter(description__icontains=query)
    else:
        annales = Annale.objects.all()

    return render(request, 'admin_website/admin_manage_annales.html', {'annales': annales, 'query': query})

@staff_member_required
def delete_annale(request, annale_id):
    annale = get_object_or_404(Annale, id=annale_id)
    if request.method == 'POST':
        annale.delete()
        messages.success(request, 'Annale supprimée avec succès.')
        return redirect('admin-annales-manage')
    return redirect('admin-annales-manage')
