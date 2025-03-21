from ninja import NinjaAPI
from sales.models import *
from typing import List
from ninja import Schema
from datetime import date

api = NinjaAPI()

class PeliculaOut(Schema):
    titol: str
    durada: int
    genere: str

class PeliculaIn(Schema):
    titol : str
    durada : int
    descripcio : str
    genere : str
    data_estrena : date

@api.get("/pelicules", response=List[PeliculaOut])
def pelicules(request):
    return Pelicula.objects.all()

@api.post("/crear/pelicula")
def crearPelicula(request, payload: PeliculaIn):
    pelicula = Pelicula.objects.create(**payload.dict())
    return {"id": pelicula.id}



class ButacaOut(Schema):
    fila:int
    numero:int
    tipus:str

class SalesOut(Schema):
    nom: str
    capacitat: int
    butaques: List[ButacaOut]

#butaques -> devuelve la lista porque en el modelo de Sala esta definido como related model
@api.get("/sales", response=List[SalesOut])
def obtenirSales(request):
    sales = Sala.objects.all()
    return sales

# curl localhost:8000/api/pelicules