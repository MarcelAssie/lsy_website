from django.db import models
from django.utils import timezone
class Actualite(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='actualites/')
    date_publiée = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titre

class Evenement(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='evenements/')
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titre


class Annale(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='annales/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
