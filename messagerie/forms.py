from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body', 'file']
        labels = {
            'subject': 'Sujet',
            'body': 'Message',
            'file': 'Joindre un fichier (facultatif)',
        }
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }