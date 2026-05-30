#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF Tools - Lire, Creer, Modifier des PDF
Python 3.14.2
"""

import os
import sys

try:
    from colorama import init, Fore, Style
    init(autoreset=False, strip=False, convert=True)
except ImportError:
    class _D:
        def __getattr__(self, _): return ""
    Fore = Style = _D()

G  = Fore.GREEN  + Style.BRIGHT
Y  = Fore.YELLOW + Style.BRIGHT
C  = Fore.CYAN   + Style.BRIGHT
W  = Fore.WHITE
D  = Style.DIM   + Fore.WHITE
R  = Style.RESET_ALL
RE = Fore.RED    + Style.BRIGHT
LN = G + "=" * 55 + R


# ════════════════════════════════════════════
#  MODULE 1 - LIRE UN PDF
# ════════════════════════════════════════════
def lire_pdf(chemin):
    """Lit et extrait le texte d'un PDF"""
    try:
        from pypdf import PdfReader
        reader   = PdfReader(chemin)
        nb_pages = len(reader.pages)

        print(G + "\n  PDF : " + chemin + R)
        print(C + "  Pages : " + str(nb_pages) + R)
        print(LN)

        texte_complet = ""
        for i, page in enumerate(reader.pages, 1):
            texte = page.extract_text()
            texte_complet += texte + "\n"
            print(Y + "\n  PAGE " + str(i) + "/" + str(nb_pages) + R)
            print(W + texte[:500] + R)
            if len(texte) > 500:
                print(D + "  ... (" + str(len(texte)) + " caracteres total)" + R)

        return texte_complet

    except FileNotFoundError:
        print(RE + "  Fichier introuvable : " + chemin + R)
        return None
    except Exception as e:
        print(RE + "  Erreur : " + str(e) + R)
        return None


def infos_pdf(chemin):
    """Affiche les metadonnees d'un PDF"""
    try:
        from pypdf import PdfReader
        reader = PdfReader(chemin)
        meta   = reader.metadata

        print(G + "\n  Metadonnees PDF :" + R)
        print("  " + Y + "Pages    :" + R + " " + W + str(len(reader.pages)) + R)

        if meta:
            champs = {
                '/Title':    'Titre',
                '/Author':   'Auteur',
                '/Creator':  'Createur',
                '/Producer': 'Producteur',
                '/Subject':  'Sujet',
            }
            for key, label in champs.items():
                val = meta.get(key, '')
                if val:
                    print("  " + Y + label.ljust(12) + ":" + R + " " + W + str(val) + R)

    except Exception as e:
        print(RE + "  Erreur : " + str(e) + R)


# ════════════════════════════════════════════
#  MODULE 2 - CREER UN PDF SIMPLE
# ════════════════════════════════════════════
def creer_pdf_simple(chemin, titre, contenu):
    """Cree un PDF simple avec du texte"""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import cm
        from reportlab.lib import colors

        c = canvas.Canvas(chemin, pagesize=A4)
        largeur, hauteur = A4

        # Fond blanc
        c.setFillColor(colors.white)
        c.rect(0, 0, largeur, hauteur, fill=True, stroke=False)

        # Titre
        c.setFillColor(colors.HexColor('#007700'))
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(largeur/2, hauteur - 3*cm, titre)

        # Ligne separatrice
        c.setStrokeColor(colors.HexColor('#007700'))
        c.setLineWidth(2)
        c.line(2*cm, hauteur - 4*cm, largeur - 2*cm, hauteur - 4*cm)

        # Contenu
        c.setFillColor(colors.HexColor('#333333'))
        c.setFont("Helvetica", 12)

        y = hauteur - 5*cm
        for ligne in contenu.split('\n'):
            if y < 2*cm:
                c.showPage()
                c.setFillColor(colors.white)
                c.rect(0, 0, largeur, hauteur, fill=True, stroke=False)
                c.setFillColor(colors.HexColor('#333333'))
                c.setFont("Helvetica", 12)
                y = hauteur - 2*cm
            c.drawString(2*cm, y, ligne)
            y -= 0.6*cm

        # Footer
        c.setFillColor(colors.HexColor('#999999'))
        c.setFont("Helvetica", 9)
        c.drawCentredString(largeur/2, 1*cm,
            "Genere par UTF-8 Converter Pro - Python 3.14.2")

        c.save()
        print(G + "\n  PDF cree : " + chemin + R)
        return True

    except Exception as e:
        print(RE + "  Erreur : " + str(e) + R)
        return False


# ════════════════════════════════════════════
#  MODULE 3 - CREER RAPPORT PROFESSIONNEL
# ════════════════════════════════════════════
def creer_rapport_utf8(chemin, analyses):
    """Cree un rapport PDF professionnel"""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import cm
        from reportlab.lib import colors
        from reportlab.platypus import (
            SimpleDocTemplate, Table,
            TableStyle, Paragraph, Spacer)
        from reportlab.lib.styles import (
            getSampleStyleSheet, ParagraphStyle)
        from datetime import datetime

        doc    = SimpleDocTemplate(chemin, pagesize=A4,
                    rightMargin=2*cm, leftMargin=2*cm,
                    topMargin=2*cm, bottomMargin=2*cm)
        styles = getSampleStyleSheet()
        story  = []

        # Style titre
        titre_style = ParagraphStyle(
            'titre',
            parent=styles['Title'],
            fontSize=20,
            textColor=colors.HexColor('#007700'),
            spaceAfter=12)

        # Style normal
        normal_style = ParagraphStyle(
            'normal',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=6)

        # Titre
        story.append(Paragraph(
            "Rapport UTF-8 Converter Pro", titre_style))
        story.append(Spacer(1, 0.5*cm))

        # Date
        date_str = datetime.now().strftime("%d/%m/%Y %H:%M")
        story.append(Paragraph(
            "Genere le : " + date_str, normal_style))
        story.append(Spacer(1, 1*cm))

        # Tableau
        if analyses:
            story.append(Paragraph(
                "Analyses UTF-8 :",
                ParagraphStyle('h2',
                    parent=styles['Heading2'],
                    fontSize=14,
                    textColor=colors.HexColor('#cc8800'))))
            story.append(Spacer(1, 0.3*cm))

            data = [['Texte', 'Hex UTF-8', 'Chars', 'Octets']]
            for a in analyses:
                data.append([
                    str(a.get('texte', ''))[:20],
                    str(a.get('hex', ''))[:25],
                    str(a.get('nb_chars', '')),
                    str(a.get('nb_octets', '')),
                ])

            table = Table(data,
                colWidths=[5*cm, 7*cm, 2*cm, 2*cm])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0),
                 colors.HexColor('#1e5c1e')),
                ('TEXTCOLOR', (0,0), (-1,0),
                 colors.white),
                ('FONTNAME', (0,0), (-1,0),
                 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,-1), 10),
                ('ROWBACKGROUNDS', (0,1), (-1,-1),
                 [colors.white,
                  colors.HexColor('#f0f0f0')]),
                ('GRID', (0,0), (-1,-1),
                 0.5, colors.HexColor('#cccccc')),
                ('ALIGN', (2,0), (-1,-1), 'CENTER'),
                ('PADDING', (0,0), (-1,-1), 6),
            ]))
            story.append(table)

        doc.build(story)
        print(G + "\n  Rapport PDF : " + chemin + R)
        return True

    except Exception as e:
        print(RE + "  Erreur : " + str(e) + R)
        return False


# ════════════════════════════════════════════
#  MODULE 4 - FUSIONNER DES PDF
# ════════════════════════════════════════════
def fusionner_pdf(chemins_entree, chemin_sortie):
    """Fusionne plusieurs PDF en un seul"""
    try:
        from pypdf import PdfWriter, PdfReader

        writer = PdfWriter()
        for chemin in chemins_entree:
            reader = PdfReader(chemin)
            for page in reader.pages:
                writer.add_page(page)
            print(C + "  + " + chemin +
                  " (" + str(len(reader.pages)) + " pages)" + R)

        with open(chemin_sortie, 'wb') as f:
            writer.write(f)

        print(G + "\n  Fusion OK : " + chemin_sortie + R)
        return True

    except Exception as e:
        print(RE + "  Erreur : " + str(e) + R)
        return False


# ════════════════════════════════════════════
#  PROGRAMME PRINCIPAL
# ════════════════════════════════════════════
def main():
    os.system("cls" if os.name == "nt" else "clear")
    print(G + """
╔══════════════════════════════════════════════════════╗
║         PDF TOOLS - Python 3.14.2                   ║
║         Lire, Creer, Modifier des PDF               ║
╚══════════════════════════════════════════════════════╝""" + R)

    # Test 1 - Creer un PDF simple
    print(Y + "\n  [1] Creation PDF simple...\n" + R)
    creer_pdf_simple(
        r"C:\PythonProjets\test_simple.pdf",
        "UTF-8 Converter Pro",
        "Bonjour mon ami !\n\n"
        "Ce PDF a ete cree avec Python 3.14.2\n"
        "et la bibliotheque ReportLab.\n\n"
        "Caracteres UTF-8 :\n"
        "- cafe  (4 chars, 4 octets)\n"
        "- Bonjour (7 chars, 7 octets)\n\n"
        "Encodage UTF-8 :\n"
        "A       = 41h (1 octet)\n"
        "e accent = C3 A9h (2 octets)\n"
        "Euro    = E2 82 ACh (3 octets)\n")

    # Test 2 - Rapport professionnel
    print(Y + "\n  [2] Creation rapport PDF...\n" + R)
    sys.path.insert(0, r"C:\PythonProjets")
    try:
        from utf8_package.encodeur import encoder_texte
        analyses = []
        for texte in ["cafe", "Bonjour", "Python", "Django"]:
            res = encoder_texte(texte)
            analyses.append(res)
        creer_rapport_utf8(
            r"C:\PythonProjets\rapport_utf8.pdf",
            analyses)
    except Exception as e:
        print(D + "  Note : " + str(e) + R)

    # Test 3 - Lire le PDF
    print(Y + "\n  [3] Lecture du PDF cree...\n" + R)
    lire_pdf(r"C:\PythonProjets\test_simple.pdf")

    # Test 4 - Infos PDF
    print(Y + "\n  [4] Infos PDF...\n" + R)
    infos_pdf(r"C:\PythonProjets\test_simple.pdf")

    print()
    print(LN)
    print(G + "\n  PDF Tools OK !\n" + R)
    print(W + "  Fichiers crees :\n"
          "  C:\\PythonProjets\\test_simple.pdf\n"
          "  C:\\PythonProjets\\rapport_utf8.pdf\n" + R)
    input(D + "  Entree pour quitter..." + R)


if __name__ == "__main__":
    main()