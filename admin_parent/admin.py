from django.contrib import admin
from .models import Motif, Creneau, RendezVous

@admin.register(Motif)
class MotifAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description')
    search_fields = ('nom',)

@admin.register(Creneau)
class CreneauAdmin(admin.ModelAdmin):
    list_display = ('date', 'heure', 'disponible')
    list_filter = ('date', 'disponible')
    search_fields = ('date', 'heure')

@admin.register(RendezVous)
class RendezVousAdmin(admin.ModelAdmin):
    list_display = ('parent', 'motif', 'autre_motif', 'creneau')
    list_filter = ('parent', 'motif')
    search_fields = ('parent__nom', 'motif__nom', 'autre_motif', 'creneau__date', 'creneau__heure')
