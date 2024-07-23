from django.contrib import admin
from .models import Actualite, Evenement, Annale

@admin.register(Actualite)
class ActualiteAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date_publiée')  # Colonnes affichées dans la liste
    search_fields = ('titre', 'description')  # Champs pour la recherche
    list_filter = ('date_publiée',)  # Filtres pour la liste
    date_hierarchy = 'date_publiée'  # Hiérarchie de date pour filtrer

@admin.register(Evenement)
class EvenementAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date')  # Colonnes affichées dans la liste
    search_fields = ('titre', 'description')  # Champs pour la recherche
    list_filter = ('date',)  # Filtres pour la liste
    date_hierarchy = 'date'  # Hiérarchie de date pour filtrer

@admin.register(Annale)
class AnnaleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')  # Champs à afficher dans la liste des annales
    search_fields = ('title', 'description')  # Champs à utiliser pour la recherche
    ordering = ('-created_at',)