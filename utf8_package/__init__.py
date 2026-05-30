# utf8_package/__init__.py
from .encodeur  import encoder_char, encoder_texte
from .decodeur  import decoder_hex
from .analyseur import analyser_char, analyser_texte, comparer
from .utils     import valider_hex, octets_vers_hex, taille_utf8

__version__ = "1.0.0"
__auteur__  = "Votre Nom"
