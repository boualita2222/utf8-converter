from django.urls import path
from . import views

urlpatterns = [
    path('',
         views.accueil,      name='accueil'),
    path('encoder/',
         views.encoder,      name='encoder'),
    path('decoder/',
         views.decoder,      name='decoder'),
    path('analyser/',
         views.analyser,     name='analyser'),
    path('stats/',
         views.stats,        name='stats'),
    path('historique/',
         views.historique,   name='historique'),
    path('inscription/',
         views.inscription,  name='inscription'),
    path('connexion/',
         views.connexion,    name='connexion'),
    path('deconnexion/',
         views.deconnexion,  name='deconnexion'),
    path('profil/',
         views.profil,       name='profil'),
]