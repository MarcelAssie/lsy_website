from django import forms
from .models import Violence

class ViolenceForm(forms.ModelForm):
    class Meta:
        model = Violence
        fields = [
            'date', 'time', 'place', 'other_place',
            'reason', 'other_reason', 'description', 'perpetrator',
            'reported_by', 'severity', 'action_taken', 'witnesses',
        ]
        labels = {
            'date': "Date de l'incident",
            'time': "Heure de l'incident",
            'place': "Lieu",
            'other_place': "Autre lieu (si non listé)",
            'reason': "Motif",
            'other_reason': "Autre motif (si non listé)",
            'description': "Description des faits",
            'perpetrator': "Auteur présumé",
            'reported_by': "Signalé par",
            'severity': "Gravité",
            'action_taken': "Actions entreprises",
            'witnesses': "Témoins éventuels",
        }
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'place': forms.Select(attrs={'class': 'form-control'}),
            'other_place': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Précisez le lieu'}),
            'reason': forms.Select(attrs={'class': 'form-control'}),
            'other_reason': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Précisez le motif'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Décrivez brièvement les faits'}),
            'witnesses': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Citez les témoins si il y en a eu (noms, rôles, observations)'}),
            'perpetrator': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex : un camarade, un enseignant'}),
            'reported_by': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex : un parent, un surveillant (si ce n\'est vous)'}),
            'severity': forms.Select(attrs={'class': 'form-control'}),
            'action_taken': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Décrivez les mesures prises'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

        def clean(self):
            cleaned_data = super().clean()
            place = cleaned_data.get('place')
            other_place = cleaned_data.get('other_place')
            reason = cleaned_data.get('reason')
            other_reason = cleaned_data.get('other_reason')

            if not place and not other_place:
                raise forms.ValidationError("Veuillez renseigner un lieu ou bien préciser 'Autre lieu'.")

            if not reason and not other_reason:
                raise forms.ValidationError("Veuillez indiquer un motif ou bien préciser 'Autre motif'.")

            return cleaned_data
