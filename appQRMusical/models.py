# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import os
from django.utils.timezone import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date

Valores_Online = [
    ("si", "si"),
    ("no", "no"),
]
Genero = [
    ("Masculino","Masculino"),
    ("Femenino","Femenino"),
]
Nivel = [
    (1,'1'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5'),
    (6,'6'),
    (7,'7'),
]

# Creat tus modelos aqui.

#Entidad que guarda los indicadores presentes en las actividades

class Indicador(models.Model):
    id_indicador =  models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=True)
    descripcion = models.TextField(blank=True)
    def __str__(self):
        return self.nombre

#Entidad que guarda las actividades

class Actividad(models.Model):
	id = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=100)
	descripcion = models.CharField(max_length=200, blank=True)
	proposito = models.CharField(max_length=100, blank=True)
	indicador = models.ManyToManyField(Indicador, blank=True)

	def __str__(self):
		return self.nombre

#Directorio donde se suben los ficheros

def directory_to_upload(self, file):
    nombre, extension = os.path.splitext(file)
    extension.lower()
    directory = ''

    if extension == '.jpg' or extension == '.jpeg':
        directory = 'images/'

    elif extension == '.mp3':
        directory = 'songs/'

    elif extension == '.mp4':
        directory = 'movies/'

    return os.path.join(directory, file)

def calcular_edad(self,fecha_de_nacimiento):
    hoy = date.today()
    return hoy.year - fecha_de_nacimiento.year - ((hoy.month, hoy.day) < (fecha_de_nacimiento.month, fecha_de_nacimiento.day))

#Entidad que guarda los pacientes existentes en el sistema

class Paciente(models.Model):
    id = models.AutoField(primary_key=True)
    imagen = models.ImageField(upload_to='profiles/', blank=True)
    nombre = models.CharField("Nombre",max_length=50)
    apellido = models.CharField("Apellido",max_length=50)
    fecha_de_nacimiento = models.DateField(null=True,blank=True)
    edad = models.IntegerField(null=True,blank=True)
    genero = models.CharField(max_length=10,choices = Genero, blank=True)
    nivel = models.IntegerField(choices = Nivel,default=1)
    codigo = models.CharField(max_length=8, blank=True)
    online = models.CharField(max_length=10, choices=Valores_Online, default="no")
    def __str__(self):
        return self.nombre

#Entidad que guarda los especialistas

class Especialista(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField("Nombre",max_length=50)
    apellido = models.CharField("Apellido",max_length=50)
    email = models.EmailField()    

@receiver(post_save, sender=User)
def create_therapist_profile(sender, instance, created, **kwargs):
    if created:
        Especialista.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_therapist_profile(sender, instance, **kwargs):
    instance.especialista.save()


#Entidad que guarda los tratamientos

class Tratamiento(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField("Nombre",max_length=50) 
    paciente = models.ForeignKey(Paciente,on_delete=models.CASCADE)
    fecha_inicio = models.DateField(null=True,blank=True)
    fecha_fin = models.DateField(null=True,blank=True)
    descripcion = models.TextField(blank=True)
    activado = models.BooleanField(default=False)
    def __str__(self):
        return self.nombre


#Entidad que guarda las terapias

class Terapia(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField("Nombre",max_length=50) 
    descripcion = models.TextField(blank=True)
    tipo = models.CharField("Tipo",max_length=50)
    def __str__(self):
        return self.nombre

#Entidad que guarda las asiganaciones de las terapias y los tratamientos

class Asigna_Terapia(models.Model):
    id_asign_therapy = models.AutoField(primary_key=True)
    terapia = models.ManyToManyField(Terapia)
    tratamiento = models.ForeignKey(Tratamiento,on_delete=models.CASCADE)
 
#Entidad que guarda el especialista ya la terapia asignada.

class Especialista_Asigna_Terapia(models.Model):
    asigna_terapia = models.ForeignKey(Asigna_Terapia,on_delete=models.CASCADE)
    especialista = models.ForeignKey(Especialista,on_delete=models.CASCADE)
    fecha = models.DateField(null=True,blank=True)
    class Meta:
        unique_together = ("asigna_terapia","especialista","fecha")

#Entidad que guarda el especialista que supervisa un tratamiento

class Supervisa(models.Model):
    especialista = models.ForeignKey(Especialista,on_delete=models.CASCADE)
    tratamiento = models.ForeignKey(Tratamiento,on_delete=models.CASCADE)
    class Meta:
        unique_together = ("especialista","tratamiento")

#Entidad que guarda las actividades

class Diagnostico(models.Model):
    id_diagnostico = models.AutoField(primary_key=True)
    paciente = models.ForeignKey(Paciente,on_delete=models.CASCADE)
    fecha = datetime.today()
    valoracion = models.CharField(max_length=50, blank=True)
    notas = models.TextField(blank=True)

#Entidad que guarda las sesiones de los pacientes

class Sesion(models.Model):
    id_sesion = models.AutoField(primary_key=True)
    asigna_Terapia = models.ForeignKey(Asigna_Terapia,on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

#Entidad que almacena los indicadores asociados a una actividad
"""
class Actividad_Indicador(models.Model):
    actividad = models.ForeignKey(Actividad,on_delete=models.CASCADE)
    indicador = models.ForeignKey(Indicador,on_delete=models.CASCADE)
    class Meta:
        unique_together = ("actividad","indicador")
"""
#Entidad que guarda las actividades

class Terapia_Actividad(models.Model):
    actividad = models.ForeignKey(Actividad,on_delete=models.CASCADE)
    terapia = models.ForeignKey(Terapia,on_delete=models.CASCADE)
    class Meta:
        unique_together = ("actividad","terapia")

#Entidad que guarda las actividades

class Terapia_Indicador(models.Model):
    terapia = models.ForeignKey(Terapia,on_delete=models.CASCADE)
    indicador = models.ForeignKey(Indicador,on_delete=models.CASCADE)
    class Meta:
        unique_together = ("terapia","indicador")

#Entidad que guarda las actividades

class Resultado_Sesion(models.Model):
    sesion = models.ForeignKey(Sesion,on_delete=models.CASCADE)
    indicador = models.ForeignKey(Indicador,on_delete=models.CASCADE)
    actividad = models.ForeignKey(Actividad,on_delete=models.CASCADE)
    resultado =  models.TextField(blank=True)
    class Meta:
        unique_together = ("sesion","indicador","actividad")

#Entidad que guarda las actividades

class Categoria(models.Model):
    id_categoria =  models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=True)
    def __str__(self):
        return self.nombre

#Entidad que guarda las actividades

class Categoria_Actividad(models.Model):
    categoria = models.ForeignKey(Categoria,on_delete=models.CASCADE)
    actividad = models.ForeignKey(Actividad,on_delete=models.CASCADE)
    class Meta:
        unique_together = ("categoria","actividad")

#Entidad que guarda las actividades

class Contenido(models.Model):
    id_contenido =  models.AutoField(primary_key=True)
    desripcion =  models.CharField(max_length=50, blank=True)
    codigo = models.CharField(max_length=8, blank=True)

#Entidad que guarda las actividades

class Texto(Contenido):
    data =  models.CharField(max_length=50, blank=True)

#Entidad que guarda las actividades

class Multimedia(Contenido):
	nombre = models.CharField(max_length=100)
	file = models.FileField(upload_to=directory_to_upload, null=True, blank=True)
	imagen = models.ImageField(upload_to='images/')
	filetype = models.CharField(max_length=3)
	datetime = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('datetime',)

	def __str__(self):
		return self.nombre

#Entidad que guarda las actividades

class Actividad_Contenido(models.Model):
    actividad= models.ForeignKey(Actividad,on_delete=models.CASCADE)
    contenido = models.ForeignKey(Contenido,on_delete=models.CASCADE)
    class Meta:
        unique_together = ("actividad","contenido")

