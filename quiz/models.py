from django.db import models
from quiz import constants

class Pregunta(models.Model):

    tema = models.CharField(max_length=4, choices=constants.TEMAS)

    enunciado = models.CharField(max_length=256)
    imagen_enunciado= models.ImageField(upload_to='preguntas', null=True, blank=True)

    alternativa_1 = models.CharField(max_length=256)
    alternativa_2 = models.CharField(max_length=256)
    alternativa_3 = models.CharField(max_length=256)
    alternativa_4 = models.CharField(max_length=256)

    imagen_alternativa_1 = models.ImageField(upload_to='alternativas', null=True, blank=True);
    imagen_alternativa_2 = models.ImageField(upload_to='alternativas', null=True, blank=True);
    imagen_alternativa_3 = models.ImageField(upload_to='alternativas', null=True, blank=True);
    imagen_alternativa_4 = models.ImageField(upload_to='alternativas', null=True, blank=True);

    alternativa_correcta = models.CharField(max_length=1, choices=constants.ALTERNATIVAS)

    categoria_AI = models.BooleanField(default = False)
    categoria_AIIA = models.BooleanField(default = False)
    categoria_AIIB = models.BooleanField(default = False)
    categoria_AIIIA = models.BooleanField(default = False)
    categoria_AIIIB = models.BooleanField(default = False)
    categoria_AIIIC = models.BooleanField(default = False)  

    def __unicode__(self):
        return enunciado