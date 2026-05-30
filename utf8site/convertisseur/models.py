from django.db import models
from django.contrib.auth.models import User


class Historique(models.Model):

    OPERATIONS = [
        ('ENCODE',  'Encodage'),
        ('DECODE',  'Decodage'),
        ('ANALYSE', 'Analyse'),
        ('STATS',   'Statistiques'),
    ]

    user       = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True, blank=True)
    operation  = models.CharField(
        max_length=10,
        choices=OPERATIONS)
    entree     = models.TextField()
    sortie     = models.TextField()
    nb_chars   = models.IntegerField(default=0)
    nb_octets  = models.IntegerField(default=0)
    date       = models.DateTimeField(
        auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Historique'

    def __str__(self):
        username = self.user.username \
            if self.user else 'Anonyme'
        return (f"{self.operation} - "
                f"{self.entree[:20]} - "
                f"{username}")


class Favori(models.Model):

    user      = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True, blank=True)
    nom       = models.CharField(max_length=50)
    texte     = models.CharField(max_length=100)
    hex_utf8  = models.TextField()
    date      = models.DateTimeField(
        auto_now_add=True)

    class Meta:
        ordering = ['nom']
        verbose_name = 'Favori'

    def __str__(self):
        return f"{self.nom} - {self.texte}"