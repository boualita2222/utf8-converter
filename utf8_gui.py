#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UTF-8 CONVERTER — Interface Graphique + SQLite
Python 3.14.2 + Tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import tkinter.simpledialog as sd
import unicodedata
import os
import sys
sys.path.insert(0, r"C:\PythonProjets")

from utf8_package.encodeur  import encoder_texte
from utf8_package.decodeur  import decoder_hex
from utf8_package.analyseur import (analyser_char,
                                     analyser_texte,
                                     comparer)
from utf8_db import UTF8Database

# ════════════════════════════════════════════
#  COULEURS ET FONTS
# ════════════════════════════════════════════
COULEURS = {
    "bg":        "#0d0d0d",
    "panel":     "#111111",
    "green":     "#00ff41",
    "yellow":    "#ffb000",
    "cyan":      "#00e5ff",
    "magenta":   "#ff79c6",
    "red":       "#ff4444",
    "white":     "#e0e0e0",
    "dim":       "#555555",
    "btn_bg":    "#0a0a0a",
    "btn_hover": "#1a2a1a",
}

FONTS = {
    "mono":    ("Courier New", 11),
    "mono_lg": ("Courier New", 13),
    "mono_sm": ("Courier New", 10),
    "title":   ("Courier New", 14, "bold"),
    "header":  ("Courier New", 12, "bold"),
}


# ════════════════════════════════════════════
#  CLASSE PRINCIPALE
# ════════════════════════════════════════════
class UTF8GUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("UTF-8 Converter — Python 3.14.2")
        self.root.geometry("950x720")
        self.root.configure(bg=COULEURS["bg"])
        self.root.resizable(True, True)

        # Fermeture propre
        self.root.protocol("WM_DELETE_WINDOW", self._fermer)

        # Variables
        self.var_status = tk.StringVar()
        self.var_status.set("Pret — Entrez du texte ou du hex")

        # Base de données
        self.db = UTF8Database()

        # Construction interface
        self._build_header()
        self._build_tabs()
        self._build_statusbar()

        # Raccourcis
        self.root.bind("<Control-l>", lambda e: self._effacer_tout())
        self._onglet_actif = "encoder"

    # ────────────────────────────────────────
    #  HEADER
    # ────────────────────────────────────────
    def _build_header(self):
        header = tk.Frame(self.root, bg=COULEURS["panel"], pady=8)
        header.pack(fill="x")
        tk.Label(header, text="UTF-8 CONVERTER + SQLite",
                 font=FONTS["title"], fg=COULEURS["green"],
                 bg=COULEURS["panel"]).pack()
        tk.Label(header, text="Python 3.14.2 + Tkinter + SQLite",
                 font=FONTS["mono_sm"], fg=COULEURS["dim"],
                 bg=COULEURS["panel"]).pack()

    # ────────────────────────────────────────
    #  ONGLETS
    # ────────────────────────────────────────
    def _build_tabs(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook",
                         background=COULEURS["bg"], borderwidth=0)
        style.configure("TNotebook.Tab",
                         background=COULEURS["panel"],
                         foreground=COULEURS["dim"],
                         font=FONTS["mono"], padding=[10, 5])
        style.map("TNotebook.Tab",
                   background=[("selected", COULEURS["bg"])],
                   foreground=[("selected", COULEURS["green"])])

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)

        self._build_tab_encoder()
        self._build_tab_decoder()
        self._build_tab_analyser()
        self._build_tab_comparer()
        self._build_tab_stats()
        self._build_tab_historique()

        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_change)

    # ────────────────────────────────────────
    #  ONGLET 1 — ENCODER
    # ────────────────────────────────────────
    def _build_tab_encoder(self):
        frame = tk.Frame(self.notebook, bg=COULEURS["bg"])
        self.notebook.add(frame, text=" [1] ENCODER ")

        self._label(frame, "Texte a encoder :")
        self.enc_input = self._entry(frame)
        self.enc_input.bind("<Return>", lambda e: self._encoder())

        bf = tk.Frame(frame, bg=COULEURS["bg"])
        bf.pack(fill="x", padx=10)
        self._btn(bf, "Encoder", self._encoder, COULEURS["green"])
        self._btn(bf, "Effacer", self._effacer_enc, COULEURS["red"])

        self._label(frame, "Resultat :")
        self.enc_output = self._text(frame, 6)
        self._label(frame, "Details :")
        self.enc_detail = self._text(frame, 8)

    # ────────────────────────────────────────
    #  ONGLET 2 — DECODER
    # ────────────────────────────────────────
    def _build_tab_decoder(self):
        frame = tk.Frame(self.notebook, bg=COULEURS["bg"])
        self.notebook.add(frame, text=" [2] DECODER ")

        self._label(frame, "Sequence hex UTF-8 :")
        self._label(frame, "  Exemple : C3 A9 20 E2 82 AC", COULEURS["dim"])
        self.dec_input = self._entry(frame)
        self.dec_input.bind("<Return>", lambda e: self._decoder())

        bf = tk.Frame(frame, bg=COULEURS["bg"])
        bf.pack(fill="x", padx=10)
        self._btn(bf, "Decoder", self._decoder, COULEURS["cyan"])
        self._btn(bf, "Effacer", self._effacer_dec, COULEURS["red"])

        self._label(frame, "Texte decode :")
        self.dec_output = self._text(frame, 4)
        self._label(frame, "Details :")
        self.dec_detail = self._text(frame, 10)

    # ────────────────────────────────────────
    #  ONGLET 3 — ANALYSER
    # ────────────────────────────────────────
    def _build_tab_analyser(self):
        frame = tk.Frame(self.notebook, bg=COULEURS["bg"])
        self.notebook.add(frame, text=" [3] ANALYSER ")

        self._label(frame, "Entrez un caractere :")
        self.ana_input = self._entry(frame)
        self.ana_input.bind("<Return>", lambda e: self._analyser())
        self.ana_input.bind("<KeyRelease>", lambda e: self._analyser_live())

        bf = tk.Frame(frame, bg=COULEURS["bg"])
        bf.pack(fill="x", padx=10)
        self._btn(bf, "Analyser", self._analyser, COULEURS["yellow"])

        self._label(frame, "Analyse complete :")
        self.ana_output = self._text(frame, 20)

    # ────────────────────────────────────────
    #  ONGLET 4 — COMPARER
    # ────────────────────────────────────────
    def _build_tab_comparer(self):
        frame = tk.Frame(self.notebook, bg=COULEURS["bg"])
        self.notebook.add(frame, text=" [4] COMPARER ")

        self._label(frame, "Texte 1 :")
        self.cmp_input1 = self._entry(frame)
        self._label(frame, "Texte 2 :")
        self.cmp_input2 = self._entry(frame)

        bf = tk.Frame(frame, bg=COULEURS["bg"])
        bf.pack(fill="x", padx=10)
        self._btn(bf, "Comparer", self._comparer, COULEURS["magenta"])
        self._btn(bf, "Effacer", self._effacer_cmp, COULEURS["red"])

        self._label(frame, "Resultat :")
        self.cmp_output = self._text(frame, 18)

    # ────────────────────────────────────────
    #  ONGLET 5 — STATS
    # ────────────────────────────────────────
    def _build_tab_stats(self):
        frame = tk.Frame(self.notebook, bg=COULEURS["bg"])
        self.notebook.add(frame, text=" [5] STATS ")

        self._label(frame, "Texte a analyser :")
        self.stats_input = self._entry(frame)
        self.stats_input.bind("<Return>", lambda e: self._stats())

        bf = tk.Frame(frame, bg=COULEURS["bg"])
        bf.pack(fill="x", padx=10)
        self._btn(bf, "Analyser", self._stats, COULEURS["cyan"])

        self._label(frame, "Statistiques :")
        self.stats_output = self._text(frame, 20)

    # ────────────────────────────────────────
    #  ONGLET 6 — HISTORIQUE
    # ────────────────────────────────────────
    def _build_tab_historique(self):
        frame = tk.Frame(self.notebook, bg=COULEURS["bg"])
        self.notebook.add(frame, text=" [6] HISTORIQUE ")

        # Recherche
        self._label(frame, "Rechercher :")
        sf = tk.Frame(frame, bg=COULEURS["bg"])
        sf.pack(fill="x", padx=10)
        self.hist_search = tk.Entry(
            sf, font=FONTS["mono"],
            fg=COULEURS["green"],
            bg=COULEURS["btn_bg"],
            insertbackground=COULEURS["green"],
            relief="flat", bd=5)
        self.hist_search.pack(side="left", fill="x", expand=True)
        self._btn(sf, "Chercher", self._rechercher_hist, COULEURS["cyan"])
        self._btn(sf, "Tout voir", self._refresh_historique, COULEURS["green"])

        # Boutons
        bf = tk.Frame(frame, bg=COULEURS["bg"])
        bf.pack(fill="x", padx=10)
        self._btn(bf, "Ajouter favori", self._ajouter_favori, COULEURS["yellow"])
        self._btn(bf, "Voir favoris", self._voir_favoris, COULEURS["magenta"])
        self._btn(bf, "Resume DB", self._voir_resume, COULEURS["cyan"])
        self._btn(bf, "Effacer tout", self._effacer_hist, COULEURS["red"])

        # Historique
        self._label(frame, "Historique des conversions :")
        self.hist_output = self._text(frame, 12)

        # Favoris
        self._label(frame, "Favoris :")
        self.fav_output = self._text(frame, 6)

        # Charger au démarrage
        self.root.after(500, self._refresh_historique)

    # ────────────────────────────────────────
    #  BARRE DE STATUT
    # ────────────────────────────────────────
    def _build_statusbar(self):
        sb = tk.Frame(self.root, bg=COULEURS["panel"], pady=4)
        sb.pack(fill="x", side="bottom")
        tk.Label(sb, textvariable=self.var_status,
                  font=FONTS["mono_sm"], fg=COULEURS["dim"],
                  bg=COULEURS["panel"], anchor="w", padx=10).pack(fill="x")

    # ────────────────────────────────────────
    #  WIDGETS HELPERS
    # ────────────────────────────────────────
    def _label(self, parent, text, color=None):
        tk.Label(parent, text=text, font=FONTS["mono_sm"],
                  fg=color or COULEURS["yellow"],
                  bg=COULEURS["bg"], anchor="w", padx=10
                  ).pack(fill="x", pady=(6, 0))

    def _entry(self, parent):
        e = tk.Entry(parent, font=FONTS["mono_lg"],
                      fg=COULEURS["green"], bg=COULEURS["btn_bg"],
                      insertbackground=COULEURS["green"],
                      relief="flat", bd=5)
        e.pack(fill="x", padx=10, pady=4)
        return e

    def _text(self, parent, height=6):
        t = scrolledtext.ScrolledText(
            parent, font=FONTS["mono_sm"],
            fg=COULEURS["white"], bg=COULEURS["btn_bg"],
            insertbackground=COULEURS["green"],
            relief="flat", bd=5, height=height,
            state="disabled")
        t.pack(fill="both", expand=True, padx=10, pady=4)
        return t

    def _btn(self, parent, text, command, color):
        b = tk.Button(parent, text=text, font=FONTS["mono"],
                       fg=color, bg=COULEURS["btn_bg"],
                       activeforeground=color,
                       activebackground=COULEURS["btn_hover"],
                       relief="flat", bd=1, padx=12, pady=4,
                       cursor="hand2", command=command)
        b.pack(side="left", padx=5, pady=6)
        return b

    def _write(self, widget, text, clear=True):
        widget.configure(state="normal")
        if clear:
            widget.delete("1.0", "end")
        widget.insert("end", text)
        widget.configure(state="disabled")

    def _status(self, msg):
        self.var_status.set(msg)

    # ────────────────────────────────────────
    #  ACTION 1 — ENCODER
    # ────────────────────────────────────────
    def _encoder(self):
        texte = self.enc_input.get().strip()
        if not texte:
            messagebox.showwarning("Attention", "Entrez du texte !")
            return
        try:
            res = encoder_texte(texte)

            out  = "Texte    : " + res['texte'] + "\n"
            out += "Hex      : " + res['hex'] + "\n"
            out += "Chars    : " + str(res['nb_chars']) + "\n"
            out += "Octets   : " + str(res['nb_octets']) + "\n"
            self._write(self.enc_output, out)

            det = ""
            for d in res["details"]:
                det += ("  " + d['char'] + "  " +
                        "U+" + format(d['cp'], '04X') + "  " +
                        d['hex'] + "  " +
                        str(d['n']) + " oct\n")
            self._write(self.enc_detail, det)

            self._status("OK Encode : " + str(res['nb_chars']) +
                          " chars -> " + str(res['nb_octets']) + " octets")

            # Sauvegarde DB
            self.db.ajouter_historique(
                "ENCODE", texte, res["hex"],
                res["nb_chars"], res["nb_octets"])
            self._refresh_historique()

        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def _effacer_enc(self):
        self.enc_input.delete(0, "end")
        self._write(self.enc_output, "")
        self._write(self.enc_detail, "")
        self._status("Efface")

    # ────────────────────────────────────────
    #  ACTION 2 — DECODER
    # ────────────────────────────────────────
    def _decoder(self):
        hex_str = self.dec_input.get().strip()
        if not hex_str:
            messagebox.showwarning("Attention", "Entrez une sequence hex !")
            return
        try:
            res = decoder_hex(hex_str)

            self._write(self.dec_output,
                         "Texte decode : " + res['texte'] + "\n")

            det = ""
            for d in res["details"]:
                det += ("  " + d['hex'].ljust(15) +
                        "->  " + d['char'] + "  " +
                        "U+" + format(d['cp'], '04X') + "  " +
                        str(d['n']) + " oct\n")
            self._write(self.dec_detail, det)

            self._status("OK Decode : " + str(len(res['details'])) + " caracteres")

            # Sauvegarde DB
            self.db.ajouter_historique(
                "DECODE", hex_str, res["texte"],
                len(res["texte"]), len(res["details"]))
            self._refresh_historique()

        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def _effacer_dec(self):
        self.dec_input.delete(0, "end")
        self._write(self.dec_output, "")
        self._write(self.dec_detail, "")
        self._status("Efface")

    # ────────────────────────────────────────
    #  ACTION 3 — ANALYSER
    # ────────────────────────────────────────
    def _analyser(self):
        c = self.ana_input.get().strip()
        if not c:
            return
        try:
            res = analyser_char(c[0])

            try:
                res['char'].encode('cp1252')
                char_display = res['char']
            except Exception:
                char_display = "U+" + format(res['cp'], '04X')

            out  = "  Caractere   : " + char_display + "\n"
            out += "  Codepoint   : U+" + format(res['cp'], '04X') + "\n"
            out += "  Decimal     : " + str(res['cp']) + "\n"
            out += "  Hex UTF-8   : " + res['hex'] + "\n"
            out += "  Binaire     : " + res['bin'] + "\n"
            out += "  Octets      : " + str(res['n']) + "\n"
            out += "  Dec. brut   : " + str(res['raw_int']) + "\n"
            out += "  Nom Unicode : " + res['nom'] + "\n"
            out += "  Categorie   : " + res['cat'] + "\n"
            out += "\n" + "-"*40 + "\n"
            out += "  Schema UTF-8 :\n"
            out += self._schema_utf8(res['cp'], res['n'])
            self._write(self.ana_output, out)

            self._status("U+" + format(res['cp'], '04X') +
                          " = " + res['hex'] + " = " + res['nom'])

            # Sauvegarde DB
            self.db.ajouter_historique(
                "ANALYSE", c[0], res["hex"], 1, res["n"])
            self._refresh_historique()

        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def _analyser_live(self):
        c = self.ana_input.get().strip()
        if c:
            self._analyser()

    def _schema_utf8(self, cp, n):
        templates = {
            1: ["0xxxxxxx"],
            2: ["110xxxxx", "10xxxxxx"],
            3: ["1110xxxx", "10xxxxxx", "10xxxxxx"],
            4: ["11110xxx", "10xxxxxx", "10xxxxxx", "10xxxxxx"],
        }
        payload = [7, 11, 16, 21][n-1]
        bits    = format(cp, '0' + str(payload) + 'b')
        result  = ""
        idx     = 0
        raw     = chr(cp).encode("utf-8")
        for i, tmpl in enumerate(templates[n]):
            filled = ""
            for ch in tmpl:
                if ch == "x":
                    filled += bits[idx]
                    idx += 1
                else:
                    filled += ch
            bv = raw[i]
            result += ("    Octet " + str(i+1) + " : " +
                       filled + "   (" +
                       format(bv, '02X') + "h = " +
                       str(bv) + ")\n")
        return result

    # ────────────────────────────────────────
    #  ACTION 4 — COMPARER
    # ────────────────────────────────────────
    def _comparer(self):
        t1 = self.cmp_input1.get().strip()
        t2 = self.cmp_input2.get().strip()
        if not t1 or not t2:
            messagebox.showwarning("Attention", "Entrez les deux textes !")
            return
        try:
            res = comparer(t1, t2)
            out  = "  Texte 1 : " + t1 + "\n"
            out += "  Texte 2 : " + t2 + "\n"
            out += "  Octets 1 : " + str(res['oct1']) + "\n"
            out += "  Octets 2 : " + str(res['oct2']) + "\n"
            out += "-"*45 + "\n"
            if res["identiques"]:
                out += "  IDENTIQUES !\n"
            else:
                nb = len(res["differences"])
                out += "  " + str(nb) + " difference(s) :\n\n"
                for d in res["differences"]:
                    c1 = d["c1"] or "-"
                    c2 = d["c2"] or "-"
                    out += ("  Pos " + str(d['pos']) + " : '" +
                            c1 + "' " + d['h1'] +
                            "  !=  '" +
                            c2 + "' " + d['h2'] + "\n")
            self._write(self.cmp_output, out)

            status = ("Identiques !" if res["identiques"]
                       else str(len(res['differences'])) + " difference(s)")
            self._status(status)

            # Sauvegarde DB
            self.db.ajouter_historique(
                "COMPARE",
                t1 + " vs " + t2,
                str(len(res["differences"])) + " diff.",
                len(t1) + len(t2),
                res["oct1"] + res["oct2"])
            self._refresh_historique()

        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def _effacer_cmp(self):
        self.cmp_input1.delete(0, "end")
        self.cmp_input2.delete(0, "end")
        self._write(self.cmp_output, "")
        self._status("Efface")

    # ────────────────────────────────────────
    #  ACTION 5 — STATS
    # ────────────────────────────────────────
    def _stats(self):
        texte = self.stats_input.get().strip()
        if not texte:
            messagebox.showwarning("Attention", "Entrez du texte !")
            return
        try:
            res = analyser_texte(texte)
            labels = {
                1: "ASCII    (1 oct)",
                2: "Latin    (2 oct)",
                3: "Symboles (3 oct)",
                4: "Emojis   (4 oct)",
            }
            out  = "  Texte      : " + texte + "\n"
            out += "  Caracteres : " + str(res['nb_chars']) + "\n"
            out += "  Octets     : " + str(res['nb_octets']) + "\n"
            out += "  ASCII%     : " + str(round(res['pct_ascii'], 1)) + "%\n"
            out += "-"*45 + "\n"

            for n in range(1, 5):
                chars = res["types"][n]
                if not chars:
                    continue
                nb  = len(chars)
                pct = nb * n / res['nb_octets'] * 100
                bar = "=" * int(pct / 4)
                uniques = ""
                for ch in dict.fromkeys(chars):
                    try:
                        ch.encode('cp1252')
                        uniques += ch
                    except Exception:
                        uniques += "[U+" + format(ord(ch), '04X') + "]"
                    if len(uniques) > 30:
                        break
                out += "\n  " + labels[n] + "\n"
                out += "    Chars  : " + str(nb) + "  (" + str(round(pct, 1)) + "%)\n"
                out += "    " + bar + "\n"
                out += "    Uniques: " + uniques + "\n"

            self._write(self.stats_output, out)
            self._status("OK " + str(res['nb_chars']) +
                          " chars -> " + str(res['nb_octets']) + " octets")

            # Sauvegarde DB
            self.db.ajouter_stats(texte, res)
            self._refresh_historique()

        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    # ────────────────────────────────────────
    #  ACTIONS HISTORIQUE
    # ────────────────────────────────────────
    def _refresh_historique(self):
        try:
            rows = self.db.get_historique(15)
            if not rows:
                self._write(self.hist_output, "  Historique vide.\n")
                return
            out  = "  " + "ID  ".ljust(4) + "OP".ljust(10)
            out += "ENTREE".ljust(20) + "SORTIE".ljust(18)
            out += "OCT  DATE\n"
            out += "  " + "-"*68 + "\n"
            for row in rows:
                entree = str(row['entree'])[:17]
                sortie = str(row['sortie'])[:16]
                out += ("  #" + str(row['id']).ljust(3) +
                         row['operation'].ljust(10) +
                         entree.ljust(20) +
                         sortie.ljust(18) +
                         str(row['nb_octets']).ljust(5) +
                         row['date'] + "\n")
            self._write(self.hist_output, out)
        except Exception as e:
            self._write(self.hist_output, "  Erreur : " + str(e) + "\n")

    def _rechercher_hist(self):
        motif = self.hist_search.get().strip()
        if not motif:
            self._refresh_historique()
            return
        try:
            rows = self.db.rechercher(motif)
            if not rows:
                self._write(self.hist_output,
                              "  Aucun resultat pour '" + motif + "'\n")
                return
            out = "  Resultats pour '" + motif + "' :\n\n"
            for row in rows:
                out += ("  #" + str(row['id']).ljust(3) +
                         row['operation'].ljust(10) +
                         str(row['entree'])[:20].ljust(22) +
                         "-> " + str(row['sortie'])[:20] + "\n")
            self._write(self.hist_output, out)
            self._status("OK " + str(len(rows)) +
                          " resultat(s) pour '" + motif + "'")
        except Exception as e:
            self._write(self.hist_output, "  Erreur : " + str(e) + "\n")

    def _ajouter_favori(self):
        try:
            rows = self.db.get_historique(1)
            if not rows:
                self._status("Aucune conversion !")
                return
            row = rows[0]
            nom = sd.askstring(
                "Favori",
                "Nom du favori :",
                initialvalue=str(row['entree'])[:15])
            if nom:
                self.db.ajouter_favori(
                    nom,
                    str(row['entree']),
                    str(row['sortie']))
                self._voir_favoris()
                self._status("Favori ajoute : " + nom)
        except Exception as e:
            self._status("Erreur : " + str(e))

    def _voir_favoris(self):
        try:
            rows = self.db.get_favoris()
            if not rows:
                self._write(self.fav_output, "  Aucun favori.\n")
                return
            out = ""
            for row in rows:
                out += ("  #" + str(row['id']).ljust(3) +
                         row['nom'].ljust(15) +
                         str(row['texte']).ljust(12) +
                         str(row['hex'])[:25] + "\n")
            self._write(self.fav_output, out)
        except Exception as e:
            self._write(self.fav_output, "  Erreur : " + str(e) + "\n")

    def _voir_resume(self):
        try:
            stats = self.db.get_resumé()
            out  = "  Resume base de donnees :\n\n"
            out += "  Total operations : " + str(stats['total_ops']) + "\n"
            out += "  Total octets     : " + str(stats['total_octets']) + "\n"
            out += "  Favoris          : " + str(stats['nb_favoris']) + "\n\n"
            if stats["par_type"]:
                out += "  Par type :\n"
                for op, nb in stats["par_type"].items():
                    out += "    " + op.ljust(12) + str(nb) + "\n"
            if stats["plus_long"]:
                pl = stats["plus_long"]
                out += ("\n  Plus long :\n  " +
                         pl['entree'][:30] +
                         " (" + str(pl['nb_octets']) + " oct)\n")
            self._write(self.hist_output, out)
            self._status("DB : " + str(stats['total_ops']) +
                          " ops, " + str(stats['nb_favoris']) + " favoris")
        except Exception as e:
            self._write(self.hist_output, "  Erreur : " + str(e) + "\n")

    def _effacer_hist(self):
        if messagebox.askyesno("Confirmation", "Effacer TOUT l'historique ?"):
            nb = self.db.supprimer_historique()
            self._refresh_historique()
            self._status("OK " + str(nb) + " entrees supprimees")

    # ────────────────────────────────────────
    #  EFFACER TOUT
    # ────────────────────────────────────────
    def _effacer_tout(self):
        self.enc_input.delete(0, "end")
        self._write(self.enc_output, "")
        self._write(self.enc_detail, "")
        self.dec_input.delete(0, "end")
        self._write(self.dec_output, "")
        self._write(self.dec_detail, "")
        self.ana_input.delete(0, "end")
        self._write(self.ana_output, "")
        self.cmp_input1.delete(0, "end")
        self.cmp_input2.delete(0, "end")
        self._write(self.cmp_output, "")
        self.stats_input.delete(0, "end")
        self._write(self.stats_output, "")
        self._status("Tout efface !")

    def _on_tab_change(self, event):
        idx  = self.notebook.index("current")
        noms = ["encoder", "decoder", "analyser",
                "comparer", "stats", "historique"]
        self._onglet_actif = noms[idx]
        if noms[idx] == "historique":
            self._refresh_historique()
            self._voir_favoris()

    # ────────────────────────────────────────
    #  FERMETURE
    # ────────────────────────────────────────
    def _fermer(self):
        try:
            self.db.fermer()
        except Exception:
            pass
        self.root.destroy()

    def run(self):
        self.root.mainloop()


# ════════════════════════════════════════════
#  POINT D'ENTREE
# ════════════════════════════════════════════
if __name__ == "__main__":
    app = UTF8GUI()
    app.run()