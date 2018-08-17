# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import os
from django.utils.timezone import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

Values_Online = [
    ("yes", "yes"),
    ("no", "no"),
]
Gender_Choice = [
    ("Male","Male"),
    ("Female","Female"),
]
Level_Choice = [
    (1,'1'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5'),
    (6,'6'),
    (7,'7'),
]

# Create your models here.
class Player(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=200, blank=True)
	purpose = models.CharField(max_length=100, blank=True)

	def __str__(self):
		return self.name


def directory_to_upload(self, file):
    name, extension = os.path.splitext(file)
    extension.lower()
    directory = ''

    if extension == '.jpg' or extension == '.jpeg':
        directory = 'images/'

    elif extension == '.mp3':
        directory = 'songs/'

    elif extension == '.mp4':
        directory = 'movies/'

    return os.path.join(directory, file)

class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='profiles/', blank=True)
    name = models.CharField("Name",max_length=50)
    surname = models.CharField("Surname",max_length=50)
    date_of_birth = models.DateField(null=True,blank=True)
    age = models.IntegerField("Age",default=0)
    gender = models.CharField(max_length=10,choices = Gender_Choice, blank=True)
    level = models.IntegerField(choices = Level_Choice,default=1)
    code = models.CharField(max_length=8, blank=True)
    online = models.CharField(max_length=10, choices=Values_Online, default="no")
    def __str__(self):
        return self.name

class Therapist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField("Name",max_length=50)
    surname = models.CharField("Surname",max_length=50)
    email = models.EmailField()    

@receiver(post_save, sender=User)
def create_therapist_profile(sender, instance, created, **kwargs):
    if created:
        Therapist.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_therapist_profile(sender, instance, **kwargs):
    instance.therapist.save()


class Therapy(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField("Name",max_length=50) 
    description = models.TextField(blank=True)
    therapy_type = models.CharField("Type",max_length=50)
    def __str__(self):
        return self.name

class Treatment(models.Model):
    id = models.AutoField(primary_key=True)
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    start_date = models.DateField(null=True,blank=True)
    end_date = models.DateField(null=True,blank=True)
    description = models.TextField(blank=True)
    enabled = models.BooleanField(default=False)
    def __str__(self):
        return str(self.id) + str('-') + self.profile.name

class Asign_Therapy(models.Model):
    id_asign_therapy = models.AutoField(primary_key=True)
    therapy = models.ForeignKey(Therapy,on_delete=models.CASCADE)
    treatment = models.ForeignKey(Treatment,on_delete=models.CASCADE)
 
class Therapist_Asign_Therapy(models.Model):
    asign_therapy = models.ForeignKey(Asign_Therapy,on_delete=models.CASCADE)
    therapist = models.ForeignKey(Therapist,on_delete=models.CASCADE)
    date = models.DateField(null=True,blank=True)
    class Meta:
        unique_together = ("asign_therapy","therapist","date")

class Supervise(models.Model):
    therapist = models.ForeignKey(Therapist,on_delete=models.CASCADE)
    treatment = models.ForeignKey(Treatment,on_delete=models.CASCADE)
    class Meta:
        unique_together = ("therapist","treatment")

class Diagnostic(models.Model):
    id_diagnostic = models.AutoField(primary_key=True)
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    date = datetime.today()
    assesment = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)

class Session(models.Model):
    id_session = models.AutoField(primary_key=True)
    asign_therapy = models.ForeignKey(Asign_Therapy,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

class Indicator(models.Model):
    id_indicator =  models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name

class Player_Indicator(models.Model):
    player = models.ForeignKey(Player,on_delete=models.CASCADE)
    indicator = models.ForeignKey(Indicator,on_delete=models.CASCADE)
    class Meta:
        unique_together = ("player","indicator")

class Therapy_Player(models.Model):
    player = models.ForeignKey(Player,on_delete=models.CASCADE)
    therapy = models.ForeignKey(Therapy,on_delete=models.CASCADE)
    class Meta:
        unique_together = ("player","therapy")

class Therapy_Indicator(models.Model):
    therapy = models.ForeignKey(Therapy,on_delete=models.CASCADE)
    indicator = models.ForeignKey(Indicator,on_delete=models.CASCADE)
    class Meta:
        unique_together = ("therapy","indicator")

class Result_Session(models.Model):
    session = models.ForeignKey(Session,on_delete=models.CASCADE)
    indicator = models.ForeignKey(Indicator,on_delete=models.CASCADE)
    player = models.ForeignKey(Player,on_delete=models.CASCADE)
    result =  models.TextField(blank=True)
    class Meta:
        unique_together = ("session","indicator","player")

class Category(models.Model):
    id_category =  models.AutoField(primary_key=True)
    category = models.CharField(max_length=50, blank=True)
    def __str__(self):
        return self.category

class Category_Player(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    player = models.ForeignKey(Player,on_delete=models.CASCADE)
    class Meta:
        unique_together = ("category","player")

class Content(models.Model):
    id_content =  models.AutoField(primary_key=True)
    desription =  models.CharField(max_length=50, blank=True)
    code = models.CharField(max_length=8, blank=True)

class Text(Content):
    data =  models.CharField(max_length=50, blank=True)

class Multimedia(Content):
	name = models.CharField(max_length=100)
	file = models.FileField(upload_to=directory_to_upload, null=True, blank=True)
	image = models.ImageField(upload_to='images/')
	filetype = models.CharField(max_length=3)
	datetime = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('datetime',)

	def __str__(self):
		return self.name

class Player_Content(models.Model):
    player= models.ForeignKey(Player,on_delete=models.CASCADE)
    content = models.ForeignKey(Content,on_delete=models.CASCADE)
    class Meta:
        unique_together = ("player","content")

