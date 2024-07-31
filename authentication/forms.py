from django import forms
from authentication.models import User, Student, Teacher, Parent
from administration.models import Subject, Class
import string
import random


class LoginForm(forms.Form):
    username = forms.CharField(max_length=12, label="Identifiant")
    password = forms.CharField(max_length=12, widget=forms.PasswordInput, label="Mot de passe")

class StudentSignUpForm(forms.ModelForm):
    classe = forms.ModelChoiceField(queryset=Class.objects.all(), required=True, label="Classe")
    class Meta:
        model = User
        fields = ('last_name', 'first_name')
        labels = {
            'last_name': 'Nom',
            'first_name': 'Prénom(s)',
        }

    def save(self, commit=True):
        user = User(
            last_name=self.cleaned_data['last_name'],
            first_name=self.cleaned_data['first_name'],
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
            )
        return user, password  # Retourner l'utilisateur et le mot de passe généré
    def generate_username(self, last_name, first_name):
        base_username = last_name[:4].upper() + first_name[:2].lower()
        unique_suffix = ''.join(random.choices(string.digits, k=4))
        return base_username + unique_suffix

    def generate_password(self, length=8):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        return password

class TeacherSignUpForm(forms.ModelForm):
    matiere = forms.ModelChoiceField(queryset=Subject.objects.all(), label="Matière enseignée")
    classes = forms.ModelMultipleChoiceField(label="Classes", queryset=Class.objects.all(), widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'matiere', 'classes')
        labels = {
            'last_name': 'Nom',
            'first_name': 'Prénom(s)',
        }

    def save(self, commit=True):
        user = User(
            last_name=self.cleaned_data['last_name'],
            first_name=self.cleaned_data['first_name'],
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
            )
            teacher.classes.set(self.cleaned_data['classes'])
        return user, password  # Retourner l'utilisateur et le mot de passe généré

    def generate_username(self, last_name, first_name):
        base_username = last_name[:4].upper() + first_name[:2].lower()
        unique_suffix = ''.join(random.choices(string.digits, k=4))
        return base_username + unique_suffix

    def generate_password(self, length=8):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        return password

class ParentSignUpForm(forms.ModelForm):
    contact = forms.CharField(max_length=20, required=False, label="N°Téléphone")
    id_children = forms.CharField(max_length=8, required=False, label="Identifiant unique enfant")
    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'contact', 'id_children')
        labels = {
            'last_name': 'Nom',
            'first_name': 'Prénom(s)',
        }

    def save(self, commit=True):
        user = User(
            last_name=self.cleaned_data['last_name'],
            first_name=self.cleaned_data['first_name'],
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
                contact=self.cleaned_data['contact'],
                id_children = self.cleaned_data['id_children']
            )
        return user, password
    def generate_username(self, last_name, first_name):
        base_username = last_name[:4].upper() + first_name[:2].lower()
        unique_suffix = ''.join(random.choices(string.digits, k=4))
        return base_username + unique_suffix

    def generate_password(self, length=8):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        return password


