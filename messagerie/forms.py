from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body', 'file']
        labels = {
            'subject': 'Objet',
            'body': 'Message',
            'file': 'Joindre un fichier (facultatif)',
        }
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 250}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'maxlength': 250}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }