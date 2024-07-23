from django.contrib import admin
from .models import Subject, Class, Note, Absence, Coefficient

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name',)
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'score', 'date')
    search_fields = ('student__user__username', 'subject__name')
    list_filter = ('subject', 'date')

@admin.register(Absence)
class AbsenceAdmin(admin.ModelAdmin):
    list_display = ('student', 'start_time', 'end_time', 'reason')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'reason')
    list_filter = ('start_time', 'end_time')

@admin.register(Coefficient)
class CoefficientAdmin(admin.ModelAdmin):
    list_display = ('school_class', 'subject', 'coefficient')
    list_filter = ('school_class', 'subject')

