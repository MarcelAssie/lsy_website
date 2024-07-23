from django.contrib.auth.models import AbstractUser
from django.db import models
from administration.models import Class, Subject
from django_countries.fields import CountryField
from django.utils import timezone
from django.utils.crypto import get_random_string

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_parent = models.BooleanField(default=False)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    classe = models.ForeignKey(Class, on_delete=models.CASCADE)
    date_naissance = models.DateField(default=timezone.now)
    annee_admission = models.IntegerField(default=timezone.now().year)
    pays_origine = CountryField(default="CI")
    ville_origine = models.CharField(max_length=100, default='Abidjan')
    photo_profile = models.ImageField(upload_to='photos_profile/', blank=True,null=True)
    telephone = models.CharField(max_length=20, default='')
    lycee_provenance = models.CharField(max_length=100, default='')
    student_id = models.CharField(max_length=20, unique=True, blank=True)
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.classe}"
    def save(self, *args, **kwargs):
        if not self.student_id:
            self.student_id = self.generate_unique_student_id()
        super().save(*args, **kwargs)

    def generate_unique_student_id(self):
        while True:
            student_id = get_random_string(length=16)
            if not Student.objects.filter(student_id=student_id).exists():
                return student_id

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matiere = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='teacher', default=None)
    classes = models.ManyToManyField('administration.Class', related_name='teachers')
    date_naissance = models.DateField(default=timezone.now)
    annee_entree = models.IntegerField(default=timezone.now().year)
    photo_profile = models.ImageField(upload_to='photos_profile/', blank=True, null=True)
    telephone = models.CharField(max_length=20, default='')
    def __str__(self):
        return f"{self.user.get_full_name()}"

class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ville = models.CharField(max_length=100, default='Abidjan')
    pays = CountryField(default="CI")
    telephone = models.CharField(max_length=20, default='')
    contact = models.CharField(max_length=20, default='')
    def __str__(self):
        return f"{self.user.get_full_name()}"