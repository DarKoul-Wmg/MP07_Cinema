import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
from sales.models import Pelicula, Sala, Butaca, Sessio, Entrada

fake = Faker()
Usuari = get_user_model()  

class Command(BaseCommand):
    help = "Seed database with fake data"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Eliminando datos previos..."))
        Entrada.objects.all().delete()
        Sessio.objects.all().delete()
        Butaca.objects.all().delete()
        Sala.objects.all().delete()
        Pelicula.objects.all().delete()
        Usuari.objects.filter(is_superuser=False).delete()
        
        self.stdout.write(self.style.SUCCESS("Generando datos falsos..."))

        # Crear usuarios
        usuarios = [Usuari.objects.create_user(username=fake.user_name(), email=fake.email(), password="password") for _ in range(5)]
        
        # Crear películas
        peliculas = [Pelicula.objects.create(
            titol=fake.sentence(nb_words=3),
            durada=random.randint(80, 180),
            descripcio=fake.text(),
            genere=random.choice(["Acció", "Drama", "Comèdia", "Terror", "Ciència Ficció"]),
            data_estrena=fake.date_between(start_date="-5y", end_date="today")
        ) for _ in range(10)]
        
        # Crear salas
        salas = [Sala.objects.create(nom=f"Sala {i+1}", capacitat=random.randint(50, 200)) for i in range(5)]
        
        # Crear butacas
        for sala in salas:
            for fila in range(1, 6):  # 5 filas
                for numero in range(1, 11):  # 10 asientos por fila
                    Butaca.objects.create(
                        sala=sala,
                        fila=fila,
                        numero=numero,
                        tipus=random.choice([Butaca.STANDARD, Butaca.PREMIUM])
                    )
        
        # Crear sesiones
        sesiones = [Sessio.objects.create(
            pelicula=random.choice(peliculas),
            sala=random.choice(salas),
            data_hora=fake.date_time_between(start_date="now", end_date="+30d")
        ) for _ in range(10)]
        
        # Crear entradas
        butacas = Butaca.objects.all()
        for _ in range(20):
            sessio = random.choice(sesiones)
            butaca = random.choice(butacas)
            Entrada.objects.create(
                sessio=sessio,
                butaca=butaca,
                preu=round(random.uniform(5.0, 20.0), 2),
                comprador=random.choice(usuarios) if random.random() > 0.2 else None
            )
        
        self.stdout.write(self.style.SUCCESS("Datos generados exitosamente!"))
