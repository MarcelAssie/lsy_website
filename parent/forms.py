from django import forms

class StudentIDForm(forms.Form):
    id_student = forms.CharField(max_length=100, required=True, label="ID de votre enfant")

