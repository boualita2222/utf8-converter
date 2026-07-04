#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crée une icône .ico pour l'application UTF-8
"""

import tkinter as tk
from tkinter import PhotoImage
import os

def creer_icone():
    """Crée une icône simple en base64"""

    # Icône 32x32 en base64 — carré vert UTF-8
    icon_data = """
R0lGODlhIAAgAMQAAAAAABD/QRD/cRD/kTH/QTH/cTH/kVL/QVL/
cVL/kXP/QXP/cXP/kZT/QZT/cZT/kb3/Qb3/cb3/kb7/kb//kP//
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAABIALAAA
AAAIACAAAAT/kMlJq7046827/2AojmRpnmiqrmzrvnAsz3Rt
33iu73zv/8CgcEgsGo/IpHLJbDqf0Kh0Sq1ar9isdsvter
/gsHhMLpvP6LR6zW673/C4fE6v2+/4vH7P7/v/gIGCg4SF
hoeIiYqLjI2Oj5CRkpOUlZaXmJmam5ydnp+goaKjpKWmp6
ipqqusra6vsLGys7S1tre4ubq7vL2+v8DBwsPExcbHyMnKy8
zNzs/Q0dLT1NXW19jZ2tvc3d7f4OHi4+Tl5ufo6err7O3u7
/Dx8vP09fb3+Pn6+/z9/v8AAwocSLCgwYMIEypcyLChw4cQ
I0qcSLGixYsYM2rcyLGjx48gQ4ocSbKkyZMoU6pcybKly5c
wY8qcSbOmzZs4c+rcybOnz59AgwodSrSo0aNIkypdyrSp06d
Qo0qdSrWq1atYs2rdyrWr169gw4odS7as2bNo06pdy7at27d
w48qdS7eu3bt48+rdy7ev37+AAwseTLiw4cOIEytezLix48e
QI0ueTLmy5cuYM2vezLmz58+gQ4seTbq06dOoU6vmaAAAOw==
"""

    # Créer fenêtre temporaire
    root = tk.Tk()
    root.withdraw()

    try:
        img  = PhotoImage(data=icon_data)
        img.write(
            r"C:\PythonProjets\utf8_icon.png",
            format="png")
        print("✅ Icône créée !")
    except Exception as e:
        print(f"Note : {e}")
    finally:
        root.destroy()

if __name__ == "__main__":
    creer_icone()