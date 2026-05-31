#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════╗
║         UTF-8 CONVERTER — Interface Graphique       ║
║         Python 3.14.2 + Tkinter                    ║
╚══════════════════════════════════════════════════════╝
"""

import tkinter as tk
from utf8_db import UTF8Database
from tkinter import ttk, messagebox, scrolledtext
import unicodedata
import sys
sys.path.insert(0, r"C:\PythonProjets")

from utf8_package.encodeur  import encoder_texte
from utf8_package.decodeur  import decoder_hex
from utf8_package.analyseur import (analyser_char,
                                     analyser_texte,
                                     comparer)

# ════════════════════════════════════════════
#  COULEURS ET STYLES
# ════════════════════════════════════════════
COULEURS = {
    "bg":        "#0d0d0d",
    "panel":     "#111111",
    "border":    "#1e3a1e",
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
    
    def _fermer(self):
       """Ferme proprement l'application"""
    try:
        self.db.fermer()
    except Exception:
        pass
    self.root.destroy()
        
    """Interface graphique du convertisseur UTF-8"""

    def __init__(self):
        # Fenêtre principale
        self.root = tk.Tk()
        self.root.title(
            "UTF-8 Converter — Python 3.14.2")
        self.root.geometry("900x700")
        self.root.configure(
            bg=COULEURS["bg"])
        self.root.resizable(True, True)
        self.root.protocol(
           "WM_DELETE_WINDOW",
        self._fermer)
        # Icône de la fenêtre
        self._set_icone()

    def _set_icone(self):
        """Configure l'icône de la fenêtre"""
        try:
            # Créer une icône depuis du texte
            self.root.iconbitmap(default="")
            icon = tk.PhotoImage(
                width=32, height=32)
            # Dessiner un carré vert
            for x in range(32):
                for y in range(32):
                    if (x < 2 or x > 29 or
                        y < 2 or y > 29):
                        icon.put(
                            "#00ff41",
                            (x, y))
                    else:
                        icon.put(
                            "#0d0d0d",
                            (x, y))
            # Lettres UTF au centre
            for x, y in [
                (8,8),(9,8),(10,8),
                (8,16),(9,16),(10,16),
                (8,24),(9,24),(10,24),
                (14,8),(14,12),(14,16),
                (14,20),(14,24),
                (18,8),(19,8),(20,8),
                (21,12),(20,16),(19,20),
                (18,24),(19,24),(20,24),
            ]:
                try:
                    icon.put("#00ff41", (x,y))
                except Exception:
                    pass
            self.root.iconphoto(True, icon)
        except Exception:
            pass
        self.root.title(
            "UTF-8 Converter — Python 3.14.2")
        self.root.geometry("900x700")
        self.root.configure(
            bg=COULEURS["bg"])
        self.root.resizable(True, True)

        # Variables
        self.var_input   = tk.StringVar()
        self.var_status  = tk.StringVar()
        self.var_status.set(
            "Prêt — Entrez du texte ou du hex")

        # Construction interface
        self._build_header()
        self._build_tabs()
        self._build_statusbar()

        # Raccourcis clavier
        self.root.bind("<Return>",
            lambda e: self._action_courante())
        self.root.bind("<Control-l>",
            lambda e: self._effacer_tout())

    # ────────────────────────────────────────
    #  CONSTRUCTION — HEADER
    # ────────────────────────────────────────
    def _build_header(self):
        """Barre de titre"""
        header = tk.Frame(
            self.root,
            bg=COULEURS["panel"],
            pady=8)
        header.pack(fill="x")

        tk.Label(
            header,
            text="╔══ UTF-8 CONVERTER ══╗",
            font=FONTS["title"],
            fg=COULEURS["green"],
            bg=COULEURS["panel"],
        ).pack()

        tk.Label(
            header,
            text="Python 3.14.2 + Tkinter",
            font=FONTS["mono_sm"],
            fg=COULEURS["dim"],
            bg=COULEURS["panel"],
        ).pack()

    # ────────────────────────────────────────
    #  CONSTRUCTION — ONGLETS
    # ────────────────────────────────────────
    def _build_tabs(self):
        self._build_tab_historique()
        """Onglets principaux"""
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "TNotebook",
            background=COULEURS["bg"],
            borderwidth=0)
        style.configure(
            "TNotebook.Tab",
            background=COULEURS["panel"],
            foreground=COULEURS["dim"],
            font=FONTS["mono"],
            padding=[12, 6])
        style.map(
            "TNotebook.Tab",
            background=[("selected",
                          COULEURS["bg"])],
            foreground=[("selected",
                          COULEURS["green"])])

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(
            fill="both", expand=True,
            padx=5, pady=5)

        # Créer les onglets
        self._build_tab_encoder()
        self._build_tab_decoder()
        self._build_tab_analyser()
        self._build_tab_comparer()
        self._build_tab_stats()

        # Mémoriser l'onglet actif
        self.notebook.bind(
            "<<NotebookTabChanged>>",
            self._on_tab_change)
        self._onglet_actif = "encoder"

    # ────────────────────────────────────────
    #  ONGLET 1 — ENCODEUR
    # ────────────────────────────────────────
    def _build_tab_encoder(self):
        frame = tk.Frame(
            self.notebook,
            bg=COULEURS["bg"])
        self.notebook.add(
            frame, text=" [1] ENCODER ")

        # Entrée
        self._label(frame,
            "Texte à encoder :")
        self.enc_input = self._entry(frame)
        self.enc_input.bind("<Return>",
            lambda e: self._encoder())

        # Boutons
        btn_frame = tk.Frame(
            frame, bg=COULEURS["bg"])
        btn_frame.pack(fill="x", padx=10)
        self._btn(btn_frame,
            "Encoder →", self._encoder,
            COULEURS["green"])
        self._btn(btn_frame,
            "Effacer", self._effacer_enc,
            COULEURS["red"])

        # Résultat
        self._label(frame, "Résultat :")
        self.enc_output = self._text(frame, 8)

        # Détails
        self._label(frame,
            "Détails caractère par caractère :")
        self.enc_detail = self._text(frame, 8)

    # ────────────────────────────────────────
    #  ONGLET 2 — DÉCODEUR
    # ────────────────────────────────────────
    def _build_tab_decoder(self):
        frame = tk.Frame(
            self.notebook,
            bg=COULEURS["bg"])
        self.notebook.add(
            frame, text=" [2] DECODER ")

        self._label(frame,
            "Séquence hex UTF-8 :")
        self._label(frame,
            "  Exemple : C3 A9 20 E2 82 AC",
            COULEURS["dim"])
        self.dec_input = self._entry(frame)
        self.dec_input.bind("<Return>",
            lambda e: self._decoder())

        btn_frame = tk.Frame(
            frame, bg=COULEURS["bg"])
        btn_frame.pack(fill="x", padx=10)
        self._btn(btn_frame,
            "Décoder →", self._decoder,
            COULEURS["cyan"])
        self._btn(btn_frame,
            "Effacer", self._effacer_dec,
            COULEURS["red"])

        self._label(frame, "Texte décodé :")
        self.dec_output = self._text(frame, 4)

        self._label(frame, "Détails :")
        self.dec_detail = self._text(frame, 10)

    # ────────────────────────────────────────
    #  ONGLET 3 — ANALYSER
    # ────────────────────────────────────────
    def _build_tab_analyser(self):
        frame = tk.Frame(
            self.notebook,
            bg=COULEURS["bg"])
        self.notebook.add(
            frame, text=" [3] ANALYSER ")

        self._label(frame,
            "Entrez un caractère :")
        self.ana_input = self._entry(frame)
        self.ana_input.bind("<Return>",
            lambda e: self._analyser())
        self.ana_input.bind("<KeyRelease>",
            lambda e: self._analyser_live())

        btn_frame = tk.Frame(
            frame, bg=COULEURS["bg"])
        btn_frame.pack(fill="x", padx=10)
        self._btn(btn_frame,
            "Analyser →", self._analyser,
            COULEURS["yellow"])

        self._label(frame, "Analyse complète :")
        self.ana_output = self._text(
            frame, 20)

    # ────────────────────────────────────────
    #  ONGLET 4 — COMPARER
    # ────────────────────────────────────────
    def _build_tab_comparer(self):
        frame = tk.Frame(
            self.notebook,
            bg=COULEURS["bg"])
        self.notebook.add(
            frame, text=" [4] COMPARER ")

        self._label(frame, "Texte 1 :")
        self.cmp_input1 = self._entry(frame)

        self._label(frame, "Texte 2 :")
        self.cmp_input2 = self._entry(frame)

        btn_frame = tk.Frame(
            frame, bg=COULEURS["bg"])
        btn_frame.pack(fill="x", padx=10)
        self._btn(btn_frame,
            "Comparer →", self._comparer,
            COULEURS["magenta"])
        self._btn(btn_frame,
            "Effacer", self._effacer_cmp,
            COULEURS["red"])

        self._label(frame, "Résultat :")
        self.cmp_output = self._text(
            frame, 18)

    # ────────────────────────────────────────
    #  ONGLET 5 — STATISTIQUES
    # ────────────────────────────────────────
    def _build_tab_stats(self):
        frame = tk.Frame(
            self.notebook,
            bg=COULEURS["bg"])
        self.notebook.add(
            frame, text=" [5] STATS ")

        self._label(frame,
            "Texte à analyser :")
        self.stats_input = self._entry(frame)
        self.stats_input.bind("<Return>",
            lambda e: self._stats())

        btn_frame = tk.Frame(
            frame, bg=COULEURS["bg"])
        btn_frame.pack(fill="x", padx=10)
        self._btn(btn_frame,
            "Analyser →", self._stats,
            COULEURS["cyan"])

        self._label(frame, "Statistiques :")
        self.stats_output = self._text(
            frame, 20)

    # ────────────────────────────────────────
    #  BARRE DE STATUT
    # ────────────────────────────────────────
    def _build_statusbar(self):
        # Connexion base de données
        self.db = UTF8Database()
        self._status(
           "✅ Base de données connectée !")
        statusbar = tk.Frame(
            self.root,
            bg=COULEURS["panel"],
            pady=4)
        statusbar.pack(fill="x", side="bottom")

        tk.Label(
            statusbar,
            textvariable=self.var_status,
            font=FONTS["mono_sm"],
            fg=COULEURS["dim"],
            bg=COULEURS["panel"],
            anchor="w",
            padx=10,
        ).pack(fill="x")

    # ────────────────────────────────────────
    #  WIDGETS HELPERS
    # ────────────────────────────────────────
    def _label(self, parent, text,
               color=None):
        tk.Label(
            parent,
            text=text,
            font=FONTS["mono_sm"],
            fg=color or COULEURS["yellow"],
            bg=COULEURS["bg"],
            anchor="w",
            padx=10,
        ).pack(fill="x", pady=(6,0))

    def _entry(self, parent):
        e = tk.Entry(
            parent,
            font=FONTS["mono_lg"],
            fg=COULEURS["green"],
            bg=COULEURS["btn_bg"],
            insertbackground=COULEURS["green"],
            relief="flat",
            bd=5)
        e.pack(fill="x", padx=10, pady=4)
        return e

    def _text(self, parent, height=6):
        t = scrolledtext.ScrolledText(
            parent,
            font=FONTS["mono_sm"],
            fg=COULEURS["white"],
            bg=COULEURS["btn_bg"],
            insertbackground=COULEURS["green"],
            relief="flat",
            bd=5,
            height=height,
            state="disabled")
        t.pack(fill="both", expand=True,
               padx=10, pady=4)
        return t

    def _btn(self, parent, text,
             command, color):
        b = tk.Button(
            parent,
            text=text,
            font=FONTS["mono"],
            fg=color,
            bg=COULEURS["btn_bg"],
            activeforeground=color,
            activebackground=
                COULEURS["btn_hover"],
            relief="flat",
            bd=1,
            padx=12, pady=4,
            cursor="hand2",
            command=command)
        b.pack(side="left",
               padx=5, pady=6)
        return b

    def _write(self, widget, text,
               clear=True):
        """Écrit dans un widget Text"""
        widget.configure(state="normal")
        if clear:
            widget.delete("1.0", "end")
        widget.insert("end", text)
        widget.configure(state="disabled")

    def _status(self, msg,
                color=None):
        """Met à jour la barre de statut"""
        self.var_status.set(msg)

    # ────────────────────────────────────────
    #  ACTIONS
    # ────────────────────────────────────────
    def _encoder(self):
        texte = self.enc_input.get().strip()
        if not texte:
            messagebox.showwarning(
                "Attention",
                "Entrez du texte !")
            return
        try:
            res = encoder_texte(texte)

            # Résultat principal
            out  = f"Texte    : {res['texte']}\n"
            out += f"Hex      : {res['hex']}\n"
            out += f"Chars    : {res['nb_chars']}\n"
            out += f"Octets   : {res['nb_octets']}\n"
            self._write(self.enc_output, out)

            # Détails
            det = ""
            for d in res["details"]:
                det += (f"  {d['char']}  "
                        f"U+{d['cp']:04X}  "
                        f"{d['hex']:<12}  "
                        f"{d['n']} oct\n")
            self._write(self.enc_detail, det)

            self._status()
            # Sauvegarde automatique
            self.db.ajouter_historique(
               "ENCODE",
                texte,
                res["hex"],
                res["nb_chars"],
                res["nb_octets"])
            self._refresh_historique()
            print(f"✅ Encodé : ")
            print(f"{res['nb_chars']} chars ")
            print(f"→ {res['nb_octets']} octets")

        except Exception as e:
            messagebox.showerror(
                "Erreur", str(e))

    def _effacer_enc(self):
        self.enc_input.delete(0, "end")
        self._write(self.enc_output, "")
        self._write(self.enc_detail, "")
        self._status("Effacé")

    def _decoder(self):
        hex_str = self.dec_input.get().strip()
        if not hex_str:
            messagebox.showwarning(
                "Attention",
                "Entrez une séquence hex !")
            return
        try:
            res = decoder_hex(hex_str)

            self._write(
                self.dec_output,
                f"Texte décodé : {res['texte']}\n")

            det = ""
            for d in res["details"]:
                det += (f"  {d['hex']:<15}"
                        f"→  {d['char']}  "
                        f"U+{d['cp']:04X}  "
                        f"{d['n']} oct\n")
            self._write(self.dec_detail, det)

            self._status(
                f"✅ Décodé : "
                f"{len(res['details'])} "
                f"caractères")

        except Exception as e:
            messagebox.showerror(
                "Erreur", str(e))

    def _effacer_dec(self):
        self.dec_input.delete(0, "end")
        self._write(self.dec_output, "")
        self._write(self.dec_detail, "")
        self._status("Effacé")

    def _analyser(self):
        c = self.ana_input.get().strip()
        if not c:
            return
        try:
            res = analyser_char(c[0])
            out  = f"  Caractère  : {res['char']}\n"
            out += f"  Codepoint  : U+{res['cp']:04X}\n"
            out += f"  Décimal    : {res['cp']}\n"
            out += f"  Hex UTF-8  : {res['hex']}\n"
            out += f"  Binaire    : {res['bin']}\n"
            out += f"  Octets     : {res['n']}\n"
            out += f"  Décimal brut: {res['raw_int']}\n"
            out += f"  Nom Unicode : {res['nom']}\n"
            out += f"  Catégorie  : {res['cat']}\n"
            out += "\n" + "─"*40 + "\n"
            out += "  Schéma UTF-8 :\n"
            out += self._schema_utf8(
                res['cp'], res['n'])
            self._write(
                self.ana_output, out)
            self._status(
# Sauvegarde automatique
self.db.ajouter_historique(
    "ANALYSE",
    c[0],
    res["hex"],
    1,
    res["n"])
self._refresh_historique()
               # Sauvegarde automatique
self.db.ajouter_historique(
    "DECODE",
    hex_str,
    res["texte"],
    len(res["texte"]),
    len(res["details"]))
self._refresh_historique()
                f"✅ {res['char']} = "
                f"U+{res['cp']:04X} = "
                f"{res['hex']}")
        except Exception as e:
            messagebox.showerror(
                "Erreur", str(e))
    def _analyser_live(self):
        """Analyse en temps réel"""
        c = self.ana_input.get().strip()
        if c:
            self._analyser()

    def _schema_utf8(self, cp, n):
        """Génère le schéma UTF-8"""
        templates = {
            1: ["0xxxxxxx"],
            2: ["110xxxxx", "10xxxxxx"],
            3: ["1110xxxx","10xxxxxx","10xxxxxx"],
            4: ["11110xxx","10xxxxxx", "10xxxxxx","10xxxxxx"],
        }
        payload = [7,11,16,21][n-1]
        bits    = f"{cp:0{payload}b}"
        result  = ""
        idx     = 0
        raw     = chr(cp).encode("utf-8")
        for i, tmpl in enumerate(templates[n]):
            filled = ""
            for ch in tmpl:
                if ch == "x":
                    filled += bits[idx]
                    idx    += 1
                else:
                    filled += ch
            bv = raw[i]
            result += (f"    Octet {i+1} : "
                      f"{filled}   "
                      f"({bv:02X}h = {bv})\n")
        return result

    def _comparer(self):
        t1 = self.cmp_input1.get().strip()
        t2 = self.cmp_input2.get().strip()
        if not t1 or not t2:
            messagebox.showwarning(
                "Attention",
                "Entrez les deux textes !")
            return
        try:
            res = comparer(t1, t2)
            out  = f"  Texte 1 : {t1}\n"
            out += f"  Texte 2 : {t2}\n"
            out += f"  Octets 1 : {res['oct1']}\n"
            out += f"  Octets 2 : {res['oct2']}\n"
            out += "─"*45 + "\n"
            if res["identiques"]:
                out += "  ✅ IDENTIQUES !\n"
            else:
                nb = len(res["differences"])
                out += f"  {nb} différence(s) :\n\n"
                for d in res["differences"]:
                    c1 = d["c1"] or "—"
                    c2 = d["c2"] or "—"
                    out += (f"  Pos {d['pos']} : "
                           f"'{c1}' {d['h1']}"
                           f"  ≠  "
                           f"'{c2}' {d['h2']}\n")
            self._write(self.cmp_output, out)
            status = ("Identiques ✅"
                      if res["identiques"]
                      else f"{len(res['differences'])}"
                           f" différence(s)")
            self._status(status)
# Sauvegarde automatique
        self.db.ajouter_historique(
            "COMPARE",
            t1 + " vs " + t2,
            str(len(res["differences"])) +
            " diff.",
            len(t1) + len(t2),
            res["oct1"] + res["oct2"])
        self._refresh_historique()
        except Exception as e:
        messagebox.showerror(
                "Erreur", str(e))

    def _effacer_cmp(self):
        self.cmp_input1.delete(0, "end")
        self.cmp_input2.delete(0, "end")
        self._write(self.cmp_output, "")
        self._status("Effacé")

    def _stats(self):
        texte = self.stats_input.get().strip()
        if not texte:
            messagebox.showwarning(
                "Attention",
                "Entrez du texte !")
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
            out += "-" * 45 + "\n"

            for n in range(1, 5):
                chars = res["types"][n]
                if not chars:
                    continue
                nb  = len(chars)
                pct = nb * n / res['nb_octets'] * 100
                bar = "=" * int(pct / 4)

                uniques = ""
                for c in dict.fromkeys(chars):
                    try:
                        c.encode('cp1252')
                        uniques += c
                    except Exception:
                        uniques += "[U+" + format(ord(c), '04X') + "]"
                    if len(uniques) > 30:
                        break

                out += "\n  " + labels[n] + "\n"
                out += "    Chars  : " + str(nb) + "  (" + str(round(pct, 1)) + "%)\n"
                out += "    " + bar + "\n"
                out += "    Uniques: " + uniques + "\n"

            self._write(self.stats_output, out)
            self._status(
            # Sauvegarde automatique
            self.db.ajouter_stats(texte, res)
            self._refresh_historique()
                "OK " + str(res['nb_chars']) +
                " chars -> " +
                str(res['nb_octets']) + " octets")

        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def _action_courante(self):
        """Entrée → action selon onglet actif"""
        actions = {
            "encoder":  self._encoder,
            "decoder":  self._decoder,
            "analyser": self._analyser,
            "comparer": self._comparer,
            "stats":    self._stats,
        }
        fn = actions.get(self._onglet_actif)
        if fn: fn()

    def _effacer_tout(self):
     """Ctrl+L → efface TOUS les onglets"""
    # Onglet 1
     self.enc_input.delete(0, "end")
     self._write(self.enc_output, "")
     self._write(self.enc_detail, "")
    # Onglet 2
     self.dec_input.delete(0, "end")
     self._write(self.dec_output, "")
     self._write(self.dec_detail, "")
    # Onglet 3
     self.ana_input.delete(0, "end")
     self._write(self.ana_output, "")
    # Onglet 4
     self.cmp_input1.delete(0, "end")
     self.cmp_input2.delete(0, "end")
     self._write(self.cmp_output, "")
    # Onglet 5
     self.stats_input.delete(0, "end")
     self._write(self.stats_output, "")
    # Statut
     self._status("✅ Tout effacé !")
    def _on_tab_change(self, event):
        """Mémorise l'onglet actif"""
        idx = self.notebook.index("current")
        noms = ["encoder","decoder",
                "analyser","comparer","stats"]
        self._onglet_actif = noms[idx]

    # ────────────────────────────────────────
    #  LANCEMENT
    # ────────────────────────────────────────
    def run(self):
        """Lance l'interface graphique"""
        self.root.mainloop()


# ════════════════════════════════════════════
#  POINT D'ENTRÉE
# ════════════════════════════════════════════
if __name__ == "__main__":
    app = UTF8GUI()
    app.run()