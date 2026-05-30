from django.contrib import admin
from .models import Historique, Favori

@admin.register(Historique)
class HistoriqueAdmin(admin.ModelAdmin):
    list_display  = ['operation', 'entree',
                     'sortie', 'nb_octets',
                     'date']
    list_filter   = ['operation', 'date']
    search_fields = ['entree', 'sortie']
    readonly_fields = ['date']
    ordering      = ['-date']

@admin.register(Favori)
class FavoriAdmin(admin.ModelAdmin):
    list_display  = ['nom', 'texte',
                     'hex_utf8', 'date']
    search_fields = ['nom', 'texte']
    ordering      = ['nom']