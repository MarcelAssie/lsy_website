from django import forms
from django.contrib.auth.forms import UserCreationForm
from authentication.models import User, Student, Teacher, Parent
from administration.models import Subject, Class
from django.utils import timezone
import string
import random
from django_countries.fields import CountryField


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label="Identifiants")
    password = forms.CharField(max_length=100, widget=forms.PasswordInput, label="Mot de passe")

class StudentSignUpForm(forms.ModelForm):
    classe = forms.ModelChoiceField(queryset=Class.objects.all(), required=True, label="Classe")
    date_naissance = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}), initial=timezone.now().date, label="Date de naissance")
    annee_admission = forms.IntegerField(required=True, initial=timezone.now().year, label="Année d'admission")
    pays_origine = CountryField().formfield(required=True, label="Pays d'origine")
    ville_origine = forms.CharField(max_length=100, required=True, label="Ville d'origine")
    photo_profile = forms.ImageField(required=False, label="Photo de profil")
    telephone = forms.CharField(max_length=20, required=True, label="N° de Téléphone")
    lycee_provenance = forms.CharField(max_length=100, required=True, label="Lycée de provenance")
    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'email', 'classe', 'date_naissance', 'annee_admission', 'pays_origine', 'ville_origine', 'photo_profile', 'telephone', 'lycee_provenance')
        labels = {
            'last_name': 'Nom',
            'first_name': 'Prénoms',
            'email': 'Adresse email',
        }

    def save(self, commit=True):
        user = User(
            last_name=self.cleaned_data['last_name'],
            first_name=self.cleaned_data['first_name'],
            email=self.cleaned_data['email'],
            is_student=True
        )
        # Générer automatiquement le username et le mot de passe
        username = self.generate_username(self.cleaned_data['last_name'], self.cleaned_data['first_name'])
        password = self.generate_password()
        user.username = username
        user.set_password(password)  # Définir le mot de passe généré

        if commit:
            user.save()
            Student.objects.create(
                user=user,
                classe=self.cleaned_data['classe'],
                date_naissance=self.cleaned_data['date_naissance'],
                annee_admission=self.cleaned_data['annee_admission'],
                pays_origine=self.cleaned_data['pays_origine'],
                ville_origine=self.cleaned_data['ville_origine'],
                photo_profile=self.cleaned_data['photo_profile'],
                telephone=self.cleaned_data['telephone'],
                lycee_provenance=self.cleaned_data['lycee_provenance']
            )
        return user, password  # Retourner l'utilisateur et le mot de passe généré
    def generate_username(self, last_name, first_name):
        base_username = last_name[:4].upper() + first_name[:2].lower()
        unique_suffix = ''.join(random.choices(string.digits, k=4))
        return base_username + unique_suffix

    def generate_password(self, length=12):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        return password

class TeacherSignUpForm(forms.ModelForm):
    matiere = forms.ModelChoiceField(queryset=Subject.objects.all(), label="Matière enseignée")
    classes = forms.ModelMultipleChoiceField(label="Classes", queryset=Class.objects.all(), widget=forms.CheckboxSelectMultiple)
    date_naissance = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}),
                                     initial=timezone.now().date, label="Date de naissance")
    annee_entree = forms.IntegerField(required=True, initial=timezone.now().year, label="Année d'entrée au LSY")
    photo_profile = forms.ImageField(required=False, label="Photo de profile")
    telephone = forms.CharField(max_length=20, required=True, label="N° de téléphone")

    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'email', 'matiere', 'classes',
                  'date_naissance', 'photo_profile', 'telephone')
        labels = {
            'email': 'Adresse email',
            'last_name': 'Nom',
            'first_name': 'Prénoms',
        }

    def save(self, commit=True):
        user = User(
            last_name=self.cleaned_data['last_name'],
            first_name=self.cleaned_data['first_name'],
            email=self.cleaned_data['email'],
            is_teacher=True
        )
        # Générer automatiquement le username et le mot de passe
        username = self.generate_username(self.cleaned_data['last_name'], self.cleaned_data['first_name'])
        password = self.generate_password()
        user.username = username
        user.set_password(password)
        if commit:
            user.save()
            teacher = Teacher.objects.create(
                user=user,
                matiere=self.cleaned_data['matiere'],
                date_naissance=self.cleaned_data['date_naissance'],
                annee_entree=self.cleaned_data['annee_entree'],
                photo_profile=self.cleaned_data['photo_profile'],
                telephone=self.cleaned_data['telephone']
            )
            teacher.classes.set(self.cleaned_data['classes'])
        return user, password  # Retourner l'utilisateur et le mot de passe généré

    def generate_username(self, last_name, first_name):
        base_username = last_name[:4].upper() + first_name[:2].lower()
        unique_suffix = ''.join(random.choices(string.digits, k=4))
        return base_username + unique_suffix

    def generate_password(self, length=12):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        return password

class ParentSignUpForm(forms.ModelForm):
    ville = forms.CharField(max_length=100, required=True, label="Ville de résidence")
    pays = CountryField().formfield(required=True, label="Pays de résidence")
    telephone = forms.CharField(max_length=20, required=True, label="N° de Téléphone")
    contact = forms.CharField(max_length=20, required=True, label="Autre N°Téléphone")
    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'email', 'ville', 'pays', 'telephone', 'contact')
        labels = {
            'last_name': 'Nom',
            'first_name': 'Prénoms',
            'email': 'Adresse email',
        }

    def save(self, commit=True):
        user = User(
            last_name=self.cleaned_data['last_name'],
            first_name=self.cleaned_data['first_name'],
            email=self.cleaned_data['email'],
            is_parent=True
        )
        username = self.generate_username(self.cleaned_data['last_name'], self.cleaned_data['first_name'])
        password = self.generate_password()
        user.username = username
        user.set_password(password)
        if commit:
            user.save()
            Parent.objects.create(
                user=user,
                ville=self.cleaned_data['ville'],
                pays=self.cleaned_data['pays'],
                telephone=self.cleaned_data['telephone'],
                contact=self.cleaned_data['contact']
            )
        return user, password
    def generate_username(self, last_name, first_name):
        base_username = last_name[:4].upper() + first_name[:2].lower()
        unique_suffix = ''.join(random.choices(string.digits, k=4))
        return base_username + unique_suffix

    def generate_password(self, length=12):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        return password


