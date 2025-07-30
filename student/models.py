from django.db import models

MOTIFS = [
    ('physique', 'Violence physique'),
    ('verbale', 'Violence verbale'),
    ('psychologique', 'Violence psychologique'),
    ('sexuelle', 'Violence sexuelle'),
    ('cyber', 'Cyberharcèlement'),
    ('discrimination', 'Discrimination'),
    ('negligence', 'Négligence éducative'),
    ('intimidation', 'Intimidation / menaces')
]

LIEUX = [
    ('school', 'À l’école'),
    ('home', 'En famille / à la maison'),
    ('road', 'Sur le chemin de l’école'),
    ('social', 'En ligne / sur les réseaux'),
    ('public_space', 'Dans l’espace public'),
    ('internat', 'À l’internat'),
    ('activite', 'Pendant une activité périscolaire'),
]

GRAVITE = [
    ('low', 'Faible'),
    ('moderate', 'Modérée'),
    ('high', 'Grave'),
    ('critical', 'Critique')
]
STATUS =[
    ('reported', 'Signalé'),
    ('investigating', 'En cours d\'enquête'),
    ('resolved', 'Résolu'),
    ('archived', 'Archivé')
]

class Violence(models.Model):
    student = models.ForeignKey('authentication.Student', on_delete=models.CASCADE, related_name='violences')
    date = models.DateField()
    time = models.TimeField()
    place = models.CharField(max_length=20, choices=LIEUX, default="school")
    other_place = models.CharField(max_length=30, blank=True)
    reason = models.CharField(max_length=20, choices=MOTIFS, default="verbale")
    other_reason = models.CharField(max_length=30, blank=True)
    description = models.TextField(max_length=200, blank=True, help_text="Description libre des faits")

    perpetrator = models.CharField(max_length=50, blank=True, help_text="Auteur présumé (élève, adulte, inconnu, etc.)")

    reported_by = models.CharField(max_length=50, blank=True, help_text="Personne ayant signalé les faits")

    witnesses = models.TextField(blank=True, help_text="Témoins éventuels (noms, rôles, observations)")

    severity = models.CharField(max_length=10, choices=GRAVITE, default="moderate")

    action_taken = models.TextField(max_length=200, blank=True, help_text="Action(s) entreprise(s) suite au signalement")

    status = models.CharField(max_length=20, choices=STATUS, default='reported')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.date} - {self.student} - {self.reason}"
