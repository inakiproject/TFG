# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, DeleteView, UpdateView, CreateView
from datetime import datetime, time, date

#Users
from django.contrib.auth.models import User

# Login
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

# Settings
from django.contrib.auth.mixins import LoginRequiredMixin

# Play + Multimedia
from .models import Actividad
from . import global_vars

# Multimedia
from .models import Multimedia, Contenido, Actividad_Contenido
import os
from PIL import Image
from django.conf import settings
from django.views.generic.edit import FormView
from .forms import UploadMultimediaForm

# Player
from .models import Actividad
from .forms import FormularioActividad
from django.urls import reverse_lazy, reverse

# Paciente
from .models import Paciente
from .forms import UploadUserForm

# Especialista
from .models import Especialista
from .forms import FormularioEspecialista

# Terapia
from .models import Terapia, Asigna_Terapia, Especialista_Asigna_Terapia, Terapia_Actividad
from .forms import UploadTherapyForm, UploadAsign, UploadTherapyFormActividad, UploadAsignTherapyForm, UploadOneActividadTherapyForm, UploadOnePlayerTerapiaForm

# Tratamiento
from .models import Tratamiento, Supervisa
from .forms import UploadTreatmentForm

# Diagnostico
from .models import Diagnostico
from .forms import UploadDiagnosticForm

# Indicador
from .models import Indicador, Terapia_Indicador
from .forms import UploadIndicatorForm

# Categoria
from .models import Categoria, Categoria_Actividad
from .forms import UploadCategoryForm, FormularioCategoriaActividad

#Sesion
from .models import Sesion, Resultado_Sesion

#Player Game
import threading
import subprocess
#import RPi.GPIO as GPIO
import time
#GPIO.setmode(GPIO.BOARD)

# Card reader
import sys, time, serial
import pygame
from pygame import mixer
serialPort ='/dev/ttyACM0'

# User Settings
from .forms import EditNameForm, EditEmailForm, EditPassForm
from django.contrib.auth.hashers import make_password

from django.http import JsonResponse

# Create your views here.

#Lector de Codigos que guarda en global vars el codigo leido.

def read_ID():
    arduinoPort = serial.Serial(serialPort, 9600, timeout=1)
    code = 0

    while True:
        tag = arduinoPort.readline()
        code = tag.decode('utf-8')
        if hash(tag) != 0:
            #global_vars.message = code
            #arduinoPort.flushInput()
            if len(code)==8:
                global_vars.message = code
                arduinoPort.flushInput()
                #arduinoPort.close()
            else:
                arduinoPort.flushInput()

#Llamada al hilo que llama al lector para el juego



def start_reader():
    #global_vars.message = 'Put the card near the scanner'
    t1 = threading.Thread(target=read_ID)
    t1.start()

#Lector para identficación de usuario, elementos multimedia etc

def Identify_ID():
    arduinoPort = serial.Serial(serialPort, 9600, timeout=1)
    code = 0

    while True:
        tag = arduinoPort.readline()
        code = tag.decode('utf-8')
        if hash(tag) != 0:
            #global_vars.message = code
            #arduinoPort.flushInput()
            if len(code)==8:
                return code
                arduinoPort.flushInput()
                #arduinoPort.close()
            else:
                arduinoPort.flushInput()

#Vista de la pagina inicial

class Home(TemplateView):
	template_name="home.html"
	def get_context_data(self, **kwargs):
		context = super(Home, self).get_context_data(**kwargs)
		try:
			player = Paciente.objects.get(online="si")
		except Paciente.DoesNotExist:
			player = None

		context['QRM_color'] = "QRM_blue"
		context['player'] = player
		return context

#Vista de la elección de tratamiento una vez identificado el paciente

class Choose_treatment(TemplateView):
	pygame.mixer.init()
	pygame.mixer.stop()
	template_name="choose_treatment.html"
	model = Actividad.objects.all()
	def get_context_data(self, **kwargs):
		context = super(Choose_treatment, self).get_context_data(**kwargs)
		try:
			actividad = Paciente.objects.get(online="si")
		except Paciente.DoesNotExist:
			actividad = None
			return context

		actividad = Paciente.objects.get(online="si")

		content = list()
		skip = 1
		terapy = Terapia.objects.all()
		tera2 = Tratamiento.objects.filter(activado=True)
		tera2 = Asigna_Terapia.objects.filter(tratamiento_id__in=tera2.filter(paciente_id=actividad.id))
		for i in tera2:
			content.append(i)
			skip = 0
		context['treat'] = tera2
		context['therapy_p'] = Terapia_Actividad.objects.all()
		context['content'] = content
		context['skip'] = skip
		context['QRM_color'] = "QRM_pink"
		context['player'] = actividad
		return context

#Vista de la elección de actividad una vez seleccionado tratamiento

def Play(request, pk):
	print("Antes")
	print(global_vars.end)
	global_vars.end = 0
	print("Despues")
	print(global_vars.end)
	try:
		actividad = Paciente.objects.get(online="si")
	except Paciente.DoesNotExist:
		actividad = None
		return context
	print(pk)
	actividad = Paciente.objects.get(online="si")
	tera = Asigna_Terapia.objects.filter(pk=pk)
	print(tera)
	skip = 1
	for i in tera:
		for j in i.terapia.all():
			for k in Terapia_Actividad.objects.all():
				if j.id == k.terapia.id:
					skip = 0


	context = {
		'therapy_p' : Terapia_Actividad.objects.all(),
		'content' : tera,
		'skip' : skip,
		'QRM_color' : "QRM_pink",
		'player' : actividad
	}
	return render(request, 'play.html', context)		

#Almacena el mensaje presente en las variables globales

def message(request):
	context = {'glob_message' : global_vars.message,}


def blink(nTimes, speed, pin):
	GPIO.setup(pin, GPIO.OUT)
	for i in range(0, nTimes):
		GPIO.output(pin, True)
		time.sleep(speed)
		GPIO.output(pin, False)
		time.sleep(speed)
	print("Blink finished")


class Buzzer(object):
	def __init__(self, buzzer_pin):
		GPIO.setmode(GPIO.BOARD)  
		self.buzzer_pin = buzzer_pin  
		GPIO.setup(self.buzzer_pin, GPIO.IN)
		GPIO.setup(self.buzzer_pin, GPIO.OUT)
		print("buzzer ready")

	def __del__(self):
		class_name = self.__class__.__name__
		print (class_name, "finished")

	def buzz(self,pitch, duration):   		#create the function buzz and feed it the pitch and duration
		if(pitch==0):
			time.sleep(duration)
			return
		period = 1.0 / pitch     			#in physics, the period (sec/cyc) is the inverse of the frequency (cyc/sec)
		delay = period / 2     				#calcuate the time for half of the wave  
		cycles = int(duration * pitch)   	#the number of waves to produce is the duration times the frequency

		for i in range(cycles):    			#start a loop from 0 to the variable cycles calculated above
			GPIO.output(self.buzzer_pin, True)   #set pin 18 to high
			time.sleep(delay)    			#wait with pin 18 high
			GPIO.output(self.buzzer_pin, False)    #set pin 18 to low
			time.sleep(delay)    			#wait with pin 18 low

	def play(self, tune):
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.buzzer_pin, GPIO.OUT)
		x=0

		print("Playing tune ",tune)
		if(tune==1): 	# Success
			pitches=[523, 700, 1047]			
			duration=[0.1,0.1,0.1]
			for p in pitches:
				self.buzz(p, duration[x])  #feed the pitch and duration to the func$
				time.sleep(duration[x] *0.5)
				x+=1

		else: 			# Fail
			pitches=[392,294]
			duration=[0.1,0.1]
			for p in pitches:
				self.buzz(p, duration[x])  #feed the pitch and duration to the func$
				time.sleep(duration[x] *0.5)
				x+=1

		GPIO.setup(self.buzzer_pin, GPIO.IN)


def read_code():
		data = global_vars.zbar_status.readline()
		qrcode = str(data)[8:]
		if qrcode:
			print(qrcode)
			global_vars.message = qrcode


def start_cam():
	if global_vars.cam == 0:
		global_vars.message = 'Get close QR code to cam'
		global_vars.cam = 1

	elif global_vars.cam == 1:
		global_vars.zbar_status = os.popen('/usr/bin/zbarcam --prescale=%sx%s' % (global_vars.cam_width, global_vars.cam_height),'r')
		global_vars.cam = 2
		
	elif global_vars.cam == 2:
		if global_vars.zbar_status != None:
			t = threading.Thread(target=read_code)
			t.start()	

#Llama al lector de codigo e identifica al paciente

def Identify(request):
	coder = Identify_ID()
	try:
		user = Paciente.objects.get(codigo=coder)
		user.online = "si"
		user.save()
		context = {
			'QRM_color' : "QRM_blue",
			'message_alert' : "alert-info",
			'message_head' : user.nombre,
			'player' : user
    	}
		return HttpResponseRedirect('/choose_treatment/')
		return render(request, 'home.html', context)		
	except:
		user = None
		context = {
			'QRM_color' : "QRM_blue",
			'message_alert' : "alert-info",
			'message_head' : "No se ha encontrado un jugador con este Identificador",
			'message_text' : ", Por favor intentelo de nuevo",
			'player' : user
    	}	

	return render(request, 'info.html', context)

#Desconecta al usuario identificado

def Disconnect(request):
	try:
		user = Paciente.objects.get(online="si")
		user.online = "no"
		user.save()
		context = {
			'QRM_color' : "QRM_blue",
			'message_alert' : "alert-info",
			'message_head' : user.nombre,
			'player' : user
	    }
		return render(request, 'home.html', context)
	except Paciente.DoesNotExist:
		user = None
		context = {
			'QRM_color' : "QRM_blue",
	    }		

#Vista del juego principal

def gamem(id_player,asgn_thera,thera_indi):
	if global_vars.game_initialized == False: 	# First start of game
		mults = Actividad_Contenido.objects.filter(actividad_id=id_player)
		global_vars.game_number_objects = mults.count()
		mults = list(mults)
		global_vars.game_objects = mults
		global_vars.game_initialized = True
		sessionone = Sesion()
		sessionone.asigna_Terapia = asgn_thera
		sessionone.save()
		global_vars.identifier = sessionone.id_sesion
		global_vars.thera_indi = thera_indi
		global_vars.timestart =time.time()

	

	global_vars.match = 0
	url=""
	code = global_vars.message# del "\n" in end

	matching = False
	print(code)
	print(global_vars.end)

	if global_vars.game_success == global_vars.game_number_objects:
		global_vars.game_display = "inline"
		global_vars.timeend =  time.time()
		timefinal = global_vars.timeend - global_vars.timestart
		global_vars.time = round(timefinal,2)
		print("Fin del juego")
		print(global_vars.end)
		if global_vars.end == 0:
			print("Guardando resultados...")
			for i in global_vars.thera_indi:
				print(i.id_indicador)
				if i.id_indicador == 2:
					results = Resultado_Sesion()
					results.sesion = Sesion.objects.get(id_sesion=global_vars.identifier)
					results.actividad = Actividad.objects.get(id=id_player)
					results.indicador = Indicador.objects.get(id_indicador=2)
					results.resultado = global_vars.correct
					results.save()
					print("Aciertos")
					print(global_vars.correct)
				if i.id_indicador == 3:
					results = Resultado_Sesion()
					results.sesion = Sesion.objects.get(id_sesion=global_vars.identifier)
					results.actividad = Actividad.objects.get(id=id_player)
					results.indicador = Indicador.objects.get(id_indicador=3)
					results.resultado = global_vars.fail
					results.save()
					print("Fallos")
					print(global_vars.correct)
				if i.id_indicador == 1:
					results = Resultado_Sesion()
					results.sesion = Sesion.objects.get(id_sesion=global_vars.identifier)
					results.actividad = Actividad.objects.get(id=id_player)
					results.indicador = Indicador.objects.get(id_indicador=1)
					results.resultado = round(timefinal,2)
					print("Tiempo")
					print(results.resultado)
					results.save()
			time.sleep(2)
			print("Cerrando juego...")
			global_vars.end = 1


	else:
		for index, obj in enumerate(global_vars.game_objects):
			if "images" == code.split('/')[0]:
				url = obj.imagen.url

				
			elif "songs" == code.split('/')[0] or "movies" == code.split('/')[0]:
				if obj.file:
					url = obj.file.url
					
			url = url[6:]  			# del "files/" of url
			if index == 0:
				global_vars.game_image_prev = ('/%s%s') % (settings.MEDIA_URL,obj.contenido.multimedia.imagen.url[6:])

				if obj.contenido.codigo == code: 		# Match OK
					global_vars.match = 1
					global_vars.game_success +=1
					global_vars.correct = global_vars.game_success
					global_vars.game_objects.remove(obj)
					global_vars.last_message = global_vars.message
					matching = True
					global_vars.message_alert = "alert-success"
					global_vars.game_image = ('/%s%s') % (settings.MEDIA_URL,obj.contenido.multimedia.imagen.url[6:])
					if obj.contenido.multimedia.file:
						global_vars.game_file = obj.contenido.multimedia.file.url
						#music = os.path.abspath('') + '/appQRMusical/'
						#music = music + global_vars.game_file
						#print(music)
						#print(global_vars.failsong)
						music = '/home/pi/Desktop/RFIDMusic/appQRMusical/' + global_vars.game_file
						pygame.mixer.init()
						pygame.mixer.music.load(os.path.abspath(music))
						pygame.mixer.music.play()
					else:
						global_vars.game_file = None
						#music = os.path.abspath('') + '/appQRMusical/files/songs/success.wav'
						music = '/home/pi/Desktop/RFIDMusic/appQRMusical/files/songs/success.wav'
						pygame.mixer.init()
						pygame.mixer.music.load(os.path.abspath(music))
						pygame.mixer.music.play()

		
		if global_vars.last_message != global_vars.message and matching == False: # Doesnt match
			global_vars.game_fail += 1
			global_vars.fail = global_vars.game_fail
			global_vars.last_message = global_vars.message
			global_vars.message_alert = "alert-danger"
			#music = os.path.abspath('') + '/appQRMusical/files/songs/fail.mp3'
			music = '/home/pi/Desktop/RFIDMusic/appQRMusical/files/songs/fail.mp3'
			pygame.mixer.init()
			pygame.mixer.music.load(os.path.abspath(os.path.abspath(music)))
			pygame.mixer.music.play()
		
#Vista que se llama desde el juego para comprobar aciertos/fallos lectura de codigo con el tiempo

def match_game(request, id_player):
	global_vars.cam = 0
	global_vars.rfid_code='No code read'
	global_vars.message = 'Put the card near the reader'
	global_vars.last_message = global_vars.message
	global_vars.message_alert = "alert-info"
	global_vars.game_image = "/files/static/Who.png"
	global_vars.game_image = ""
	global_vars.game_file = ""
	global_vars.game_display = "none"


	player = Actividad.objects.get(id=id_player)
	profile = Paciente.objects.get(online="si")
	global_vars.time = datetime.now()
	start_reader()

	treat = Tratamiento.objects.filter(paciente_id=profile.id)
	treat = treat.filter(activado=True)
		
	for i in treat:
		if  Asigna_Terapia.objects.filter(tratamiento_id=i.id):
			tera = Asigna_Terapia.objects.filter(tratamiento_id=i.id)

	for i in tera:
		asgn_thera = tera.get(id_asign_therapy=i.id_asign_therapy)

	thera_indi=list()
	for i in player.indicador.all():
		thera_indi.append(i)

	gamem(id_player,asgn_thera,thera_indi)

	context = {'message_alert' : global_vars.message_alert}	
	context['image'] = global_vars.game_image
	context['image_prev'] = global_vars.game_image_prev
	context['check'] = global_vars.match
	context['file'] = global_vars.game_file
	context['message_text'] = global_vars.message
	context['title'] = "%s Player Game" % player.nombre
	context['subtitle'] = "Search the correct card!!"
	context['id_player'] = id_player
	context['player_name'] = profile.nombre
	context['name_player'] = player.nombre
	context['game_fail'] = global_vars.game_fail
	context['game_success'] = global_vars.game_success
	context['game_points'] = global_vars.game_points
	context['game_number_objects'] = global_vars.game_number_objects
	context['game_display'] = global_vars.game_display
	context['player'] = profile
	context['correct'] = global_vars.correct
	context['fails'] = global_vars.fail
	context['game_time'] = global_vars.time
	
	return render(request, 'match_game.html', context)

#Vista que se llama desde el html del juego para la actualizacion de estado

def match_game_matching(request, id_player):
        player = Actividad.objects.get(id=id_player)
        profile = Paciente.objects.get(online="si")
        global_vars.time = datetime.now()
        #start_reader()

        #print(global_vars.message)
        treat = Tratamiento.objects.filter(paciente_id=profile.id)
        treat = treat.filter(activado=True)
	
        for i in treat:
            if  Asigna_Terapia.objects.filter(tratamiento_id=i.id):
                tera = Asigna_Terapia.objects.filter(tratamiento_id=i.id)

        for i in tera:
            asgn_thera = tera.get(id_asign_therapy=i.id_asign_therapy)

        thera_indi=list()
        for i in player.indicador.all():
            thera_indi.append(i)

        gamem(id_player,asgn_thera,thera_indi)

        context = {'message_alert' : global_vars.message_alert}
        context['image'] = global_vars.game_image  
        context['file'] = global_vars.game_file
        context['message_text'] = global_vars.message
        context['title'] = "%s Player Game" % player.nombre
        context['subtitle'] = "Select a list of songs"
        context['id_player'] = id_player
        context['name_player'] = player.nombre
        context['game_fail'] = global_vars.game_fail
        context['game_success'] = global_vars.game_success
        context['game_time'] = global_vars.time
        context['game_points'] = global_vars.game_points
        context['game_number_objects'] = global_vars.game_number_objects
        context['game_display'] = global_vars.game_display
        #if global_vars.match == 1:
        context['url'] = reverse('match_game', args=(id_player,)) if global_vars.game_image else None
        #else:
         #   None
        #os.system('wmctrl -r zbar barcode reader -b add,above')

        return JsonResponse(context)


# ======== Login zone ========

#Vista para el inicio de sesión de los especialistas

def Login(request):    
	context = {
		'message_alert' : 	'alert-info',
		'message_head'	:	'Info!',
		'QRM_color' : "QRM_blue",
		'message_text'	:	'Sign in form access to settings.',
	}

	if request.method == 'POST':

		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				login(request, user)
				context['message_alert'] = "alert-success"
				context['message_head'] = "Success! "
				context['message_text'] = "The user <%s> is active." % username
				return HttpResponseRedirect('/settings/')

			else:
				context['message_alert'] = "alert-danger"
				context['message_head'] = "Error, "
				context['message_text'] = "The account-user %s is disable." % username		
		else:
			context['message_alert'] = "alert-danger"
			context['message_head'] = "Error, "
			context['message_text'] = "Username or pass incorrects: {0}".format(username)			

	return render(request, 'login.html', context)  

#Cierra sesion del usuario Especialista o administrador conectado

@login_required
def Logout(request):
    logout(request)
    context = {
		'QRM_color' : "QRM_blue",
    }
    return render(request, 'home.html', context)  
    return HttpResponseRedirect('/')


# ======== Settings zone ========

#Vista de la pantalla principal de las opciones

class Settings(LoginRequiredMixin, TemplateView):
	template_name="settings.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	def get_context_data(self, **kwargs):
		context = super(Settings, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		return context

#Vista para la pantalla de creación de actividades, lista y categorias

class Game_settings(LoginRequiredMixin, TemplateView):
	template_name="game_settings.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	def get_context_data(self, **kwargs):
		context = super(Game_settings, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		return context

#Vista para las opciones de los indicadores, asociar actividad y terapia y acceder a más opciones de actividad

class Activity_settings(LoginRequiredMixin, TemplateView):
	template_name="activity_settings.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	def get_context_data(self, **kwargs):
		context = super(Activity_settings, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		return context

#Vista de los Indicadores existentes en el sistema

class Lista_Indicadores(LoginRequiredMixin, ListView):
	model = Actividad
	template_name="indicators_list.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	def get_context_data(self, **kwargs):
		context = super(Lista_Indicadores, self).get_context_data(**kwargs)
		context['Activities'] = Actividad.objects.all
		context['QRM_color'] = "QRM_orange"
		return context

#Vista de las Terapias existentes en el sistema

class Terapia_player_list(LoginRequiredMixin, ListView):
	model = Terapia_Actividad
	template_name="therapy_player_list.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	def get_context_data(self, **kwargs):
		context = super(Terapia_player_list, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		context['title'] = "Terapia-Activities"
		context['activities'] = Actividad.objects.all()
		return context

#Vista de los contenidos Multimedia existentes en el sistema

class Gallery(LoginRequiredMixin, ListView):
	model = Multimedia
	template_name="gallery.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	def get_context_data(self, **kwargs):
		context = super(Gallery, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		context['message_alert'] = "alert-info"
		context['message_head'] = "Info, "
		context['message_text'] = "Setting of the gallery."
		context['title'] = "Gallery"
		context['subtitle'] = "Configure your app"
		context['actividad_contenido'] = Actividad_Contenido.objects.all()
		return context

#Vista del detalle de los elementos Multimedia

class Multimedia_detail(LoginRequiredMixin, DetailView):
	model = Multimedia
	template_name = "multimedia_detail.html"
	login_url='/login/'
	redirect_field_name = "/login/"

	def get_context_data(self, **kwargs):
		context = super(Multimedia_detail, self).get_context_data(**kwargs)
		if self.object.file:
			url = str(self.object.file.url)
		else:  # If there are not file and only exists image:
			url = str(self.object.imagen.url)

		url = url[6:] # Deleting 'files/'
		
		if not os.path.exists('appQRMusical/files/temp/'):
			os.mkdir('appQRMusical/files/temp/')
		
		qrencode_command = "qrencode %s -o appQRMusical/files/temp/temp.png -s 6" % (url)
		context['qr'] = os.popen(qrencode_command)

		if context['qr']:
			print("QR code of %s make it!" % self.object.nombre)

		context['QRM_color'] = "QRM_orange"
		context['title'] = "QR code"
		context['subtitle'] = "QR of multimedia %s" % self.object.nombre

		img_thumb = square_thumbnail(self.object.imagen.path)
		imgQR = img_QR("appQRMusical/files/temp/temp.png")
		join_thumbnails(img_thumb, imgQR)

		return context
	

def square_thumbnail(url):
	thumb_size =300, 300

	img = Image.open(url)
	width, height = img.size

	if width > height:
		delta = width - height
		left = int(delta/2)
		upper = 0
		right = height + left
		lower = height
	else:
		delta = height - width
		left = 0
		upper = int(delta/2)
		right = width
		lower = width + upper

	img = img.crop((left, upper, right, lower))
	img.thumbnail(thumb_size)
	img = img.resize((300,300))
	return img

def img_QR(url):
	imgQR = Image.open(url)
	imgQR = imgQR.resize((300,300))
	imgQR = imgQR.convert('RGB')
	return imgQR


def join_thumbnails(img, imgQR):
	canvas = Image.new('RGB',(600,300))
	canvas.paste(img,(0,0))
	canvas.paste(imgQR,(300,0))
	canvas.save(settings.MEDIA_ROOT+"/temp/img_QR.jpg")

#Vista para la subida de archivos Multimedia a la aplicación

@login_required(login_url='login')
def upload_multimedia(request):

	context = {
		'QRM_color': "QRM_blue",
		'message_alert' : 	'alert-info',
		'message_head'	:	'Info, ',
		'message_text'	:	'Selecciona un fichero y pulsa subir.',
	}

	if request.method == 'POST':
		context['form'] = UploadMultimediaForm(request.POST, request.FILES)
		if context['form'].is_valid():
			file_up = Multimedia()
			files = request.FILES
			data = request.POST
			success_url = '/settings/gallery'
			file_up.imagen = files['imagen']

			if 'file' in files:
				file_up.file = files['file']
				file_up.name = file_up.file.name
			else:
				file_up.file = None
				file_up.name = file_up.imagen.name

			nombre, ext = file_up.name.rsplit('.', 1)
			file_up.nombre = nombre
			file_up.filetype = ext
			file_up.save()

			#if 'players' in dict(request.POST.iterlists()):
			#	file_up.players = dict((request.POST))['players']

			context['message_alert'] = "alert-success"
			context['message_head'] = "Conseguido! "
			context['message_text'] = "Fichero \"%s\" subido con exito, pulse atras para volver a la pantalla anterior " % (file_up.nombre)

	else:
		context['form'] = UploadMultimediaForm()

	return render(request, 'upload.html', context)	

#Vista para la actualización de multimedia existente

class Multimedia_update(LoginRequiredMixin, UpdateView):
	model = Multimedia
	form_class = UploadMultimediaForm
	template_name = 'upload.html'
	login_url='/login/'
	redirect_field_name = "/login/"

	def get_success_url(self):
		return reverse('multimedia_update', kwargs={'pk': self.object.id_contenido})

#Vista para la eliminacion de multimedia existente

class Multimedia_delete(DeleteView):
	model = Multimedia
	success_url = '/settings/gallery'
	def get_object(self):
		obj = super(Multimedia_delete, self).get_object()

		if obj.file:
			path_file = join_url_with_media_root(obj.file.url)
			os.remove(path_file)

		path_image = join_url_with_media_root(obj.image.url)
		os.remove(path_image)
		return obj			


def join_url_with_media_root(url):
	url = url[6:] # del 'files/'....
	path = os.path.join(settings.MEDIA_ROOT+'%s' % url)
	return path

#Vista de las Actividades existentes en el sistema

class Actividads_list(LoginRequiredMixin, ListView):
	model = Actividad
	template_name="players_list.html"
	login_url='/login/'
	redirect_field_name = "/login/"

	def get_context_data(self, **kwargs):
		context = super(Actividads_list, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		context['categoria'] = Categoria_Actividad.objects.all()
		return context

#Vista de loss Usuarios existentes en el sistema

class Users_list(LoginRequiredMixin, ListView):
	model = Paciente
	template_name="users_list.html"
	login_url='/login/'
	redirect_field_name = "/login/"

	def get_context_data(self, **kwargs):
		context = super(Users_list, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		context['title'] = "Users"
		nacimiento = Paciente.objects.all()#Calculamos la edad de los pacientes
		for i in nacimiento:
			if i.edad == None:
				i.edad = (date.today().year - i.fecha_de_nacimiento.year - ((date.today().month, date.today().day) < (i.fecha_de_nacimiento.month, i.fecha_de_nacimiento.day))) 
				i.save()
		return context

#Vista de los Tratamientos existentes en el sistema

def Tratamientos_list(request):
	model = Tratamiento
	req = request.user.id
	thera = Especialista.objects.get(user_id=req)
	sup = Supervisa.objects.filter(especialista_id=thera)
	#for i in sup:
		#sup1 = sup.objects.get(id=i)
		#wanted_id = sup.treatment_id
	#treatments = Tratamiento.objects.filter(id=sup.treatment.id)
	template_name="treatments_list.html"
	login_url='/login/'
	redirect_field_name = "/login/"

	context = {
	'QRM_color' : "QRM_orange",
	'object_list' : Tratamiento.objects.all(),
	'thera' : thera,
    'supervise' :  Supervisa.objects.all()
	}
	return render(request,'treatments_list.html',context)

#Vista de las Terapias existentes en el sistema

def Therapies_list(request):
	req = request.user.id
	thera = Especialista.objects.get(user_id=req)
	asig_t = Especialista_Asigna_Terapia.objects.filter(especialista_id=thera)
	template_name="therapies_list.html"
	login_url='/login/'
	redirect_field_name = "/login/"

	context = {
	'QRM_color' : "QRM_orange",
	'object_list' : Terapia.objects.all(),
	'asign_therapy' : Especialista_Asigna_Terapia.objects.all(),
    'asign' : asig_t
	}
	return render(request,'therapies_list.html',context)

#Vista del resumen general de las relaciones dentro del sistema

def Summary(request):

	template_name="treatments_list.html"
	login_url='/login/'
	redirect_field_name = "/login/"

	context = {
	'QRM_color' : "QRM_orange",
	'patients' : Paciente.objects.all(),
	'treatments' : Tratamiento.objects.all(),
	'therapies' : Asigna_Terapia.objects.all(),
	'activities' : Terapia_Actividad.objects.all()
	}
	return render(request,'summary.html',context)

#Vista de los Especialistas existentes en el sistema

@login_required(login_url='login')
def Especialistas_list(request):
	template_name="therapists_list.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	context = {
		'QRM_color': "QRM_orange",
		'thera_list' : Especialista.objects.all(),
		'admin' : request.user.is_staff
	}
	return render(request,'therapists_list.html',context)

#Vista para crear Especialistas en el sistema

class Create_therapist(LoginRequiredMixin, CreateView):
	model = Paciente
	form_class = FormularioEspecialista
	template_name="create_therapist.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	success_url = reverse_lazy('therapists_list')

	def get_context_data(self, **kwargs):
		context = super(Create_therapist, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		context['message_alert'] = "alert-info"
		context['message_head'] = "Info, "
		context['message_text'] = "Setting player's game."
		context['title'] = "Create Player"
		context['subtitle'] = "Create your player"
		context['btn_label'] = "Create"
		return context

#Vista de los Pacientes existentes en el sistema

class Create_user(LoginRequiredMixin, CreateView):
	model = Paciente
	form_class = UploadUserForm
	template_name="user_detail.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	success_url = reverse_lazy('users_list')

	def get_context_data(self, **kwargs):
		context = super(Create_user, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		return context

#Vista para actualizar los Pacientes del sistema

class Update_user(LoginRequiredMixin, UpdateView):
	model = Paciente
	form_class = UploadUserForm
	template_name="user_detail.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	success_url = reverse_lazy('users_list')

	def get_context_data(self, **kwargs):
		context = super(Update_user, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		context['image'] = Paciente.objects.get(id=self.object.id)
		context['user_id'] = self.object.id
		return context

#Vista para eliminar Pacientes del sistema

class User_delete(DeleteView):
	model = Paciente
	success_url = '/settings/users_list/'
	def get_object(self):
		obj = super(User_delete, self).get_object()
		return obj	

#Vista para eliminar las terapias asociadas con actividades en el sistema

class Delete_therapy_player(DeleteView):
	model = Terapia_Actividad
	success_url = '/settings/Activities/therapy-player/'
	def get_object(self):
		obj = super(Delete_therapy_player, self).get_object()
		return obj	

#Vista para eliminar  del sistema la tarjeta asociada con un jugador

def ID_delete(request, pk):
    model = get_object_or_404(Paciente, pk=pk)
    model.codigo = ''
    model.save()
    context = {
        'QRM_color' : "QRM_orange",
        'message_alert' : "alert-info",
        'message_head' : "Info, ",
        'message_text' : "Informacion actualizada.",
        'title' : "Actualiza los Ususarios",
        'subtitle' : "Actualiza y configura tu usuario",
        'btn_label' : 'Actualiza',
        'source' : '/files/static/success.png'
        }
    return render(request,'user_ID.html',context)

#Vista para asociar del sistema la tarjeta asociada con un jugador

def User_ID(request, pk):
    model = get_object_or_404(Paciente, pk=pk)
    users = Paciente.objects.all()
    cards = Multimedia.objects.all()
    code = Identify_ID()

    context = {
        'QRM_color' : "QRM_orange",
        'message_alert' : "alert-info",
        'message_head' : "Info, ",
        'message_text' : "La información se ha actualizado correctamente.",
        'title' : "Info",
        'subtitle' : "TERMINADO CON EXITO!!",
        'btn_label' : 'Actualizar',
        'source' : '/files/static/success.png'
        }
    for i in users:
        if i.codigo == code:
            context = {
                'QRM_color' : "QRM_orange",
                'message_alert' : "alert-info",
                'message_head' : "Info, ",
                'message_text' : "No se ha podido actualizar la información.",
                'title' : "Info",
                'subtitle' : "EL CODIGO USADO YA ESTA EN USO, PRUEBE UNO NUEVO",
                'btn_label' : 'Actualizar',
                'source' : '/files/static/error.png'
            }
            return render(request,'user_ID.html',context)

    for i in cards:
        if i.codigo == code:
            context = {
                'QRM_color' : "QRM_orange",
                'message_alert' : "alert-info",
                'message_head' : "Info, ",
                'message_text' : "No se ha podido actualizar la información.",
                'title' : "Info",
                'subtitle' : "EL CODIGO USADO YA ESTA EN USO ASOCIADO CON UN ARCHIVO MULTIMEDIA, PRUEBE UNO NUEVO.",
                'btn_label' : 'Actualizar',
                'source' : '/files/static/error.png'
            }
            return render(request,'user_ID.html',context)
     
    model.codigo = code
    model.save()
    return render(request,'user_ID.html',context)

#Vista que elimina un tarjeta con su elemento multimedia

def Multi_ID_delete(request, pk):
    model = get_object_or_404(Multimedia, pk=pk)
    model.codigo = ''
    model.save()
    context = {
        'QRM_color' : "QRM_orange",
        'message_alert' : "alert-info",
        'message_head' : "Info, ",
        'message_text' : "Informacion actualizada.",
        'btn_label' : 'Actualizar',
        'source' : '/files/static/success.png'
        }
    return render(request,'card_ID.html',context)

#Vista que vincula un tarjeta con su elemento multimedia

def Multi_ID(request, pk):
    model = get_object_or_404(Multimedia, pk=pk)
    users = Paciente.objects.all()
    cards = Multimedia.objects.all()
    code = Identify_ID()

    context = {
        'QRM_color' : "QRM_orange",
        'message_alert' : "alert-info",
        'message_head' : "Info, ",
        'message_text' : "La información se ha actualizado correctamente.",
        'title' : "Info View",
        'subtitle' : "TASK DONE!!",
        'btn_label' : 'Actualizar',
        'source' : '/files/static/success.png'
        }
    for i in cards:
        if i.codigo == code:
            context = {
                'QRM_color' : "QRM_orange",
                'message_alert' : "alert-info",
                'message_head' : "Info, ",
                'message_text' : "No se ha podido actualizar la información.",
                'title' : "Info",
                'subtitle' : "EL CODIGO USADO YA ESTA EN USO ASOCIADO CON UN ARCHIVO MULTIMEDIA, PRUEBE UNO NUEVO.",
                'btn_label' : 'Actualizar',
                'source' : '/files/static/error.png'
            }
            return render(request,'card_ID.html',context)

    for i in users:
        if i.codigo == code:
            context = {
                'QRM_color' : "QRM_orange",
                'message_alert' : "alert-info",
                'message_head' : "Info, ",
                'message_text' : "No se ha podido actualizar la información.",
                'title' : "Info",
                'subtitle' : "EL CODIGO USADO YA ESTA EN USO ASOCIADO CON UN USUARIO, PRUEBE UNO NUEVO.",
                'btn_label' : 'Actualizar',
                'source' : '/files/static/error.png'
            }   
            return render(request,'card_ID.html',context)
    
    model.codigo = code
    model.save()
    return render(request,'card_ID.html',context)

#Vista que vincula una Categoría con una Actividad

class Add_category_player(LoginRequiredMixin, CreateView):
	model = Categoria_Actividad
	form_class = FormularioCategoriaActividad
	template_name="playerc_detail.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	success_url = reverse_lazy('players_list')

	def get_context_data(self, **kwargs):
		context = super(Add_category_player, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		return context

#Vista que vincula una Terapia con una Actividad

class Add_therapy_player(LoginRequiredMixin, CreateView):
	model = Terapia_Actividad
	form_class = UploadTherapyFormActividad
	template_name="therapy_player_detail.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	success_url = reverse_lazy('therapy_player')

	def get_context_data(self, **kwargs):
		context = super(Add_therapy_player, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		return context

#Vista que crea una Actividad

def Create_player(request):
	context = {
		'QRM_color'		: "QRM_blue"
	}
	if request.method == 'POST':
		context['form'] = FormularioActividad(request.POST)
		context['form1'] = UploadIndicatorForm(request.POST)
		context['form2'] = UploadOnePlayerTerapiaForm(request.POST)
		if context['form'].is_valid() & context['form1'].is_valid() & context['form2'].is_valid():
#			indi = Player_Indicator()
			act = Actividad()
			TA = Terapia_Actividad()
			act = context['form'].save(commit=False)
			act = context['form1'].save(commit=False)
			TA = context['form2'].save(commit=False)
			act.nombre = context['form'].cleaned_data['nombre']
			act.descripcion = context['form'].cleaned_data['descripcion']
			act.proposito = context['form'].cleaned_data['proposito']
			act.save()
			indi = context['form1'].cleaned_data['indicador']
			terapia = context['form2'].cleaned_data['terapia']

			print(terapia)
			asigna_indi = Indicador.objects.filter(pk__in=indi)
			#asigna_tera = Terapia.objects.filter(pk__in=terapia)
			print(asigna_indi)
			if indi:
				for i in asigna_indi:
					act.indicador.add(i)
			if terapia:
				TA.actividad = act
				TA.terapia = terapia
				TA.save()
			context['object_list'] = Actividad.objects.all()
			return render(request, 'players_list.html', context)
	else:
		context['form'] = FormularioActividad()
		context['form1'] = UploadIndicatorForm()
		context['form2'] = UploadOnePlayerTerapiaForm ()
	return render(request, 'create_player.html', context)

#Vista que actualiza una Actividad

class Update_player(LoginRequiredMixin, UpdateView):
	model = Actividad
	form_class = FormularioActividad
	template_name="player_detail.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	success_url = reverse_lazy('players_list')

	def get_context_data(self, **kwargs):
		context = super(Update_player, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		context['therapy'] = Terapia_Actividad.objects.filter(actividad_id=self.object.id)
		context['indicators'] = Indicador.objects.all()
		#context['playerindicators'] = Actividad_Indicador.objects.filter(player_id=self.object.id)
		context['activities'] = Actividad_Contenido.objects.filter(actividad_id=self.object.id)
		context['player_id'] = self.object.id
		return context


#Vista que elimina una Actividad

class Actividad_delete(DeleteView):
	model = Actividad
	success_url = '/settings/players_list/'
	def get_object(self):
		obj = super(Actividad_delete, self).get_object()
		return obj	

#Vista que crea un Indicador

class Create_indicator(LoginRequiredMixin, CreateView):
	model = Actividad
	form_class = UploadIndicatorForm
	template_name="indicator_details.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	success_url = reverse_lazy('indicators_list')

	def get_context_data(self, **kwargs):
		context = super(Create_indicator, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		return context

#Vista que actualiza un Indicador

class Update_indicator(LoginRequiredMixin, UpdateView):
	model = Actividad
	form_class = UploadIndicatorForm
	template_name = 'indicator_details.html'
	login_url='/login/'
	redirect_field_name = "/login/"

	def get_success_url(self):
		return reverse('indicators_list')

#Vista que elimina un Indicador

class Indicador_delete(DeleteView):
	model = Indicador
	success_url = '/settings/activities/indicators'
	def get_object(self):
		obj = super(Indicador_delete, self).get_object()
		return obj


class Multimedia_delete(DeleteView):
	model = Multimedia
	success_url = '/settings/gallery'
	def get_object(self):
		obj = super(Multimedia_delete, self).get_object()

		if obj.file:
			path_file = join_url_with_media_root(obj.file.url)
			os.remove(path_file)

		path_image = join_url_with_media_root(obj.image.url)
		os.remove(path_image)
		return obj	

#Vista que crea un Tratamiento

def Create_treatment(request):
	context = {
		'message_alert' : 'alert-info',
		'message_head' : 'Info!',
		'message_text' : 'Create a Tratamiento.',
		'QRM_color'	: "QRM_blue"
	}

	if request.method == 'POST':
		context['form'] = UploadTreatmentForm(request.POST)
		context['form1'] = UploadAsignTherapyForm(request.POST)
		if context['form'].is_valid() & context['form1'].is_valid():
			supervise = Supervisa()
			asigna = Asigna_Terapia()
			req = request.user.id
			thera = Especialista.objects.get(user_id=req)
			Tratamiento = context['form'].save(commit=False)
#			Asigna_Terapia = context['form1'].save(commit=False)
			terapia = context['form1'].cleaned_data['terapia']
			#print(terapia)
			asigna_list = Terapia.objects.filter(pk__in=terapia)
			Tratamiento.paciente = context['form'].cleaned_data['paciente']
			Tratamiento.nombre = context['form'].cleaned_data['nombre']
			Tratamiento.fecha_inicio = context['form'].cleaned_data['fecha_inicio']
			Tratamiento.fecha_fin = context['form'].cleaned_data['fecha_fin']
			Tratamiento.descripcion = context['form'].cleaned_data['descripcion']
			Tratamiento.activado = context['form'].cleaned_data['activado']
			Tratamiento.save()
			supervise.tratamiento = Tratamiento
			supervise.especialista = thera
			supervise.save()
			if terapia:
				asigna.tratamiento = Tratamiento
				asigna.save()
				for i in asigna_list:
					asigna.terapia.add(i)
					#asigna.terapia = i
					#asigna.save()
			return render(request, 'settings.html', context)

	else:
		context['form'] = UploadTreatmentForm()
		context['form1'] = UploadAsignTherapyForm()
	return render(request, 'treatment_details.html', context)

#Vista que actualiza un Tratamiento

class Update_treatment(LoginRequiredMixin, UpdateView):
	model = Tratamiento
	form_class = UploadTreatmentForm
	template_name="treatment_details.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	success_url = reverse_lazy('treatments_list')

	def get_context_data(self, **kwargs):
		context = super(Update_treatment, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		return context

#Vista que elimina un Tratamiento

class Tratamiento_delete(DeleteView):
	model = Tratamiento
	success_url = '/settings/treatments_list/'
	def get_object(self):
		obj = super(Tratamiento_delete, self).get_object()
		return obj	

#Vista que crea una Terapia

def Create_therapy(request):

	context = {
		'QRM_color'	: "QRM_blue" 
	}

	if request.method == 'POST':
		context['form'] = UploadTherapyForm(request.POST)
		context['form1'] = UploadOneActividadTherapyForm(request.POST)
		context['form2'] = UploadAsign(request.POST)
		if context['form'].is_valid() & context['form1'].is_valid() & context['form2'].is_valid():
			TAT = Especialista_Asigna_Terapia()
			req = request.user.id
			tera = Terapia()
			thera = Especialista.objects.get(user_id=req)
			tera = context['form'].save(commit=False)
			Terapia_Actividad = context['form1'].save(commit=False)
			Asigna_Terapia = context['form2'].save(commit=False)
			tera.paciente = context['form'].cleaned_data['nombre']
			tera.description = context['form'].cleaned_data['descripcion']
			tera.tipo = context['form'].cleaned_data['tipo']
			tera.save()
			Terapia_Actividad.terapia = tera
			Terapia_Actividad.actividad = context['form1'].cleaned_data['actividad']
			tratamiento = context['form2'].cleaned_data['tratamiento']
			print(Terapia_Actividad.terapia)
			if tratamiento:
				Asigna_Terapia.tratamiento = tratamiento
				Asigna_Terapia.save()
				Asigna_Terapia.terapia.add(tera)
				TAT.asigna_terapia = Asigna_Terapia
				TAT.especialista = thera
				print(TAT)
				TAT.save()
			try:
				Terapia_Actividad.actividad
				Terapia_Actividad.save()
			except:
				context['message_alert'] = 'alert-success'
				context['message_head'] = 'Success!!. '
				context['message_text'] = 'Changes saved successfully'

			context['object_list'] = Terapia.objects.all()
			context['asign_therapy'] = Especialista_Asigna_Terapia.objects.all()
			return render(request, 'therapies_list.html', context)
	else:
		context['form'] = UploadTherapyForm()
		context['form1'] = UploadOneActividadTherapyForm()
		context['form2'] = UploadAsign()
	return render(request, 'therapy_details.html', context)

#Vista que actualiza una Terapia

class Update_therapy(LoginRequiredMixin, UpdateView):
	model = Terapia
	form_class = UploadTherapyForm
	template_name="therapy_details.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	success_url = reverse_lazy('therapies_list')

	def get_context_data(self, **kwargs):
		context = super(Update_therapy, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		return context

#Vista que elimina una Terapia

class Terapia_delete(DeleteView):
	model = Terapia
	success_url = '/settings/therapies_list/'
	def get_object(self):
		obj = super(Terapia_delete, self).get_object()
		return obj	

#Vista que muestra la lista de Categorias presentes en el sistema

class Categories_list(LoginRequiredMixin, ListView):
	model = Categoria
	template_name="categories_list.html"
	login_url='/login/'
	redirect_field_name = "/login/"

	def get_context_data(self, **kwargs):
		context = super(Categories_list, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		context['message_alert'] = "alert-info"
		context['message_head'] = "Info, "
		context['message_text'] = "Actual list of categories."
		context['title'] = "Categories"
		context['subtitle'] = "Configure your app"
		return context

#Vista que crea una Categoría

class Create_category(LoginRequiredMixin, CreateView):
	model = Categoria
	form_class = UploadCategoryForm
	template_name="category_details.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	success_url = reverse_lazy('categories_list')

	def get_context_data(self, **kwargs):
		context = super(Create_category, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		context['message_alert'] = "alert-info"
		context['message_head'] = "Info, "
		context['message_text'] = "Creating a category."
		context['title'] = "Create a category"
		context['subtitle'] = "Create your Categories"
		context['btn_label'] = "Create"
		return context

#Vista que actualiza una Categoría

class Update_category(LoginRequiredMixin, UpdateView):
	model = Categoria
	form_class = UploadCategoryForm
	template_name = 'category_details.html'
	login_url='/login/'
	redirect_field_name = "/login/"

	def get_success_url(self):
		return reverse('categories_list')

#Vista que elimina una Categoría

class Categoria_delete(DeleteView):
	model = Categoria
	success_url = '/settings/Categories'
	def get_object(self):
		obj = super(Categoria_delete, self).get_object()
		return obj

#Vista que muestra la lista de Diagnósticos presentes en el sistema

def Diagnostico_list(request, pk):
	login_url='/login/'
	redirect_field_name = "/login/"
	context = {
		'QRM_color' : "QRM_orange",
		'ide' : pk,
		'object_list' : Diagnostico.objects.filter(paciente_id=pk),
	}
	return render(request, 'diagnostic_list.html', context)

#Vista que crea un Diagnóstico

@login_required(login_url='login')
def Create_diagnostic(request, pk):
	context = {
		'QRM_color' :"QRM_blue",
		'message_alert' : 'alert-info',
		'message_head' : 'Info!',
		'message_text' : 'Create a Tratamiento.' 
	}
	profile = Paciente.objects.get(id=pk)

	if request.method == 'POST':
		context['form'] = UploadDiagnosticForm(request.POST)
		if context['form'].is_valid():
			diagnostic = Diagnostico()
			diagnostic.paciente = profile
			diagnostic.valoracion = context['form'].cleaned_data['valoracion']
			diagnostic.notas = context['form'].cleaned_data['notas']
			diagnostic.save()
			context['message_alert'] = 'alert-success'
			context['message_head'] = 'Success!!. '
			context['object_list'] = Diagnostico.objects.filter(paciente_id=pk)
			return render(request, 'diagnostic_list.html', context)
	else:
		context['form'] = UploadDiagnosticForm()
	return render(request, 'diagnostic.html', context)

#Vista que actualiza un Diagnóstico

class Update_diagnostic(LoginRequiredMixin, UpdateView):
	model = Diagnostico
	form_class = UploadDiagnosticForm
	template_name="diagnostic.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	success_url = reverse_lazy('users_list')

	def get_context_data(self, **kwargs):
		context = super(Update_diagnostic, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		return context

#Vista que elimina un Diagnóstico

class Delete_diagnostic(DeleteView):
	model = Diagnostico
	success_url = reverse_lazy('users_list')
	def get_object(self):
		obj = super(Delete_diagnostic, self).get_object()
		return obj	

#Vista que muestra el contenido disponible para vincular con la actividad

@login_required(login_url='login')
def add_multimedia_to_player(request, id):
	objs = Actividad.objects.filter(id=id)
	listcont = Actividad_Contenido.objects.filter(actividad_id=id)
	content = Contenido.objects.all()
	content1 = list(content)
	for obj in content:
		for i in listcont:
			if i.contenido.id_contenido == obj.id_contenido:
				content1.remove(obj)
	context = { 
		'object_list' 	:content1,
		'object_list1' 	:listcont,
		'title' 		: objs[0],
		'activities'    : objs,
		'subtitle'		: "Add Contenido to the Activity %s" % objs[0],
		'QRM_color'		: "QRM_orange",
		'player_id'		: id
		}

	return render(request, 'add_multimedia_to_player.html', context)	

#Vista que vincula el contenido seleccionado con una actividad

@login_required(login_url='login')
def add_multimedia_to_player_function(request, id_player, id_multimedia):
	player_to_add = Actividad.objects.get(id=id_player)
	mults = Contenido.objects.get(id_contenido=id_multimedia)
	new_content = Actividad_Contenido()
	new_content.actividad = player_to_add
	new_content.contenido = mults
	new_content.save()

	objs = Actividad.objects.filter(id=id_player)

	context = { 
		'object_list' 	: Actividad_Contenido.objects.exclude(actividad_id=id_player),
		'title' 		: objs[0],
		'subtitle'		: "Add Contenido to the Activity %s" % objs[0],
		'QRM_color'		: "QRM_orange",
		'player_id'		: id_player
		}
	return HttpResponseRedirect('/settings/players_list/%s/update/' % id_player)

#Vista que elimina el contenido asociado con una actividad

@login_required(login_url='login')
def del_multimedia_of_player_function(request, id_player, id_multimedia):
	player_to_del = Actividad.objects.get(id=id_player)
	mults = Actividad_Contenido.objects.filter(contenido_id=id_multimedia)
	mults = mults.get(actividad_id=id_player)
	mults.delete()

	objs = Actividad.objects.filter(id=id_player)

	context = { 
		'object_list' 	:Actividad_Contenido.objects.exclude(actividad_id=id_player),
		'title' 		: objs[0],
		'subtitle'		: "Add songs to Player %s" % objs[0],
		'QRM_color'		: "QRM_orange",
		}

	return HttpResponseRedirect('/settings/players_list/%s/update/' % id_player)

#Vista que muestra las opciones del especialista (cambiar nombre,apellido, contraseña o email)

class User(LoginRequiredMixin, TemplateView):
	template_name="user.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	success_url = reverse_lazy('user')
	def get_context_data(self, **kwargs):
		context = super(User, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"	
		return context

#Vista que muestra la lista de pacientes para seleccionar y ver sus Resultados

class Resultados(LoginRequiredMixin, ListView):
	template_name="results.html"
	model = Paciente
	login_url='/login/'
	redirect_field_name = "/login/"
	success_url = reverse_lazy('settings')
	def get_context_data(self, **kwargs):
		context = super(Resultados , self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"		
		return context

#Vista que muestra la lista de las tratamiento para el paciente seleccionado y ver sus Resultados

def ResultadosTratamiento(request, pk):
	objects = Tratamiento.objects.filter(paciente__id=pk)
	context = {
		'QRM_color' : "QRM_orange",
		'objects' : objects,
		'paciente' : Paciente.objects.get(pk=pk)
	}	
	return render(request, 'results_treatment.html', context) 

#Vista que muestra la lista de Resultados para el tratamiento especificada

def Resultados_details(request, pk):

	objects_treat = Tratamiento.objects.filter(id=pk)
	objects = Resultado_Sesion.objects.filter(sesion_id__in=Sesion.objects.filter(asigna_Terapia__tratamiento__in=objects_treat))
	success = objects.filter(indicador_id=2)
	fail = objects.filter(indicador_id=3)
	timing = objects.filter(indicador_id=1)
	print(success)
	print(fail)
	print(timing)
	context = {
		'QRM_color' : "QRM_orange",
		'message_alert' : "alert-info",
		'message_head' : "Info, ",
		'message_text' : "Resultado table.",
		'title' : "Resultados",
		'success' : success,
		'failures' : fail,
		'time' : timing,
		#'data' : data,
		'objects_treat' : objects_treat,
		'objects' : objects,
		'subtitle' : "Add the data that you want"
	}	
	return render(request, 'results_details.html', context)  

#Vista para cambiar el Nombre y el Apellido del especialista

@login_required(login_url='login')
def edit_name(request):
	context = {
		'QRM_color'		: "QRM_blue",
	}

	if request.method == 'POST':
		context['form'] = EditNameForm(request.POST, request=request)
		if context['form'].is_valid():
			req = request.user.id
			therapist = Especialista.objects.get(user_id=req)
			request.user.first_name = context['form'].cleaned_data['name']
			request.user.last_name = context['form'].cleaned_data['surname']
			therapist.nombre = context['form'].cleaned_data['name']
			therapist.apellido = context['form'].cleaned_data['surname']
			request.user.save()
			therapist.save()
			context['QRM_color'] ="QRM_blue"
			context['thera_list'] = Especialista.objects.all()
			context['admin'] = request.user.is_staff
			return render(request, 'therapists_list.html', context)
	else:
		context['form'] = EditNameForm(
		request=request,
		initial={'name': request.user.first_name,'surname': request.user.last_name})
	return render(request, 'userForms.html', context)

#Vista para cambiar el Email del especialista

@login_required(login_url='login')
def edit_email(request):
	context = {
		'QRM_color'		: "QRM_blue",
	}

	if request.method == 'POST':
		context['form'] = EditEmailForm(request.POST, request=request)
		if context['form'].is_valid():
			req = request.user.id
			therapist = Especialista.objects.get(user_id=req)
			request.user.email = context['form'].cleaned_data['email']
			therapist.email = context['form'].cleaned_data['email']
			request.user.save()
			therapist.save()
			context['QRM_color'] ="QRM_blue"
			context['thera_list'] = Especialista.objects.all()
			context['admin'] = request.user.is_staff
			return render(request, 'therapists_list.html', context)
	else:
		context['form'] = EditEmailForm(
		request=request,
		initial={'email': request.user.email})
	return render(request, 'userForms.html', context)

#Vista para cambiar la Contraseña del especialista

@login_required(login_url='login')
def edit_password(request):
	context = {
		'QRM_color'		: "QRM_blue",
	}	

	if request.method == 'POST':
		context['form'] = EditPassForm(request.POST)
		if context['form'].is_valid():
			request.user.password = make_password(context['form'].cleaned_data['password'])
			request.user.save()
	else:
		context['form'] = EditPassForm()
	return render(request, 'userForms.html', context) 
