from django.contrib.auth.models import AbstractUser
from django.db import models
from administration.models import Class, Subject
from django.utils.crypto import get_random_string

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_parent = models.BooleanField(default=False)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    classe = models.ForeignKey(Class, on_delete=models.CASCADE)
    id_student = models.CharField(max_length=20, unique=True, blank=True)
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.classe}"
    def save(self, *args, **kwargs):
        if not self.id_student:
            self.id_student = self.generate_unique_id_student()
        super().save(*args, **kwargs)
    def generate_unique_id_student(self):
        while True:
            id_student = get_random_string(length=8)
            if not Student.objects.filter(id_student=id_student).exists():
                return id_student

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matiere = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='teacher', default=None)
    classes = models.ManyToManyField('administration.Class', related_name='teachers')
    def __str__(self):
        return f"{self.user.get_full_name()}"

class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=20, unique=True, blank=True, null=True)
    id_children = models.CharField(max_length=8, unique=True, blank=True, null=True)
    def __str__(self):
        return f"{self.user.get_full_name()}"