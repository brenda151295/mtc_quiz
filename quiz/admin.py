from django.contrib import admin
from quiz.models import Pregunta
from import_export.admin import ImportExportModelAdmin

@admin.register(Pregunta)
class ClientRequestAdmin(ImportExportModelAdmin):
    list_display = ['enunciado']
    search_fields = ['enunciado']
