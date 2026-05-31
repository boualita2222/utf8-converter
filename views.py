from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated)
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiExample,
    OpenApiResponse)
from drf_spectacular.types import OpenApiTypes
import sys
import os

BASE = os.path.dirname(os.path.dirname(
       os.path.dirname(
       os.path.abspath(__file__))))
sys.path.insert(0, BASE)

from utf8_package.encodeur  import encoder_texte
from utf8_package.decodeur  import decoder_hex
from utf8_package.analyseur import (analyser_char,
                                     analyser_texte,
                                     comparer)
from .models      import Historique, Favori
from .serializers import (HistoriqueSerializer,
                           FavoriSerializer,
                           EncoderSerializer,
                           DecoderSerializer,
                           AnalyserSerializer,
                           ComparerSerializer,
                           StatsSerializer)


def sauvegarder(request, op, entree,
                sortie, nb_chars, nb_octets):
    Historique.objects.create(
        user      = request.user
                    if request.user.is_authenticated
                    else None,
        operation = op,
        entree    = str(entree)[:200],
        sortie    = str(sortie)[:200],
        nb_chars  = nb_chars,
        nb_octets = nb_octets)


# ════════════════════════════════════════════
#  ENCODEUR
# ════════════════════════════════════════════
@extend_schema_view(
    get=extend_schema(
        tags=['encoder'],
        summary='Encoder un texte en UTF-8',
        description='Convertit un texte en sequence hexadecimale UTF-8',
        parameters=[
            OpenApiParameter(
                name='texte',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Texte a encoder',
                examples=[
                    OpenApiExample('Simple', value='cafe'),
                    OpenApiExample('Bonjour', value='Bonjour'),
                ])
        ]),
    post=extend_schema(
        tags=['encoder'],
        summary='Encoder via POST',
        examples=[
            OpenApiExample(
                'Exemple',
                value={'texte': 'cafe'},
                request_only=True),
        ]))
class EncoderAPIView(APIView):
    """Encode un texte en UTF-8"""

    def get(self, request):
        texte = request.query_params.get('texte', '')
        if not texte:
            return Response(
                {'erreur': 'Parametre texte requis'},
                status=status.HTTP_400_BAD_REQUEST)
        return self._encoder(request, texte)

    def post(self, request):
        ser = EncoderSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors,
                status=status.HTTP_400_BAD_REQUEST)
        return self._encoder(
            request, ser.validated_data['texte'])

    def _encoder(self, request, texte):
        try:
            res = encoder_texte(texte)
            sauvegarder(request, 'ENCODE',
                texte, res['hex'],
                res['nb_chars'], res['nb_octets'])
            return Response({
                'texte':     texte,
                'hex':       res['hex'],
                'nb_chars':  res['nb_chars'],
                'nb_octets': res['nb_octets'],
                'details':   res['details'],
            })
        except Exception as e:
            return Response({'erreur': str(e)},
                status=status.HTTP_400_BAD_REQUEST)


# ════════════════════════════════════════════
#  DECODEUR
# ════════════════════════════════════════════
@extend_schema_view(
    get=extend_schema(
        tags=['decoder'],
        summary='Decoder une sequence hex UTF-8',
        parameters=[
            OpenApiParameter(
                name='hex',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Sequence hex a decoder',
                examples=[
                    OpenApiExample('e accent', value='C3 A9'),
                    OpenApiExample('Euro', value='E2 82 AC'),
                    OpenApiExample('Emoji', value='F0 9F 90 8D'),
                ])
        ]),
    post=extend_schema(
        tags=['decoder'],
        summary='Decoder via POST'))
class DecoderAPIView(APIView):
    """Decode une sequence hex UTF-8"""

    def get(self, request):
        hex_str = request.query_params.get('hex', '')
        if not hex_str:
            return Response(
                {'erreur': 'Parametre hex requis'},
                status=status.HTTP_400_BAD_REQUEST)
        return self._decoder(request, hex_str)

    def post(self, request):
        ser = DecoderSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors,
                status=status.HTTP_400_BAD_REQUEST)
        return self._decoder(
            request, ser.validated_data['hex'])

    def _decoder(self, request, hex_str):
        try:
            res = decoder_hex(hex_str)
            sauvegarder(request, 'DECODE',
                hex_str, res['texte'],
                len(res['texte']), len(res['details']))
            return Response({
                'texte':   res['texte'],
                'details': res['details'],
            })
        except Exception as e:
            return Response({'erreur': str(e)},
                status=status.HTTP_400_BAD_REQUEST)


# ════════════════════════════════════════════
#  ANALYSER
# ════════════════════════════════════════════
@extend_schema_view(
    get=extend_schema(
        tags=['analyser'],
        summary='Analyser un caractere Unicode',
        parameters=[
            OpenApiParameter(
                name='char',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Caractere a analyser',
                examples=[
                    OpenApiExample('A', value='A'),
                    OpenApiExample('Euro', value='E'),
                ])
        ]),
    post=extend_schema(
        tags=['analyser'],
        summary='Analyser via POST'))
class AnalyserAPIView(APIView):
    """Analyse un caractere Unicode"""

    def get(self, request):
        char = request.query_params.get('char', '')
        if not char:
            return Response(
                {'erreur': 'Parametre char requis'},
                status=status.HTTP_400_BAD_REQUEST)
        return self._analyser(request, char)

    def post(self, request):
        ser = AnalyserSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors,
                status=status.HTTP_400_BAD_REQUEST)
        return self._analyser(
            request, ser.validated_data['char'])

    def _analyser(self, request, char):
        try:
            res = analyser_char(char[0])
            sauvegarder(request, 'ANALYSE',
                char[0], res['hex'], 1, res['n'])
            return Response({
                'char':    res['char'],
                'cp':      res['cp'],
                'cp_hex':  format(res['cp'], '04X'),
                'hex':     res['hex'],
                'bin':     res['bin'],
                'n':       res['n'],
                'raw_int': res['raw_int'],
                'nom':     res['nom'],
                'cat':     res['cat'],
            })
        except Exception as e:
            return Response({'erreur': str(e)},
                status=status.HTTP_400_BAD_REQUEST)


# ════════════════════════════════════════════
#  COMPARER
# ════════════════════════════════════════════
@extend_schema_view(
    get=extend_schema(
        tags=['comparer'],
        summary='Comparer deux textes UTF-8',
        parameters=[
            OpenApiParameter(
                name='t1',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Premier texte'),
            OpenApiParameter(
                name='t2',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Deuxieme texte'),
        ]),
    post=extend_schema(
        tags=['comparer'],
        summary='Comparer via POST',
        examples=[
            OpenApiExample(
                'cafe vs cafe accent',
                value={'texte1': 'cafe', 'texte2': 'cafe'},
                request_only=True),
        ]))
class ComparerAPIView(APIView):
    """Compare deux textes UTF-8"""

    def get(self, request):
        t1 = request.query_params.get('t1', '')
        t2 = request.query_params.get('t2', '')
        if not t1 or not t2:
            return Response(
                {'erreur': 'Parametres t1 et t2 requis'},
                status=status.HTTP_400_BAD_REQUEST)
        return self._comparer(request, t1, t2)

    def post(self, request):
        ser = ComparerSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors,
                status=status.HTTP_400_BAD_REQUEST)
        t1 = ser.validated_data['texte1']
        t2 = ser.validated_data['texte2']
        return self._comparer(request, t1, t2)

    def _comparer(self, request, t1, t2):
        try:
            res = comparer(t1, t2)
            res['diff_octets'] = abs(
                res['oct1'] - res['oct2'])
            sauvegarder(request, 'COMPARE',
                t1 + ' vs ' + t2,
                str(len(res['differences'])) + ' diff.',
                len(t1) + len(t2),
                res['oct1'] + res['oct2'])
            return Response({
                'texte1':      t1,
                'texte2':      t2,
                'oct1':        res['oct1'],
                'oct2':        res['oct2'],
                'diff_octets': res['diff_octets'],
                'identiques':  res['identiques'],
                'nb_diff':     len(res['differences']),
                'differences': res['differences'],
            })
        except Exception as e:
            return Response({'erreur': str(e)},
                status=status.HTTP_400_BAD_REQUEST)


# ════════════════════════════════════════════
#  STATS
# ════════════════════════════════════════════
@extend_schema_view(
    get=extend_schema(
        tags=['stats'],
        summary='Statistiques UTF-8 d un texte',
        parameters=[
            OpenApiParameter(
                name='texte',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Texte a analyser'),
        ]),
    post=extend_schema(
        tags=['stats'],
        summary='Stats via POST'))
class StatsAPIView(APIView):
    """Statistiques UTF-8 d un texte"""

    def get(self, request):
        texte = request.query_params.get('texte', '')
        if not texte:
            return Response(
                {'erreur': 'Parametre texte requis'},
                status=status.HTTP_400_BAD_REQUEST)
        return self._stats(request, texte)

    def post(self, request):
        ser = StatsSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors,
                status=status.HTTP_400_BAD_REQUEST)
        return self._stats(
            request, ser.validated_data['texte'])

    def _stats(self, request, texte):
        try:
            res = analyser_texte(texte)
            sauvegarder(request, 'STATS',
                texte,
                str(res['nb_octets']) + ' octets',
                res['nb_chars'], res['nb_octets'])
            types_out = {}
            for n in range(1, 5):
                types_out[str(n)] = res['types'][n]
            return Response({
                'texte':     texte,
                'nb_chars':  res['nb_chars'],
                'nb_octets': res['nb_octets'],
                'pct_ascii': round(res['pct_ascii'], 2),
                'types':     types_out,
            })
        except Exception as e:
            return Response({'erreur': str(e)},
                status=status.HTTP_400_BAD_REQUEST)


# ════════════════════════════════════════════
#  HISTORIQUE
# ════════════════════════════════════════════
@extend_schema(
    tags=['historique'],
    summary='Historique des conversions',
    parameters=[
        OpenApiParameter(
            name='limit',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description='Nombre de resultats',
            default=20),
    ])
class HistoriqueAPIView(APIView):
    """Historique des conversions"""

    def get(self, request):
        limite = int(request.query_params.get('limit', 20))
        if request.user.is_authenticated:
            items = Historique.objects.filter(
                user=request.user)[:limite]
        else:
            items = Historique.objects.all()[:limite]
        ser = HistoriqueSerializer(items, many=True)
        return Response({
            'count':      len(ser.data),
            'historique': ser.data,
        })


# ════════════════════════════════════════════
#  FAVORIS
# ════════════════════════════════════════════
class FavoriAPIView(APIView):
    """Gestion des favoris"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = Favori.objects.filter(user=request.user)
        ser = FavoriSerializer(items, many=True)
        return Response(ser.data)

    def post(self, request):
        ser = FavoriSerializer(data=request.data)
        if ser.is_valid():
            ser.save(user=request.user)
            return Response(ser.data,
                status=status.HTTP_201_CREATED)
        return Response(ser.errors,
            status=status.HTTP_400_BAD_REQUEST)


# ════════════════════════════════════════════
#  API ROOT
# ════════════════════════════════════════════
@extend_schema(exclude=True)
@api_view(['GET'])
def api_root(request):
    """UTF-8 Converter API - Point d entree"""
    return Response({
        'message': 'UTF-8 Converter API v2.0',
        'version': '2.0',
        'docs':    request.build_absolute_uri('/api/docs/'),
        'redoc':   request.build_absolute_uri('/api/redoc/'),
        'routes': {
            'encoder':    request.build_absolute_uri('/api/encoder/'),
            'decoder':    request.build_absolute_uri('/api/decoder/'),
            'analyser':   request.build_absolute_uri('/api/analyser/'),
            'comparer':   request.build_absolute_uri('/api/comparer/'),
            'stats':      request.build_absolute_uri('/api/stats/'),
            'historique': request.build_absolute_uri('/api/historique/'),
            'favoris':    request.build_absolute_uri('/api/favoris/'),
        }
    })