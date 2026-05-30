from rest_framework import serializers
from .models import Historique, Favori


class HistoriqueSerializer(serializers.ModelSerializer):
    """Sérialiseur pour le modèle Historique"""
    username = serializers.SerializerMethodField()

    class Meta:
        model  = Historique
        fields = ['id', 'operation', 'entree',
                  'sortie', 'nb_chars',
                  'nb_octets', 'date',
                  'username']
        read_only_fields = ['id', 'date']

    def get_username(self, obj):
        if obj.user:
            return obj.user.username
        return 'Anonyme'


class FavoriSerializer(serializers.ModelSerializer):
    """Sérialiseur pour le modèle Favori"""

    class Meta:
        model  = Favori
        fields = ['id', 'nom', 'texte',
                  'hex_utf8', 'date']
        read_only_fields = ['id', 'date']


class EncoderSerializer(serializers.Serializer):
    """Sérialiseur pour l'encodage"""
    texte = serializers.CharField(
        max_length=1000,
        help_text="Texte a encoder en UTF-8")


class DecoderSerializer(serializers.Serializer):
    """Sérialiseur pour le décodage"""
    hex = serializers.CharField(
        max_length=3000,
        help_text="Sequence hex UTF-8 a decoder")


class AnalyserSerializer(serializers.Serializer):
    """Sérialiseur pour l'analyse"""
    char = serializers.CharField(
        max_length=2,
        help_text="Caractere a analyser")


class ComparerSerializer(serializers.Serializer):
    """Sérialiseur pour la comparaison"""
    texte1 = serializers.CharField(
        max_length=500,
        help_text="Premier texte")
    texte2 = serializers.CharField(
        max_length=500,
        help_text="Deuxieme texte")


class StatsSerializer(serializers.Serializer):
    """Sérialiseur pour les statistiques"""
    texte = serializers.CharField(
        max_length=1000,
        help_text="Texte a analyser")