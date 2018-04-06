from django.contrib import admin
from .models import Pregunta

@admin.register(Pregunta)
class ClientRequestAdmin(admin.ModelAdmin):
    list_display = ['enunciado']
    search_fields = ['enunciado']