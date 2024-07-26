from django.db import models

class Motif(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.nom

class Creneau(models.Model):
    date = models.DateField()
    heure = models.TimeField()
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.date} à {self.heure}"

class RendezVous(models.Model):
    parent = models.ForeignKey("authentication.Parent", on_delete=models.CASCADE)
    motif = models.ForeignKey(Motif, on_delete=models.SET_NULL, null=True, blank=True)
    autre_motif = models.CharField(max_length=30, blank=True)
    creneau = models.OneToOneField(Creneau, on_delete=models.CASCADE)

    def __str__(self):
        return f"Rendez-vous de {self.parent} le {self.creneau.date} à {self.creneau.heure}"