from django.db import models
from django.utils import timezone
import os
def upload_to_actualites(instance, filename):
    return os.path.join('actualites/', filename)

def upload_to_evenements(instance, filename):
    return os.path.join('evenements/', filename)

def upload_to_annales(instance, filename):
    return os.path.join('annales/', filename)

def upload_to_temoignages(instance, filename):
    return os.path.join('temoignages/', filename)

class Actualite(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to=upload_to_actualites)
    date_publiée = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titre

class Evenement(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to=upload_to_evenements)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titre

class Annale(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to=upload_to_annales)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Testimonial(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom")
    promotion = models.CharField(max_length=50, verbose_name="Promotion")
    photo = models.ImageField(upload_to=upload_to_temoignages, blank=True, null=True, verbose_name="Photo")
    text = models.TextField(verbose_name="Texte du Témoignage")

    def __str__(self):
        return self.name
