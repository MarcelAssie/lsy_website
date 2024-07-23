from django import forms

class StudentIDForm(forms.Form):
    student_id = forms.CharField(max_length=100, required=True, label="ID de votre enfant")