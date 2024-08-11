from django.http import HttpRequest
from admin_website.models import Annale, Evenement, Actualite, Testimonial
from django.shortcuts import get_object_or_404, redirect, render
import os
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



def home(request):
    """
    Affiche la page d'accueil.
    Cette vue récupère les deux derniers témoignages et les trois dernières actualités
    pour les afficher sur la page d'accueil.
    """
    testimonials = Testimonial.objects.all().order_by('-id')[:2]
    actualites = Actualite.objects.all().order_by('-id')[:3]
    return render(request, 'accueil/accueil.html', {'testimonials': testimonials, 'actualites' : actualites})

def director_speech(request):
    """
   Affiche la page du discours du directeur.
   """
    return render(request, 'accueil/director_speech.html')

def lycee_histoire(request):
    """
    Affiche la page de l'histoire du lycée.
    """
    return render(request, 'accueil/lycee_histoire.html')

def foundation_and_vision(request):
    """
    Affiche la page des fondations et de la vision.
    """
    return render(request, 'accueil/foundation_and_vision.html')

def excellence_education(request):
    """
    Affiche la page de l'excellence en éducation.
    """
    return render(request, 'accueil/excellence_education.html')

def lycee_mission_vision(request):
    """
    Affiche la page de la mission et de la vision du lycée.
    """
    return render(request, 'accueil/lycee_mission_vision.html')

def lycee_administration(request):
    """
    Affiche la page de l'administration du lycée.
    """
    return render(request, 'accueil/administration.html')

def lycee_infras_equipements(request):
    """
    Affiche la page des infrastructures et équipements du lycée.
    Cette vue rend un template pour montrer les infrastructures et équipements disponibles au lycée.
    """
    return render(request, 'accueil/infras_equipements.html')

def reglements_interieurs(request):
    """
    Affiche la page des règlements intérieurs du lycée.
    """
    return render(request, 'accueil/reglements_interieurs.html')

def admission(request):
    """
    Affiche la page d'admission.
    """
    return render(request, 'accueil/admission.html')

def criteres_admission(request):
    """
    Affiche la page des critères d'admission.
    """
    return render(request, 'accueil/criteres_admission.html')

def procedure_candidature(request):
    """
    Affiche la page de la procédure de candidature.
    """
    return render(request, 'accueil/procedure_candidature.html')

def annales_list(request):
    """
    Affiche la liste des annales disponibles.
    """
    query = request.GET.get('recherche', '')
    if query:
        annales = Annale.objects.filter(title__icontains=query) | Annale.objects.filter(description__icontains=query)
    else:
        annales = Annale.objects.all()

    return render(request, 'accueil/annales_list.html', {'annales': annales, 'query': query})

def alumni_network(request):
    """
    Affiche la page du réseau des anciens élèves.
    """
    return render(request, 'accueil/alumni_network.html')

def alumni_activities(request):
    """
    Affiche la page des activités des anciens élèves.
    """
    return render(request, 'accueil/alumni_activities.html')

def news(request):
    """
    Affiche la liste complète des actualités.
    """
    actualites = Actualite.objects.all().order_by('-date_publiée')
    return render(request, 'accueil/news.html', {'actualites': actualites})

def news_detail(request, pk):
    """
    Affiche les détails d'une actualité spécifique.
    """
    actualite = get_object_or_404(Actualite, pk=pk)
    return render(request, 'accueil/news_detail.html', {'actualite': actualite})

def events(request):
    """
    Affiche la liste complète des événements.
    """
    evenements = Evenement.objects.all().order_by('-date')
    return render(request, 'accueil/events.html', {'evenements': evenements})

def event_detail(request, pk):
    """
    Affiche les détails d'un événement spécifique.
    """
    evenement = get_object_or_404(Evenement, pk=pk)
    return render(request, 'accueil/event_detail.html', {'evenement': evenement})


def temoignage_list(request):
    """
    Affiche la liste de tous les témoignages.
    """
    testimonials = Testimonial.objects.all().order_by('-id')
    return render(request, 'accueil/temoignage_list.html', {'testimonials': testimonials})

def temoignage_detail(request, pk):
    """
    Affiche les détails d'un témoignage spécifique.
    """
    testimonial = get_object_or_404(Testimonial, pk=pk)
    return render(request, 'accueil/temoignage_detail.html', {'testimonial': testimonial})


def galerie(request):
    """
    Affiche la galerie d'images.
    """
    # Construire le chemin du répertoire des images
    gallery_dir = os.path.join(settings.BASE_DIR, 'static', 'images', 'galleries')
    # Lire les fichiers du répertoire
    image_files = [os.path.join('images', 'galleries', filename) for filename in os.listdir(gallery_dir) if
                   filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    # Passer les chemins relatifs des images au template
    return render(request, 'accueil/galerie.html', {'images': image_files})




def contact_view(request):
    """
    Gère le formulaire de contact et l'envoi d'un email.

    Si la requête est un POST (l'utilisateur a soumis le formulaire),
    cette vue extrait les informations du formulaire,
    crée un email formaté en HTML avec ces informations, et tente de l'envoyer
    à l'adresse email définie dans les paramètres de l'application.

    En cas de succès, l'utilisateur est redirigé vers une page de confirmation,
    avec son nom et son email en paramètres d'URL.
    Si l'envoi échoue, une exception est attrapée et un message d'erreur est imprimé.

    Si la requête est un GET (l'utilisateur accède simplement à la page de contact),
    cette vue rend le template du formulaire de contact.
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        objet = request.POST.get('objet')
        message_content = request.POST.get('message')

        # Informations de l'email
        to_emails = settings.CONTACT_EMAIL
        subject = f"Message de {name}"
        body = f"""
        <html>
        <head>
            <style>
                .email-container {{
                    font-family: 'Arial', sans-serif;
                    color: #333;
                    padding: 20px;
                    border: 1px solid #e0e0e0;
                    border-radius: 10px;
                    background: #ffffff;
                    max-width: 600px;
                    margin: auto;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                }}
                .email-container h2 {{
                    text-align: center;
                    color: #007bff;
                    font-size: 24px;
                }}
                .email-container p {{
                    font-size: 16px;
                    line-height: 1.6;
                    margin: 10px 0;
                }}
                .email-container .label {{
                    font-weight: bold;
                    color: #555;
                }}
                .email-container .message-content {{
                    padding: 15px;
                    background: #f9f9f9;
                    border-left: 4px solid #007bff;
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <h2>Message de {name}</h2>
                <p><span class="label">Nom :</span> {name}</p>
                <p><span class="label">Email :</span> {email}</p>
                <p><span class="label">Téléphone :</span> {telephone}</p>
                <p><span class="label">Objet :</span> {objet}</p>
                <p><span class="label">Message :</span></p>
                <div class="message-content">
                    {message_content}
                </div>
            </div>
        </body>
        </html>
        """

        # Création du message
        message = MIMEMultipart("alternative")
        message['From'] = settings.EMAIL_HOST_USER
        message['To'] = ', '.join(to_emails)
        message['Subject'] = subject

        message.attach(MIMEText(body, 'html'))

        try:
            with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
                server.starttls()
                server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                server.sendmail(settings.EMAIL_HOST_USER, to_emails, message.as_string())
            print('Email envoyé avec succès!')
        except Exception as e:
            print(f'Une erreur est survenue : {e}')

        return redirect(reverse('confirmation') + f'?name={name}&email={email}')

    return render(request, 'accueil/contact.html')




def confirmation_view(request: HttpRequest):
    """
    Affiche une page de confirmation après l'envoi réussi d'un email via le formulaire de contact.

    Cette vue récupère le nom et l'email de l'utilisateur à partir des paramètres d'URL
    pour personnaliser le message de confirmation affiché sur la page.
    """
    name = request.GET.get('name')
    email = request.GET.get('email')
    context = {'name': name, 'email': email}
    return render(request, 'accueil/confirmation.html', context)