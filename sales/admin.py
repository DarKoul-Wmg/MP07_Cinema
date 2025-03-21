from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Pelicula)

# class SalaAdmin(admin.ModelAdmin):
#     fields = ("")
#     inlines = []

admin.site.register(Sala) #SalaAdmin

# class ButacaInline(admin.TabularInline):
#     model = Choice
#     extra = 3

admin.site.register(Butaca)#ButacaInline
admin.site.register(Sessio)
admin.site.register(Entrada)