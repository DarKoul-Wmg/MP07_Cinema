from ninja import NinjaAPI, Schema
from sales.models import *
from typing import List
from datetime import date

from django.contrib.auth import authenticate as djangoauth
from ninja.security import HttpBasicAuth, HttpBearer
import secrets

api = NinjaAPI()

# Autenticació bàsica
class BasicAuth(HttpBasicAuth):
    def authenticate(self, request, username, password):
        user = djangoauth(username=username, password=password)
        if user:
            # return user
            # Genera un token simple
            token = secrets.token_hex(16)
            user.auth_token = token
            user.save()
            return token
        return None

class BasicAuth(HttpBasicAuth):
    def authenticate(self, request, username, password):
        user = djangoauth(username=username, password=password)
        if user:
            # return user
            # Genera un token simple
            token = secrets.token_hex(16)
            user.auth_token = token
            user.save()
            return token
        return None


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
# @api.get("/sales", response=List[SalesOut], auth=BasicAuth())
# def obtenirSales(request):
#     sales = Sala.objects.all()
#     return sales
@api.get("/sales", response=List[SalesOut], auth=AuthBearer())
def obtenirSales(request):
    sales = Sala.objects.all()
    return sales

# curl localhost:8000/api/pelicules 
#curl -H 'Authorization:Bearer YWRtaW46YWRtaW4xMjM=' http://localhost:8000/api/users/