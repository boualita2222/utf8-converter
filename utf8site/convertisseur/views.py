from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import InscriptionForm, ConnexionForm
from .models import Historique
import sys
sys.path.insert(0, r"C:\PythonProjets")

from utf8_package.encodeur  import encoder_texte
from utf8_package.decodeur  import decoder_hex
from utf8_package.analyseur import analyser_char, analyser_texte


# ════════════════════════════════════════════
#  ACCUEIL
# ════════════════════════════════════════════
def accueil(request):
    nb_conversions = Historique.objects.count()
    return render(request,
                  'convertisseur/accueil.html',
                  {'nb_conversions': nb_conversions})


# ════════════════════════════════════════════
#  ENCODER
# ════════════════════════════════════════════
def encoder(request):
    resultat = None
    erreur   = None
    texte    = ""

    if request.method == "POST":
        texte = request.POST.get("texte", "").strip()
        if texte:
            try:
                res      = encoder_texte(texte)
                resultat = res
                Historique.objects.create(
                    user      = request.user if request.user.is_authenticated else None,
                    operation = "ENCODE",
                    entree    = texte,
                    sortie    = res["hex"],
                    nb_chars  = res["nb_chars"],
                    nb_octets = res["nb_octets"])
            except Exception as e:
                erreur = str(e)

    return render(request,
                  'convertisseur/encoder.html',
                  {'resultat': resultat,
                   'erreur':   erreur,
                   'texte':    texte})


# ════════════════════════════════════════════
#  DECODER
# ════════════════════════════════════════════
def decoder(request):
    resultat = None
    erreur   = None
    hex_str  = ""

    if request.method == "POST":
        hex_str = request.POST.get("hex", "").strip()
        if hex_str:
            try:
                res      = decoder_hex(hex_str)
                resultat = res
                Historique.objects.create(
                    user      = request.user if request.user.is_authenticated else None,
                    operation = "DECODE",
                    entree    = hex_str,
                    sortie    = res["texte"],
                    nb_chars  = len(res["texte"]),
                    nb_octets = len(res["details"]))
            except Exception as e:
                erreur = str(e)

    return render(request,
                  'convertisseur/decoder.html',
                  {'resultat': resultat,
                   'erreur':   erreur,
                   'hex_str':  hex_str})


# ════════════════════════════════════════════
#  ANALYSER
# ════════════════════════════════════════════
def analyser(request):
    resultat = None
    erreur   = None
    char     = ""

    if request.method == "POST":
        char = request.POST.get("char", "").strip()
        if char:
            try:
                resultat = analyser_char(char[0])
                Historique.objects.create(
                    user      = request.user if request.user.is_authenticated else None,
                    operation = "ANALYSE",
                    entree    = char[0],
                    sortie    = resultat["hex"],
                    nb_chars  = 1,
                    nb_octets = resultat["n"])
            except Exception as e:
                erreur = str(e)

    return render(request,
                  'convertisseur/analyser.html',
                  {'resultat': resultat,
                   'erreur':   erreur,
                   'char':     char})


# ════════════════════════════════════════════
#  STATS
# ════════════════════════════════════════════
def stats(request):
    resultat = None
    erreur   = None
    texte    = ""

    if request.method == "POST":
        texte = request.POST.get("texte", "").strip()
        if texte:
            try:
                resultat = analyser_texte(texte)
                Historique.objects.create(
                    user      = request.user if request.user.is_authenticated else None,
                    operation = "STATS",
                    entree    = texte,
                    sortie    = str(resultat["nb_octets"]) + " octets",
                    nb_chars  = resultat["nb_chars"],
                    nb_octets = resultat["nb_octets"])
            except Exception as e:
                erreur = str(e)

    return render(request,
                  'convertisseur/stats.html',
                  {'resultat': resultat,
                   'erreur':   erreur,
                   'texte':    texte})


# ════════════════════════════════════════════
#  HISTORIQUE
# ════════════════════════════════════════════
def historique(request):
    items = Historique.objects.all()[:20]
    return render(request,
                  'convertisseur/historique.html',
                  {'items': items})


# ════════════════════════════════════════════
#  INSCRIPTION
# ════════════════════════════════════════════
def inscription(request):
    if request.user.is_authenticated:
        return redirect('accueil')

    if request.method == "POST":
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Bienvenue " + user.username + " !")
            return redirect('accueil')
    else:
        form = InscriptionForm()

    return render(request,
                  'convertisseur/inscription.html',
                  {'form': form})


# ════════════════════════════════════════════
#  CONNEXION
# ════════════════════════════════════════════
def connexion(request):
    if request.user.is_authenticated:
        return redirect('accueil')

    if request.method == "POST":
        form = ConnexionForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Bonjour " + user.username + " !")
            return redirect('accueil')
        else:
            messages.error(request, "Nom ou mot de passe incorrect !")
    else:
        form = ConnexionForm(request)

    return render(request,
                  'convertisseur/connexion.html',
                  {'form': form})


# ════════════════════════════════════════════
#  DECONNEXION
# ════════════════════════════════════════════
def deconnexion(request):
    if request.method == "POST":
        logout(request)
        messages.info(request, "Vous etes deconnecte !")
    return redirect('connexion')


# ════════════════════════════════════════════
#  PROFIL
# ════════════════════════════════════════════
@login_required(login_url='connexion')
def profil(request):
    historique_user = Historique.objects.filter(
        user=request.user)[:10]
    return render(request,
                  'convertisseur/profil.html',
                  {'historique': historique_user})


# ════════════════════════════════════════════
#  COMPARAISON
# ════════════════════════════════════════════
def comparaison(request):
    resultat = None
    erreur   = None
    texte1   = ""
    texte2   = ""

    if request.method == "POST":
        texte1 = request.POST.get("texte1", "").strip()
        texte2 = request.POST.get("texte2", "").strip()

        if texte1 and texte2:
            try:
                from utf8_package.analyseur import comparer as comparer_textes
                res = comparer_textes(texte1, texte2)
                res["hex1"] = encoder_texte(texte1)["hex"]
                res["hex2"] = encoder_texte(texte2)["hex"]
                res["diff_octets"] = abs(res["oct1"] - res["oct2"])
                resultat = res

                Historique.objects.create(
                    user      = request.user if request.user.is_authenticated else None,
                    operation = "COMPARE",
                    entree    = texte1 + " vs " + texte2,
                    sortie    = str(len(res["differences"])) + " difference(s)",
                    nb_chars  = len(texte1) + len(texte2),
                    nb_octets = res["oct1"] + res["oct2"])

            except Exception as e:
                erreur = str(e)
        else:
            erreur = "Entrez les deux textes !"

    return render(request,
                  'convertisseur/comparaison.html',
                  {'resultat': resultat,
                   'erreur':   erreur,
                   'texte1':   texte1,
                   'texte2':   texte2})