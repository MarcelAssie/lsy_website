from django import forms
from .models import Note, Subject, Absence, Coefficient, Class, TeacherSchedule, Schedule
from authentication.models import Teacher

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['subject', 'score', 'date']
        labels = {
            'subject': 'Matière',
            'score': 'Note',
            'date': 'Date de l\'évaluation',
        }
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'score': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Entrez la note...', 'min': 0, 'max': 20}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].queryset = Subject.objects.all()

    def clean_score(self):
        score = self.cleaned_data.get('score')
        if score < 0 or score > 20:
            raise forms.ValidationError("La note doit être comprise entre 0 et 20.")
        return score


# forms.pyx
class NoteFormForTeacher(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['score', 'date']
        labels = {
            'score': 'Note',
            'date': 'Date de l\'évaluation',
        }
        widgets = {
            'score': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Entrez la note...', 'min': 0, 'max': 20}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(NoteFormForTeacher, self).__init__(*args, **kwargs)
        self.teacher = Teacher.objects.get(user=user)  # Récupérer l'enseignant
        self.instance.subject = self.teacher.matiere  # Définir la matière de l'enseignant

class AbsenceForm(forms.ModelForm):
    class Meta:
        model = Absence
        fields = ['start_time', 'end_time', 'reason']
        labels = {
            'start_time': 'Debut',
            'end_time': 'Fin',
            'reason': 'Motif',
        }
        widgets = {
            'start_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',
                'placeholder': 'Sélectionnez la date et l\'heure de début'
            }),
            'end_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',
                'placeholder': 'Sélectionnez la date et l\'heure de fin'
            }),
            'reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Indiquez le motif de l\'absence'
            }),
        }

class CoefficientForm(forms.ModelForm):
    class Meta:
        model = Coefficient
        fields = ['school_class', 'subject', 'coefficient']
        labels = {
            'school_class': 'Classe',
            'subject': 'Matière',
            'coefficient': 'Coeffcient',
        }
        widgets = {
            'school_class': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'coefficient': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 5,  'placeholder': 'Entrez un coeffecient entre 1 et 5'}),
        }

class ClassSelectionForm(forms.Form):
    school_class = forms.ModelChoiceField(
        queryset=Class.objects.all(),
        label="Choisissez une classe",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class ScheduleStudentForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['class_name', 'day_of_week','subject', 'start_time', 'end_time']
        labels = {
            'class_name': 'Classe',
            'subject': 'Matière',
            'day_of_week': 'Jour de la semaine',
            'start_time': 'Heure de début',
            'end_time': 'Heure de fin',
        }
        widgets = {
            'class_name': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'day_of_week': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }


class ScheduleTeacherForm(forms.ModelForm):
    class Meta:
        model = TeacherSchedule
        fields = ['class_name', 'day_of_week', 'start_time', 'end_time']
        labels = {
            'class_name': 'Classe',
            'day_of_week': 'Jour de la semaine',
            'start_time': 'Heure de début',
            'end_time': 'Heure de fin',
        }
        widgets = {
            'class_name': forms.Select(attrs={'class': 'form-control'}),
            'day_of_week': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }