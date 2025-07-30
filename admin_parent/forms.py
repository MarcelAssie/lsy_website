from django import forms
from django.utils.formats import date_format
from .models import Motif, Creneau

class CreneauForm(forms.ModelForm):
    class Meta:
        model = Creneau
        fields = ['date', 'heure', 'disponible']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Sélectionnez la date'
            }),
            'heure': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
                'placeholder': 'Sélectionnez l\'heure'
            })
        }


class ChoixMotifForm(forms.Form):
    motif = forms.ModelChoiceField(
        queryset=Motif.objects.all(),
        required=False,
        label="Choisissez un motif",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    autre_motif = forms.CharField( max_length=30, required=False, label="Ou spécifiez un autre motif", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Max 30 caractères...'})
    )

    def clean(self):
        cleaned_data = super().clean()
        motif = cleaned_data.get('motif')
        autre_motif = cleaned_data.get('autre_motif')

        if not motif and not autre_motif:
            raise forms.ValidationError("Vous devez choisir un motif ou en spécifier un autre.")
        return cleaned_data

class ChoixCreneauForm(forms.Form):
    creneau = forms.ModelChoiceField(
        queryset=Creneau.objects.filter(disponible=True),
        widget=forms.RadioSelect,
        label="Choisissez un créneau",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['creneau'].queryset = Creneau.objects.filter(disponible=True)
        self.fields['creneau'].label_from_instance = lambda obj: \
            f"{date_format(obj.date, format='d F Y')} à {obj.heure.strftime('%H:%M')}"