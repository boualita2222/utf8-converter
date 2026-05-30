#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════╗
║         UTF-8 WEB API — Flask                       ║
║         Python 3.14.2                               ║
╚══════════════════════════════════════════════════════╝

Lancement : python utf8_api.py
Accès     : http://localhost:5000
"""

import sys
import os
sys.path.insert(0, r"C:\PythonProjets")

from flask import (Flask, request,jsonify, render_template_string,
 redirect, url_for)
from utf8_package.encodeur  import encoder_texte

from utf8_package.decodeur  import decoder_hex

from utf8_package.analyseur import (analyser_char,
                                    
                                     analyser_texte,
                                     
                                     comparer)
from utf8_db import UTF8Database
import unicodedata

# ════════════════════════════════════════════
#  APPLICATION FLASK
# ════════════════════════════════════════════
app = Flask(__name__)
db  = UTF8Database()

# ════════════════════════════════════════════
#  PAGE HTML PRINCIPALE
# ════════════════════════════════════════════
HTML_PAGE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width,
                   initial-scale=1.0">
    <title>UTF-8 Converter API</title>
    <style>
        * { box-sizing: border-box;
            margin: 0; padding: 0; }

        body {
            font-family: 'Courier New',
                          monospace;
            background: #0d0d0d;
            color: #e0e0e0;
            padding: 20px;
        }

        h1 {
            color: #00ff41;
            text-align: center;
            padding: 20px;
            border: 1px solid #1e3a1e;
            margin-bottom: 30px;
        }

        h2 { color: #ffb000;
             margin: 20px 0 10px; }

        .container {
            max-width: 900px;
            margin: 0 auto;
        }

        .card {
            background: #111;
            border: 1px solid #1e3a1e;
            border-radius: 6px;
            padding: 20px;
            margin-bottom: 20px;
        }

        input, textarea {
            width: 100%;
            background: #0a0a0a;
            border: 1px solid #1e3a1e;
            color: #00ff41;
            font-family: 'Courier New',
                          monospace;
            font-size: 14px;
            padding: 10px;
            border-radius: 4px;
            margin: 8px 0;
        }

        button {
            background: #0a0a0a;
            border: 1px solid #00ff41;
            color: #00ff41;
            font-family: 'Courier New',
                          monospace;
            font-size: 13px;
            padding: 8px 20px;
            border-radius: 4px;
            cursor: pointer;
            margin: 5px;
        }

        button:hover {
            background: #1a2a1a;
        }

        .btn-cyan {
            border-color: #00e5ff;
            color: #00e5ff;
        }

        .btn-yellow {
            border-color: #ffb000;
            color: #ffb000;
        }

        .btn-magenta {
            border-color: #ff79c6;
            color: #ff79c6;
        }

        .result {
            background: #080808;
            border: 1px solid #1a2a1a;
            border-radius: 4px;
            padding: 15px;
            margin-top: 15px;
            min-height: 60px;
            white-space: pre-wrap;
            font-size: 13px;
            line-height: 1.6;
        }

        .hex    { color: #ffb000; }
        .ok     { color: #00ff41; }
        .err    { color: #ff4444; }
        .info   { color: #00e5ff; }
        .label  { color: #ffb000;
                  font-size: 12px; }

        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }

        @media(max-width: 600px) {
            .grid { grid-template-columns: 1fr; }
        }

        .sep {
            border: none;
            border-top: 1px solid #1e3a1e;
            margin: 20px 0;
        }

        .badge {
            display: inline-block;
            background: #0a140a;
            border: 1px solid #1e3a1e;
            border-radius: 3px;
            padding: 2px 8px;
            font-size: 11px;
            color: #00ff41;
            margin: 3px;
        }

        .api-route {
            background: #080808;
            border-left: 3px solid #00ff41;
            padding: 8px 12px;
            margin: 5px 0;
            font-size: 12px;
        }

        .method-get  { color: #00ff41; }
        .method-post { color: #ffb000; }

        #historique-list {
            max-height: 300px;
            overflow-y: auto;
        }
    </style>
</head>
<body>
<div class="container">

    <h1>&#9608; UTF-8 CONVERTER API<br>
        <small style="font-size:14px;
               color:#555">
        Python 3.14.2 + Flask</small>
    </h1>

    <div class="grid">

        <!-- ENCODEUR -->
        <div class="card">
            <h2>[ 1 ] ENCODER</h2>
            <span class="label">
                Texte a encoder :</span>
            <input type="text"
                   id="enc-input"
                   placeholder="cafe 🌍 ete"
                   onkeydown="if(event.key==='Enter')
                              encoder()">
            <button onclick="encoder()">
                Encoder →</button>
            <button class="btn-cyan"
                    onclick="effacer('enc')">
                Effacer</button>
            <div class="result"
                 id="enc-result">
                Entrez du texte...
            </div>
        </div>

        <!-- DECODEUR -->
        <div class="card">
            <h2>[ 2 ] DECODER</h2>
            <span class="label">
                Sequence hex :</span>
            <input type="text"
                   id="dec-input"
                   placeholder="C3 A9 20 E2 82 AC"
                   onkeydown="if(event.key==='Enter')
                              decoder()">
            <button class="btn-cyan"
                    onclick="decoder()">
                Decoder →</button>
            <button class="btn-cyan"
                    onclick="effacer('dec')">
                Effacer</button>
            <div class="result"
                 id="dec-result">
                Entrez une sequence hex...
            </div>
        </div>

        <!-- ANALYSER -->
        <div class="card">
            <h2>[ 3 ] ANALYSER</h2>
            <span class="label">
                Caractere :</span>
            <input type="text"
                   id="ana-input"
                   placeholder="€ ou 🐍 ou A"
                   maxlength="2"
                   onkeyup="analyser()">
            <button class="btn-yellow"
                    onclick="analyser()">
                Analyser →</button>
            <div class="result"
                 id="ana-result">
                Entrez un caractere...
            </div>
        </div>

        <!-- COMPARER -->
        <div class="card">
            <h2>[ 4 ] COMPARER</h2>
            <span class="label">
                Texte 1 :</span>
            <input type="text"
                   id="cmp-input1"
                   placeholder="cafe">
            <span class="label">
                Texte 2 :</span>
            <input type="text"
                   id="cmp-input2"
                   placeholder="café">
            <button class="btn-magenta"
                    onclick="comparer_textes()">
                Comparer →</button>
            <button class="btn-cyan"
                    onclick="effacer('cmp')">
                Effacer</button>
            <div class="result"
                 id="cmp-result">
                Entrez deux textes...
            </div>
        </div>

    </div>

    <!-- STATS -->
    <div class="card">
        <h2>[ 5 ] STATISTIQUES</h2>
        <span class="label">
            Texte a analyser :</span>
        <input type="text"
               id="stats-input"
               placeholder="Bonjour 🌍 c'est l'ete !"
               onkeydown="if(event.key==='Enter')
                          stats()">
        <button class="btn-cyan"
                onclick="stats()">
            Analyser →</button>
        <div class="result"
             id="stats-result">
            Entrez du texte...
        </div>
    </div>

    <!-- HISTORIQUE -->
    <div class="card">
        <h2>[ 6 ] HISTORIQUE</h2>
        <button onclick="charger_hist()">
            Rafraichir</button>
        <button class="btn-yellow"
                onclick="charger_resume()">
            Resume DB</button>
        <div class="result"
             id="historique-list">
            Cliquez sur Rafraichir...
        </div>
    </div>

    <!-- ROUTES API -->
    <div class="card">
        <h2>[ 7 ] ROUTES API</h2>
        <p style="color:#555;
                  font-size:12px;
                  margin-bottom:10px">
            Utilisez ces routes avec
            curl ou Postman :</p>

        <div class="api-route">
            <span class="method-get">GET</span>
            /api/encoder?texte=café
        </div>
        <div class="api-route">
            <span class="method-get">GET</span>
            /api/decoder?hex=C3+A9
        </div>
        <div class="api-route">
            <span class="method-get">GET</span>
            /api/analyser?char=€
        </div>
        <div class="api-route">
            <span class="method-post">POST</span>
            /api/encoder {"texte": "café"}
        </div>
        <div class="api-route">
            <span class="method-post">POST</span>
            /api/decoder {"hex": "C3 A9"}
        </div>
        <div class="api-route">
            <span class="method-get">GET</span>
            /api/historique
        </div>
        <div class="api-route">
            <span class="method-get">GET</span>
            /api/resume
        </div>
    </div>

</div>

<script>
// ── ENCODER ──────────────────────────────
async function encoder() {
    const texte = document.getElementById(
        'enc-input').value.trim();
    if (!texte) return;
    const res = document.getElementById(
        'enc-result');
    res.innerHTML = 'Encodage...';
    try {
        const r = await fetch(
            '/api/encoder?texte=' +
            encodeURIComponent(texte));
        const d = await r.json();
        if (d.erreur) {
            res.innerHTML =
                '<span class="err">' +
                d.erreur + '</span>';
            return;
        }
        let html = '<span class="ok">' +
            'Texte   : ' + d.texte +
            '</span>\n';
        html += '<span class="hex">' +
            'Hex     : ' + d.hex +
            '</span>\n';
        html += '<span class="info">' +
            'Chars   : ' + d.nb_chars +
            '\nOctets  : ' + d.nb_octets +
            '</span>\n\n';
        d.details.forEach(det => {
            html += det.char + '  ' +
                'U+' + det.cp.toString(
                    16).toUpperCase()
                    .padStart(4,'0') +
                '  ' + det.hex + '\n';
        });
        res.innerHTML = html;
    } catch(e) {
        res.innerHTML =
            '<span class="err">' +
            'Erreur : ' + e + '</span>';
    }
}

// ── DECODER ──────────────────────────────
async function decoder() {
    const hex = document.getElementById(
        'dec-input').value.trim();
    if (!hex) return;
    const res = document.getElementById(
        'dec-result');
    try {
        const r = await fetch(
            '/api/decoder?hex=' +
            encodeURIComponent(hex));
        const d = await r.json();
        if (d.erreur) {
            res.innerHTML =
                '<span class="err">' +
                d.erreur + '</span>';
            return;
        }
        let html = '<span class="ok">' +
            'Texte : ' + d.texte +
            '</span>\n\n';
        d.details.forEach(det => {
            html += det.hex.padEnd(15) +
                ' ->  ' + det.char +
                '  U+' + det.cp.toString(
                    16).toUpperCase()
                    .padStart(4,'0') +
                '\n';
        });
        res.innerHTML = html;
    } catch(e) {
        res.innerHTML =
            '<span class="err">' +
            'Erreur : ' + e + '</span>';
    }
}

// ── ANALYSER ─────────────────────────────
async function analyser() {
    const c = document.getElementById(
        'ana-input').value.trim();
    if (!c) return;
    const res = document.getElementById(
        'ana-result');
    try {
        const r = await fetch(
            '/api/analyser?char=' +
            encodeURIComponent(c[0]));
        const d = await r.json();
        if (d.erreur) {
            res.innerHTML =
                '<span class="err">' +
                d.erreur + '</span>';
            return;
        }
        let html =
            '<span class="ok">' +
            'Caractere  : ' + d.char +
            '</span>\n' +
            '<span class="info">' +
            'Codepoint  : U+' + d.cp +
            '</span>\n' +
            '<span class="hex">' +
            'Hex UTF-8  : ' + d.hex +
            '</span>\n' +
            'Binaire    : ' + d.bin +
            '\nOctets     : ' + d.n +
            '\nDec. brut  : ' + d.raw_int +
            '\n<span class="info">' +
            'Nom        : ' + d.nom +
            '</span>';
        res.innerHTML = html;
    } catch(e) {
        res.innerHTML =
            '<span class="err">' +
            'Erreur : ' + e + '</span>';
    }
}

// ── COMPARER ─────────────────────────────
async function comparer_textes() {
    const t1 = document.getElementById(
        'cmp-input1').value.trim();
    const t2 = document.getElementById(
        'cmp-input2').value.trim();
    if (!t1 || !t2) return;
    const res = document.getElementById(
        'cmp-result');
    try {
        const r = await fetch(
            '/api/comparer?t1=' +
            encodeURIComponent(t1) +
            '&t2=' +
            encodeURIComponent(t2));
        const d = await r.json();
        if (d.erreur) {
            res.innerHTML =
                '<span class="err">' +
                d.erreur + '</span>';
            return;
        }
        let html =
            'Texte 1 : ' + d.texte1 +
            '  (' + d.oct1 + ' oct)\n' +
            'Texte 2 : ' + d.texte2 +
            '  (' + d.oct2 + ' oct)\n' +
            '─'.repeat(40) + '\n';
        if (d.identiques) {
            html +=
                '<span class="ok">' +
                'IDENTIQUES !</span>';
        } else {
            html +=
                '<span class="err">' +
                d.nb_diff +
                ' difference(s) :</span>\n';
            d.differences.forEach(diff => {
                html += 'Pos ' +
                    diff.pos + ' : ' +
                    (diff.c1 || '-') +
                    ' ' + diff.h1 +
                    '  !=  ' +
                    (diff.c2 || '-') +
                    ' ' + diff.h2 + '\n';
            });
        }
        res.innerHTML = html;
    } catch(e) {
        res.innerHTML =
            '<span class="err">' +
            'Erreur : ' + e + '</span>';
    }
}

// ── STATS ────────────────────────────────
async function stats() {
    const texte = document.getElementById(
        'stats-input').value.trim();
    if (!texte) return;
    const res = document.getElementById(
        'stats-result');
    try {
        const r = await fetch(
            '/api/stats?texte=' +
            encodeURIComponent(texte));
        const d = await r.json();
        if (d.erreur) {
            res.innerHTML =
                '<span class="err">' +
                d.erreur + '</span>';
            return;
        }
        let html =
            'Texte      : ' + d.texte +
            '\nCaracteres : ' + d.nb_chars +
            '\nOctets     : ' + d.nb_octets +
            '\nASCII%     : ' +
            d.pct_ascii.toFixed(1) +
            '%\n' + '-'.repeat(40) + '\n';
        const labels = {
            1: 'ASCII    (1 oct)',
            2: 'Latin    (2 oct)',
            3: 'Symboles (3 oct)',
            4: 'Emojis   (4 oct)',
        };
        [1,2,3,4].forEach(n => {
            if (d.types[n] &&
                d.types[n].length > 0) {
                const nb  = d.types[n].length;
                const pct = (nb * n /
                    d.nb_octets * 100)
                    .toFixed(1);
                const bar = '='.repeat(
                    Math.floor(pct/4));
                html += '\n' + labels[n] +
                    '\n  Chars : ' + nb +
                    '  (' + pct + '%)\n' +
                    '  ' + bar + '\n';
            }
        });
        res.innerHTML = html;
    } catch(e) {
        res.innerHTML =
            '<span class="err">' +
            'Erreur : ' + e + '</span>';
    }
}

// ── HISTORIQUE ───────────────────────────
async function charger_hist() {
    const res = document.getElementById(
        'historique-list');
    try {
        const r = await fetch(
            '/api/historique');
        const d = await r.json();
        if (!d.historique ||
            d.historique.length === 0) {
            res.innerHTML =
                'Historique vide.';
            return;
        }
        let html = 'ID    OP        ' +
            'ENTREE               ' +
            'OCT   DATE\n' +
            '-'.repeat(65) + '\n';
        d.historique.forEach(h => {
            html += '#' +
                String(h.id).padEnd(4) +
                h.operation.padEnd(10) +
                h.entree.substring(0,18)
                    .padEnd(21) +
                String(h.nb_octets)
                    .padEnd(6) +
                h.date + '\n';
        });
        res.innerHTML = html;
    } catch(e) {
        res.innerHTML =
            '<span class="err">' +
            'Erreur : ' + e + '</span>';
    }
}

// ── RESUME ───────────────────────────────
async function charger_resume() {
    const res = document.getElementById(
        'historique-list');
    try {
        const r = await fetch(
            '/api/resume');
        const d = await r.json();
        let html =
            'Resume base de donnees :\n\n' +
            'Total operations : ' +
            d.total_ops + '\n' +
            'Total octets     : ' +
            d.total_octets + '\n' +
            'Favoris          : ' +
            d.nb_favoris + '\n\n' +
            'Par type :\n';
        for (const [op, nb]
             of Object.entries(
                 d.par_type)) {
            html += '  ' +
                op.padEnd(12) +
                nb + '\n';
        }
        if (d.plus_long) {
            html += '\nPlus long :\n  ' +
                d.plus_long.entree +
                ' (' +
                d.plus_long.nb_octets +
                ' oct)\n';
        }
        res.innerHTML = html;
    } catch(e) {
        res.innerHTML =
            '<span class="err">' +
            'Erreur : ' + e + '</span>';
    }
}

// ── EFFACER ──────────────────────────────
function effacer(prefix) {
    const ids = {
        'enc': ['enc-input',
                'enc-result'],
        'dec': ['dec-input',
                'dec-result'],
        'ana': ['ana-input',
                'ana-result'],
        'cmp': ['cmp-input1',
                'cmp-input2',
                'cmp-result'],
    };
    (ids[prefix] || []).forEach(id => {
        const el = document.getElementById(id);
        if (el.tagName === 'INPUT')
            el.value = '';
        else
            el.innerHTML = '';
    });
}
</script>
</body>
</html>
"""


# ════════════════════════════════════════════
#  ROUTES — PAGES
# ════════════════════════════════════════════
@app.route("/")
def accueil():
    """Page principale"""
    return render_template_string(HTML_PAGE)


# ════════════════════════════════════════════
#  ROUTES — API ENCODEUR
# ════════════════════════════════════════════
@app.route("/api/encoder",
           methods=["GET", "POST"])
def api_encoder():
    """
    GET  /api/encoder?texte=café
    POST /api/encoder {"texte": "café"}
    """
    try:
        if request.method == "POST":
            data  = request.get_json()
            texte = data.get("texte", "")
        else:
            texte = request.args.get(
                "texte", "")

        if not texte:
            return jsonify(
                {"erreur": "Texte vide !"}), 400

        res = encoder_texte(texte)

        # Sauvegarde DB
        db.ajouter_historique(
            "ENCODE", texte,
            res["hex"],
            res["nb_chars"],
            res["nb_octets"])

        # Préparer les détails
        details = []
        for d in res["details"]:
            details.append({
                "char": d["char"],
                "cp":   d["cp"],
                "hex":  d["hex"],
                "n":    d["n"],
            })

        return jsonify({
            "texte":     texte,
            "hex":       res["hex"],
            "nb_chars":  res["nb_chars"],
            "nb_octets": res["nb_octets"],
            "details":   details,
        })

    except Exception as e:
        return jsonify(
            {"erreur": str(e)}), 500


# ════════════════════════════════════════════
#  ROUTES — API DECODEUR
# ════════════════════════════════════════════
@app.route("/api/decoder",
           methods=["GET", "POST"])
def api_decoder():
    """
    GET  /api/decoder?hex=C3+A9
    POST /api/decoder {"hex": "C3 A9"}
    """
    try:
        if request.method == "POST":
            data    = request.get_json()
            hex_str = data.get("hex", "")
        else:
            hex_str = request.args.get(
                "hex", "")

        if not hex_str:
            return jsonify(
                {"erreur": "Hex vide !"}), 400

        res = decoder_hex(hex_str)

        # Sauvegarde DB
        db.ajouter_historique(
            "DECODE", hex_str,
            res["texte"],
            len(res["texte"]),
            len(res["details"]))

        details = []
        for d in res["details"]:
            details.append({
                "hex":  d["hex"],
                "cp":   d["cp"],
                "char": d["char"],
                "n":    d["n"],
            })

        return jsonify({
            "texte":   res["texte"],
            "details": details,
        })

    except Exception as e:
        return jsonify(
            {"erreur": str(e)}), 500


# ════════════════════════════════════════════
#  ROUTES — API ANALYSER
# ════════════════════════════════════════════
@app.route("/api/analyser",
           methods=["GET", "POST"])
def api_analyser():
    """
    GET /api/analyser?char=€
    """
    try:
        if request.method == "POST":
            data = request.get_json()
            c    = data.get("char", "")
        else:
            c = request.args.get(
                "char", "")

        if not c:
            return jsonify(
                {"erreur":
                 "Caractere vide !"}), 400

        res = analyser_char(c[0])

        # Sauvegarde DB
        db.ajouter_historique(
            "ANALYSE", c[0],
            res["hex"], 1, res["n"])

        return jsonify({
            "char":    res["char"],
            "cp":      res["cp"],
            "cp_hex":  format(
                res["cp"], '04X'),
            "hex":     res["hex"],
            "bin":     res["bin"],
            "n":       res["n"],
            "raw_int": res["raw_int"],
            "nom":     res["nom"],
            "cat":     res["cat"],
        })

    except Exception as e:
        return jsonify(
            {"erreur": str(e)}), 500


# ════════════════════════════════════════════
#  ROUTES — API COMPARER
# ════════════════════════════════════════════
@app.route("/api/comparer",
           methods=["GET", "POST"])
def api_comparer():
    """
    GET /api/comparer?t1=café&t2=cafe
    """
    try:
        if request.method == "POST":
            data = request.get_json()
            t1   = data.get("t1", "")
            t2   = data.get("t2", "")
        else:
            t1 = request.args.get("t1", "")
            t2 = request.args.get("t2", "")

        if not t1 or not t2:
            return jsonify(
                {"erreur":
                 "Deux textes requis !"}), 400

        res = comparer(t1, t2)

        # Sauvegarde DB
        db.ajouter_historique(
            "COMPARE",
            t1 + " vs " + t2,
            str(len(res["differences"])) +
            " diff.",
            len(t1) + len(t2),
            res["oct1"] + res["oct2"])

        diffs = []
        for d in res["differences"]:
            diffs.append({
                "pos": d["pos"],
                "c1":  d["c1"],
                "c2":  d["c2"],
                "h1":  d["h1"],
                "h2":  d["h2"],
            })

        return jsonify({
            "texte1":      t1,
            "texte2":      t2,
            "oct1":        res["oct1"],
            "oct2":        res["oct2"],
            "identiques":  res["identiques"],
            "nb_diff":     len(diffs),
            "differences": diffs,
        })

    except Exception as e:
        return jsonify(
            {"erreur": str(e)}), 500


# ════════════════════════════════════════════
#  ROUTES — API STATS
# ════════════════════════════════════════════
@app.route("/api/stats",
           methods=["GET", "POST"])
def api_stats():
    """
    GET /api/stats?texte=Bonjour
    """
    try:
        if request.method == "POST":
            data  = request.get_json()
            texte = data.get("texte", "")
        else:
            texte = request.args.get(
                "texte", "")

        if not texte:
            return jsonify(
                {"erreur":
                 "Texte vide !"}), 400

        res = analyser_texte(texte)

        # Sauvegarde DB
        db.ajouter_stats(texte, res)

        types_out = {}
        for n in range(1, 5):
            types_out[n] = res["types"][n]

        return jsonify({
            "texte":     texte,
            "nb_chars":  res["nb_chars"],
            "nb_octets": res["nb_octets"],
            "pct_ascii": res["pct_ascii"],
            "types":     types_out,
        })

    except Exception as e:
        return jsonify(
            {"erreur": str(e)}), 500


# ════════════════════════════════════════════
#  ROUTES — API HISTORIQUE
# ════════════════════════════════════════════
@app.route("/api/historique")
def api_historique():
    """GET /api/historique"""
    try:
        rows = db.get_historique(20)
        hist = []
        for row in rows:
            hist.append({
                "id":        row["id"],
                "operation": row["operation"],
                "entree":    str(
                    row["entree"]),
                "sortie":    str(
                    row["sortie"]),
                "nb_octets": row["nb_octets"],
                "date":      row["date"],
            })
        return jsonify(
            {"historique": hist})
    except Exception as e:
        return jsonify(
            {"erreur": str(e)}), 500


# ════════════════════════════════════════════
#  ROUTES — API RESUME
# ════════════════════════════════════════════
@app.route("/api/resume")
def api_resume():
    """GET /api/resume"""
    try:
        stats = db.get_resumé()
        return jsonify({
            "total_ops":    stats["total_ops"],
            "total_octets": stats["total_octets"],
            "nb_favoris":   stats["nb_favoris"],
            "par_type":     stats["par_type"],
            "plus_long":    stats["plus_long"],
        })
    except Exception as e:
        return jsonify(
            {"erreur": str(e)}), 500


# ════════════════════════════════════════════
#  LANCEMENT
# ════════════════════════════════════════════
if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════╗
║         UTF-8 WEB API — Flask                       ║
║         http://localhost:5000                       ║
╚══════════════════════════════════════════════════════╝
""")
    print("  Ouvrez votre navigateur :")
    print("  http://localhost:5000\n")
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True)