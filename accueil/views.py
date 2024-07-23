from django.shortcuts import render
from admin_website.models import Annale, Evenement, Actualite
from django.shortcuts import render, get_object_or_404




def home(request):
    """
    Lancement de la page d'accueil
    """
    return render(request, 'accueil/accueil.html')

def director_speech(request):
    return render(request, 'accueil/director_speech.html')

def lycee_histoire(request):
    return render(request, 'accueil/lycee_histoire.html')

def lycee_mission_vision(request):
    return render(request, 'accueil/lycee_mission_vision.html')

def contact(request):
    return render(request, 'accueil/contact.html')

def lycee_administration(request):
    return render(request, 'accueil/administration.html')

def lycee_infras_equipements(request):
    return render(request, 'accueil/infras_equipements.html')

def reglements_interieurs(request):
    return render(request, 'accueil/reglements_interieurs.html')

def admission(request):
    return render(request, 'accueil/admission.html')

def criteres_admission(request):
    return render(request, 'accueil/criteres_admission.html')

def procedure_candidature(request):
    return render(request, 'accueil/procedure_candidature.html')

def annales_list(request):
    query = request.GET.get('recherche', '')
    if query:
        annales = Annale.objects.filter(title__icontains=query) | Annale.objects.filter(description__icontains=query)
    else:
        annales = Annale.objects.all()

    return render(request, 'accueil/annales_list.html', {'annales': annales, 'query': query})

def alumni_network(request):
    return render(request, 'accueil/alumni_network.html')

def alumni_activities(request):
    return render(request, 'accueil/alumni_activities.html')

def news(request):
    actualites = Actualite.objects.all().order_by('-date_publiée')
    return render(request, 'accueil/news.html', {'actualites': actualites})

def news_detail(request, pk):
    actualite = get_object_or_404(Actualite, pk=pk)
    return render(request, 'accueil/news_detail.html', {'actualite': actualite})

def events(request):
    evenements = Evenement.objects.all().order_by('-date')
    return render(request, 'accueil/events.html', {'evenements': evenements})

def event_detail(request, pk):
    evenement = get_object_or_404(Evenement, pk=pk)
    return render(request, 'accueil/event_detail.html', {'evenement': evenement})
