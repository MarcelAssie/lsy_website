from django import forms
from .models import Actualite, Evenement, Annale

class ActualiteForm(forms.ModelForm):
    class Meta:
        model = Actualite
        fields = ['titre', 'description', 'image']
        widgets = {
            'titre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre de l\'actualité'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Description de l\'actualité',
                'rows': 4
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control-file'
            }),
        }

class EvenementForm(forms.ModelForm):
    class Meta:
        model = Evenement
        fields = ['titre', 'description', 'image']
        widgets = {
            'titre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre de l\'événement'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Description de l\'événement',
                'rows': 4
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control-file'
            }),
        }


class AnnaleForm(forms.ModelForm):
    class Meta:
        model = Annale
        fields = ['title', 'description', 'file']
        labels = {
            'title': 'Titre',
            'description': 'Description',
            'file': 'Fichier Annale'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le titre'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Entrez la description'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control-file'})
        }
