from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuari(AbstractUser):
    auth_token = models.CharField(max_length=32,blank=True,null=True)

class Pelicula(models.Model):
    titol = models.CharField(max_length=200)
    durada = models.IntegerField(help_text="Durada en minuts")
    descripcio = models.TextField()
    genere = models.CharField(max_length=100)
    data_estrena = models.DateField()

    def __str__(self):
        return self.titol

class Sala(models.Model):
    nom = models.CharField(max_length=100)
    capacitat = models.IntegerField()

    def __str__(self):
        return self.nom

class Butaca(models.Model):
    STANDARD = "standard"
    PREMIUM = "premium"

    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='butaques')
    fila = models.IntegerField()
    numero = models.IntegerField()
    tipus = models.CharField(max_length=10,choices=[
            (STANDARD,"Estàndard"),
            (PREMIUM,"Premium")
        ])

    class Meta:
        unique_together = ('sala', 'fila', 'numero')

    def __str__(self):
        return f"Sala {self.sala.nom} - Fila {self.fila} - Butaca {self.numero}"

class Sessio(models.Model):
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE, related_name='sessions')
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='sessions')
    data_hora = models.DateTimeField()

    def __str__(self):
        return f"{self.pelicula.titol} - {self.sala.nom} - {self.data_hora}"

class Entrada(models.Model):
    sessio = models.ForeignKey(Sessio, on_delete=models.CASCADE, related_name='entrades')
    butaca = models.ForeignKey(Butaca, on_delete=models.CASCADE, related_name='entrades')
    preu = models.DecimalField(max_digits=6, decimal_places=2)
    comprador = models.ForeignKey(Usuari, on_delete=models.SET_NULL,
                            null=True, blank=True, related_name='entrades')
    data_compra = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sessio', 'butaca')

    def __str__(self):
        return f"Entrada per {self.sessio.pelicula.titol} - {self.butaca} - {self.comprador}"
