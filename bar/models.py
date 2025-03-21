from django.db import models

class Producte(models.Model):
    nom = models.CharField(max_length=100)
    descripcio = models.TextField(blank=True, null=True)
    preu = models.DecimalField(max_digits=6, decimal_places=2)
    categoria = models.CharField(max_length=50, choices=[
        ('beguda', 'Beguda'),
        ('aperitiu', 'Aperitiu'),
        ('plat', 'Plat principal'),
        ('postre', 'Postre'),
    ])
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nom

class Comanda(models.Model):
    data_hora = models.DateTimeField(auto_now_add=True)
    client = models.CharField(max_length=100)
    estat = models.CharField(max_length=50, choices=[
        ('pendent', 'Pendent'),
        ('en_proces', 'En procés'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ], default='pendent')
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"Comanda {self.id} - {self.client}"

class DetallsComanda(models.Model):
    comanda = models.ForeignKey(Comanda, on_delete=models.CASCADE, related_name='detalls')
    producte = models.ForeignKey(Producte, on_delete=models.CASCADE)
    quantitat = models.PositiveIntegerField(default=1)
    preu_unitari = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.quantitat}x {self.producte.nom} a {self.preu_unitari}€"

    def preu_total(self):
        return self.quantitat * self.preu_unitari