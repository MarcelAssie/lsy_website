from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Actualite, Evenement, Testimonial
from .forms import ActualiteForm, EvenementForm, TestimonialForm
from django.contrib import messages
from .models import Annale
from .forms import AnnaleForm
from django.contrib.auth.decorators import user_passes_test, login_required


@login_required
@user_passes_test(lambda user: user.is_superuser)
def actualites(request):
    actualites = Actualite.objects.all().order_by('-date_publiée')
    return render(request, 'admin_website/actualites.html', {'actualites': actualites})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def evenements(request):
    evenements = Evenement.objects.all().order_by('-date')
    return render(request, 'admin_website/evenements.html', {'evenements': evenements})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def actualite_detail(request, pk):
    actualite = get_object_or_404(Actualite, pk=pk)
    return render(request, 'admin_website/actualite_detail.html', {'actualite': actualite})
@login_required
@user_passes_test(lambda user: user.is_superuser)
def evenement_detail(request, pk):
    evenement = get_object_or_404(Evenement, pk=pk)
    return render(request, 'admin_website/evenement_detail.html', {'evenement': evenement})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def testimonials(request):
    testimonials = Testimonial.objects.all().order_by('-id')
    return render(request, 'admin_website/testimonials.html', {'testimonials': testimonials})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def testimonial_detail(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    return render(request, 'admin_website/testimonial_detail.html', {'testimonial': testimonial})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def ajouter_actualite(request):
    if request.method == 'POST':
        form = ActualiteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('actualites')
    else:
        form = ActualiteForm()
    return render(request, 'admin_website/ajouter_actualite.html', {'form': form})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def ajouter_evenement(request):
    if request.method == 'POST':
        form = EvenementForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('evenements')
    else:
        form = EvenementForm()
    return render(request, 'admin_website/ajouter_evenement.html', {'form': form})

@login_required
@user_passes_test(lambda user: user.is_superuser)
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
@login_required
@user_passes_test(lambda user: user.is_superuser)
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

@login_required
@user_passes_test(lambda user: user.is_superuser)
def supprimer_actualite(request, pk):
    actualite = get_object_or_404(Actualite, pk=pk)
    if request.method == 'POST':
        actualite.delete()
        return redirect('actualites')
    return render(request, 'admin_website/confirmer_suppression.html', {
        'obj': actualite,
        'type_obj': 'actualité',
        'cancel_url': reverse('actualites')  # URL de retour pour les actualités
    })

@login_required
@user_passes_test(lambda user: user.is_superuser)
def supprimer_evenement(request, pk):
    evenement = get_object_or_404(Evenement, pk=pk)
    if request.method == 'POST':
        evenement.delete()
        return redirect('evenements')
    return render(request, 'admin_website/confirmer_suppression.html', {
        'obj': evenement,
        'type_obj': 'événement',
        'cancel_url': reverse('evenements')  # URL de retour pour les événements
    })


@login_required
@user_passes_test(lambda user: user.is_superuser)
def add_annale(request):
    if request.method == 'POST':
        form = AnnaleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Annale ajoutée avec succès.")
            return redirect('add-annale')
    else:
        form = AnnaleForm()
    return render(request, 'admin_website/add_annale.html', {'form': form})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def admin_annales_manage(request):
    query = request.GET.get('recherche', '')
    if query:
        annales = Annale.objects.filter(title__icontains=query) | Annale.objects.filter(description__icontains=query)
    else:
        annales = Annale.objects.all()

    return render(request, 'admin_website/admin_manage_annales.html', {'annales': annales, 'query': query})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def delete_annale(request, annale_id):
    annale = get_object_or_404(Annale, id=annale_id)
    if request.method == 'POST':
        annale.delete()
        return redirect('admin-annales-manage')
    return redirect('admin-annales-manage')

@login_required
@user_passes_test(lambda user: user.is_superuser)
def add_testimonial(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('testimonials')
    else:
        form = TestimonialForm()
    return render(request, 'admin_website/add_testimonial.html', {'form': form})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def edit_testimonial(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES, instance=testimonial)
        if form.is_valid():
            form.save()
            return redirect('testimonials')
    else:
        form = TestimonialForm(instance=testimonial)
    return render(request, 'admin_website/add_testimonial.html', {'form': form})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def delete_testimonial(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    if request.method == 'POST':
        testimonial.delete()
        return redirect('testimonials')
    return render(request, 'admin_website/confirmer_suppression.html', {
        'obj': testimonial,
        'type_obj': 'témoignage',
        'cancel_url': reverse('testimonials')  # URL de retour pour les témoignages
    })