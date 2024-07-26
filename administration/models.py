from django.db import models
from django.utils import timezone

MATIERE_CHOICES = [
    ('HG', 'Histoire-Géographie'),
    ('PC', 'Physique-Chimie'),
    ('Français', 'Français'),
    ('Anglais', 'Anglais'),
    ('LV2', 'Langue Vivante 2'),
    ('Mathematiques', 'Mathématiques'),
    ('EDHC', 'Éducation Civique et Morale'),
    ('Philosophie', 'Philosophie'),
    ('Arts Plastiques', 'Arts Plastiques'),
    ('Musique', 'Musique'),
    ('EPS', 'Éducation Physique et Sportive'),
    ('Natation', 'Natation'),
]
NIVEAU = [
    ('4', '4ème'),
    ('3', '3ème'),
    ('2', '2nde'),
    ('1', '1ère'),
    ('T', 'Terminale'),
]

NUMEROS = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('C1', 'C1'),
    ('C2', 'C2'),
    ('C3', 'C3'),
    ('C4', 'C4'),
    ('C5', 'C5'),
    ('D1', 'D1'),
    ('D2', 'D2'),
]

DAYS = [
        ('Lundi', 'Lundi'),
        ('Mardi', 'Mardi'),
        ('Mercredi', 'Mercredi'),
        ('Jeudi', 'Jeudi'),
        ('Vendredi', 'Vendredi'),
    ]

# Filtrer NUMEROS en fonction des règles spécifiées pour chaque niveau
def filter_numeros(niveau_code):
    if niveau_code in ['4', '3']:
        return [(num_code, num_desc) for num_code, num_desc in NUMEROS if num_code in ['1', '2', '3']]
    elif niveau_code == '2':
        return [(num_code, num_desc) for num_code, num_desc in NUMEROS if num_code.startswith('C')]
    elif niveau_code in ['1', 'T']:
        return [(num_code, num_desc) for num_code, num_desc in NUMEROS if num_code.startswith('C') or num_code.startswith('D')]
    else:
        return []

# Générer toutes les combinaisons possibles
CLASSES = []
for niveau_code, niveau_desc in NIVEAU:
    numeros_filtres = filter_numeros(niveau_code)
    for num_code, num_desc in numeros_filtres:
        CLASSES.append((niveau_desc + num_desc, f"{niveau_desc} {num_desc}"))

class Class(models.Model):
    CHOIX_CLASSES = CLASSES
    name = models.CharField(max_length=100, choices=CHOIX_CLASSES)
    def __str__(self):
        return self.get_name_display()

class Subject(models.Model):
    CHOIX_MATIERES = MATIERE_CHOICES
    name = models.CharField(max_length=100, choices=CHOIX_MATIERES)
    def __str__(self):
        return self.get_name_display()

class Schedule(models.Model):
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10, choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    def __str__(self):
        return f"{self.class_name} - {self.day_of_week} - {self.subject}"

class TeacherSchedule(models.Model):
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    teacher = models.ForeignKey('authentication.Teacher',on_delete=models.CASCADE )
    day_of_week = models.CharField(max_length=10, choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    def __str__(self):
        return f"{self.teacher} - {self.day_of_week} - {self.class_name}"

class Note(models.Model):
    student = models.ForeignKey('authentication.Student', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.subject.name}: {self.score}"
class Coefficient(models.Model):
    school_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    coefficient = models.PositiveIntegerField()
    class Meta:
        unique_together = ('school_class', 'subject')
    def __str__(self):
        return f"{self.school_class} - {self.subject} : {self.coefficient}"

class Absence(models.Model):
    student = models.ForeignKey('authentication.Student', on_delete=models.CASCADE, related_name='absences')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    reason = models.TextField(blank=True, null=True)
    def duration(self):
        return round(((self.end_time - self.start_time).total_seconds() / 3600),1)
    def __str__(self):
        return f"Absence de {self.student} de {self.start_time} à {self.end_time}"



