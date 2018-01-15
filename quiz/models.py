from django.db import models

class Pregunta(models.Model):
    enunciado = models.CharField(max_length=256)
    alternativa_correcta = models.CharField(max_length=256)
    alternativa_incorrecta_1 = models.CharField(max_length=256)
    alternativa_incorrecta_2 = models.CharField(max_length=256)
    alternativa_incorrecta_3 = models.CharField(max_length=256)
    TEMAS = (
        ('T1', 'Tema1'),
        ('T2', 'Tema2'),
        ('T3', 'Tema3'),
        ('T4', 'Tema4'),
    	)
    tema = models.CharField(max_length=4, choices=TEMAS)
    imagen = models.ImageField(upload_to='imagenes', null=True, blank=True)