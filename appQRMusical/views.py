# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, DeleteView, UpdateView, CreateView
from datetime import datetime, time

#Users
from django.contrib.auth.models import User

# Login
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

# Settings
from django.contrib.auth.mixins import LoginRequiredMixin

# Play + Multimedia
from .models import Player#, Game_List
from . import global_vars

# Multimedia
from .models import Multimedia, Content, Player_Content
import os
from PIL import Image
from django.conf import settings
from django.views.generic.edit import FormView
from .forms import UploadMultimediaForm

# Player
from .models import Player, Player_Indicator
from .forms import UploadPlayerForm#UploadMatchListForm
from django.urls import reverse_lazy, reverse

# Profile
from .models import Profile
from .forms import UploadUserForm

# Therapist
from .models import Therapist
from .forms import UploadTherapistForm

# Therapy
from .models import Therapy, Asign_Therapy, Therapist_Asign_Therapy, Therapy_Player
from .forms import UploadTherapyForm, UploadAsignForm, UploadTherapyPlayerForm

# Treatment
from .models import Treatment, Supervise
from .forms import UploadTreatmentForm

# Diagnostic
from .models import Diagnostic
from .forms import UploadDiagnosticForm

# Indicator
from .models import Indicator, Therapy_Indicator
from .forms import UploadIndicatorForm

# Category
from .models import Category, Category_Player
from .forms import UploadCategoryForm, UploadCategoryPlayerForm

#Session
from .models import Session, Result_Session

#Player Game
import threading
import subprocess
#import RPi.GPIO as GPIO
import time
#GPIO.setmode(GPIO.BOARD)

# Card reader
import sys, time, serial
from pygame import mixer
serialPort ='/dev/ttyACM0'

# User Settings
from .forms import EditNameForm, EditEmailForm, EditPassForm
from django.contrib.auth.hashers import make_password

from django.http import JsonResponse



def read_ID():
    arduinoPort = serial.Serial(serialPort, 9600, timeout=1)
    code = 0

    while True:
        tag = arduinoPort.readline()
        code = tag.decode('utf-8')
        if hash(tag) != 0:
            #arduinoPort.close()
            if len(code)==8:
                global_vars.message = code
                arduinoPort.flushInput()
            else:
                arduinoPort.flushInput()



def start_reader():
    #global_vars.message = 'Put the card near the scanner'
    t1 = threading.Thread(target=read_ID)
    t1.start()

def Identify_ID():
    arduinoPort = serial.Serial(serialPort, 9600, timeout=1)
    arduinoPort.setDTR(False)
    time.sleep(0.3)

    arduinoPort.flushInput()
    arduinoPort.setDTR()
    time.sleep(0.3)
    code = 0

    while True:
        tag = arduinoPort.readline()
        code = tag.decode('utf-8')
        if hash(tag) != 0:
            if len(code)==8:
                arduinoPort.close()
                return code

# Create your views here.
class Home(TemplateView):
	template_name="home.html"
	#start_reader()
	def get_context_data(self, **kwargs):
		context = super(Home, self).get_context_data(**kwargs)
		try:
			player = Profile.objects.get(online="yes")
			context['subtitle'] = "Willkommen, Bienvenue, Benvenuti, Bienvenido, Namaste, karibu. Let's go to play!!"
		except Profile.DoesNotExist:
			player = None
			context['subtitle'] = "Willkommen, Bienvenue, Benvenuti, Bienvenido, Namaste, karibu. Identify a user and let's go to play!!"

		context['QRM_color'] = "QRM_blue"
		context['message_alert'] = "alert-info"
		context['message_head'] = "Info, "
		context['message_text'] = "welcome to PiMusic project, made by Iñaki."
		context['title'] = "Welcome!"
		context['player'] = player
		return context


# ======== PLAY zone ========
class Play(TemplateView):
	template_name="play.html"
	model = Player.objects.all()
	def get_context_data(self, **kwargs):
		context = super(Play, self).get_context_data(**kwargs)
<<<<<<< HEAD
		try:
			player = Profile.objects.get(online="yes")
		except Profile.DoesNotExist:
			player = None
			return context
=======
		player = Profile.objects.get(online="yes")
>>>>>>> 095192f6faba87468904e961a719516f910b185f

		content = list()
		skip = 1
		terapy = Therapy.objects.all()
		tera2 = Treatment.objects.filter(enabled=True)
		tera2 = Asign_Therapy.objects.filter(treatment_id__in=tera2.filter(profile_id=player.id))
		for i in tera2:
			for j in terapy:
				if i.therapy.id == j.id:
					content.append(j)
					skip = 0

		#tera2 = Therapy_Player.objects.filter(therapy_id__in=Therapy.objects.filter(id__in=Asign_Therapy.objects.filter(treatment_id__in=tera2)))

		context['treat'] = tera2
		context['therapy_p'] = Therapy_Player.objects.all()
		context['kk'] = content
		context['skip'] = skip
		context['QRM_color'] = "QRM_pink"
		context['message_alert'] = "alert-info"
		context['message_head'] = "Info, "
		context['message_text'] = "Select a game."
		context['title'] = "Play"
		context['subtitle'] = "Select between the different games"
<<<<<<< HEAD
		context['player'] = player
=======
>>>>>>> 095192f6faba87468904e961a719516f910b185f
		return context


class Songs(ListView):
	model = Player
	template_name="songs_list.html"
	def get_context_data(self, **kwargs):
		context = super(Songs, self).get_context_data(**kwargs)
		context.update({
			'object_list': Player.objects.all().filter(list_type="Music_list"),
		})
		context['QRM_color'] = "QRM_pink"
		context['message_alert'] = "alert-info"
		context['message_head'] = "Info, "
		context['message_text'] = "Select a songs list."
		context['title'] = "Interactive player list"
		context['subtitle'] = "Select a list of songs"
		return context

class List(ListView):
	model = Player
	template_name="matchs_list.html"
	def get_context_data(self, **kwargs):
		context = super(List, self).get_context_data(**kwargs)
		context.update({
			'object_list': Player.objects.all().filter(list_type="Match_list"),
		})
		context['QRM_color'] = "QRM_pink"
		context['message_alert'] = "alert-info"
		context['message_head'] = "Info, "
		context['message_text'] = "Select a list to play."
		context['title'] = "Interactive match list"
		context['subtitle'] = "Select a list to play"
		return context

class Match(TemplateView):
	template_name="match_view.html"


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

def Identify(request):
	#template_name="home.html"
	#coder = global_vars.rfid_code
	coder = Identify_ID()
	#global_vars.rfid_code = ''
	try:
		user = Profile.objects.get(code=coder)
		user.online = "yes"
		user.save()
		context = {
			'QRM_color' : "QRM_blue",
			'message_alert' : "alert-info",
			'message_head' : user.name,
			'message_text' : "is ready to play",
			'title' : "User identified",
			'subtitle' : "Click on Play to begin!!",
			'player' : user
    	}
<<<<<<< HEAD
		return HttpResponseRedirect('/play/')
=======
		return render(request, 'home.html', context)		
>>>>>>> 095192f6faba87468904e961a719516f910b185f
	except:
		user = None
		context = {
			'QRM_color' : "QRM_blue",
			'message_alert' : "alert-info",
			'message_head' : "No User with this ID",
			'message_text' : ", Please try another one",
			'title' : "No User Found",
			'subtitle' : "Click on Identify Player to try again",
			'player' : user
    	}	

	return render(request, 'info.html', context)

<<<<<<< HEAD
def Disconnect(request):
	try:
		user = Profile.objects.get(online="yes")
		user.online = "no"
		user.save()
		context = {
			'QRM_color' : "QRM_blue",
			'message_alert' : "alert-info",
			'message_head' : user.name,
			'message_text' : "Has just disconnect",
			'title' : "User disconnected",
			'subtitle' : "Click on Identify Player to register another player!!",
			'player' : user
	    }
		return render(request, 'home.html', context)
	except Profile.DoesNotExist:
		user = None
		context = {
			'QRM_color' : "QRM_blue",
	    }		

=======
def Disconnect(request, pk):
	#template_name="hom
	user = get_object_or_404(Profile, pk=pk)
	user.online = "no"
	user.save()
	context = {
		'QRM_color' : "QRM_blue",
		'message_alert' : "alert-info",
		'message_head' : user.name,
		'message_text' : "Has just disconnect",
		'title' : "User disconnected",
		'subtitle' : "Click on Identify Player to register another player!!",
		'player' : user
    }		
>>>>>>> 095192f6faba87468904e961a719516f910b185f
	return render(request, 'home.html', context)

def game(id_player):
	if global_vars.game_initialized == False: 	# First start of game
		#mults = Multimedia.objects.filter(players__in=Player.objects.filter(id = id_player))
		global_vars.game_number_objects = mults.count()
		mults = list(mults)
		global_vars.game_objects = mults
		global_vars.game_initialized = True

	url=""
	qrcode = global_vars.message[:-1] # del "\n" in end

	matching = False


	if global_vars.game_success == global_vars.game_number_objects:
		global_vars.game_display = "inline"

	else:
		for obj in global_vars.game_objects:
			if "images" == qrcode.split('/')[0]:
				url = obj.image.url
				
			elif "songs" == qrcode.split('/')[0] or "movies" == qrcode.split('/')[0]:
				if obj.file:
					url = obj.file.url
					
			url = url[6:]  			# del "files/" of url
			os.system('wmctrl -r zbar barcode reader -b add,above')
			
			if url == qrcode: 		# Match OK
				global_vars.game_success +=1
				global_vars.game_objects.remove(obj)
				global_vars.last_message = global_vars.message
				matching = True
				global_vars.message_alert = "alert-success"
				global_vars.game_image = ('/%s%s') % (settings.MEDIA_URL,obj.image.url[6:])
				if obj.file:
					global_vars.game_file = obj.file.url
				else:
					global_vars.game_file = None
				buzzer = Buzzer(8)						# Init Buzzer
				blink(5, .05, 5)	# nTimes, speed, pin
				buzzer.play(1)		# 1 --> Sucess melody
		
		if global_vars.last_message != global_vars.message and matching == False: # Doesnt match
			global_vars.game_fail += 1
			global_vars.last_message = global_vars.message
			global_vars.message_alert = "alert-danger"
			buzzer = Buzzer(8)						# Init Buzzer
			blink(5, .05, 7)	# nTimes, speed, pin
			buzzer.play(2)		# 1 --> Sucess melody
	


def gamem(id_player,asgn_thera,thera_indi):
	indis = Player_Indicator.objects.filter(player_id=id_player)

	if global_vars.game_initialized == False: 	# First start of game
		mults = Player_Content.objects.filter(player_id=id_player)
		global_vars.game_number_objects = mults.count()
		mults = list(mults)
		global_vars.game_objects = mults
		global_vars.game_initialized = True
		sessionone = Session()
		sessionone.asign_therapy = asgn_thera
		sessionone.save()
		global_vars.identifier = sessionone.id_session
		global_vars.thera_indi = thera_indi
		global_vars.timestart =time.time()

	

	global_vars.match = 0
	url=""
	code = global_vars.message# del "\n" in end

	matching = False


	if global_vars.game_success == global_vars.game_number_objects:
		global_vars.game_display = "inline"
		#timestart = global_vars.time
		global_vars.timeend =  time.time()
		timefinal = global_vars.timeend - global_vars.timestart
		results = Result_Session()
		for i in global_vars.thera_indi:
			if i.indicator.id_indicator == 1:
				results.session = Session.objects.get(id_session=global_vars.identifier)
				results.player = Player.objects.get(id=id_player)
				results.indicator = Indicator.objects.get(id_indicator=1)
				results.result = timefinal
				results.save()
			if i.indicator.id_indicator == 2:
				results.session = Session.objects.get(id_session=global_vars.identifier)
				results.player = Player.objects.get(id=id_player)
				results.indicator = Indicator.objects.get(id_indicator=2)
				results.result = global_vars.correct
				results.save()
			if i.indicator.id_indicator == 3:
				results.session = Session.objects.get(id_session=global_vars.identifier)
				results.player = Player.objects.get(id=id_player)
				results.indicator = Indicator.objects.get(id_indicator=3)
				results.result = global_vars.fail
				results.save()


		#global_vars.time = time

	else:
		for index, obj in enumerate(global_vars.game_objects):
			if "images" == code.split('/')[0]:
				url = obj.image.url

				
			elif "songs" == code.split('/')[0] or "movies" == code.split('/')[0]:
				if obj.file:
					url = obj.file.url
					
			url = url[6:]  			# del "files/" of url
			#os.system('wmctrl -r zbar barcode reader -b add,above')
			if index == 0:
				global_vars.game_image_prev = ('/%s%s') % (settings.MEDIA_URL,obj.content.multimedia.image.url[6:])

				if obj.content.code == code: 		# Match OK
					global_vars.match = 1
					global_vars.game_success +=1
					global_vars.correct = global_vars.game_success
					global_vars.game_objects.remove(obj)
					global_vars.last_message = global_vars.message
					matching = True
					global_vars.message_alert = "alert-success"
					global_vars.game_image = ('/%s%s') % (settings.MEDIA_URL,obj.content.multimedia.image.url[6:])
					if obj.content.multimedia.file:
						global_vars.game_file = obj.content.multimedia.file.url
					else:
						global_vars.game_file = None
				#buzzer = Buzzer(8)						# Init Buzzer
				#blink(5, .05, 5)	# nTimes, speed, pin
				#buzzer.play(1)		# 1 --> Sucess melody
		
		if global_vars.last_message != global_vars.message and matching == False: # Doesnt match
			global_vars.game_fail += 1
			global_vars.fail = global_vars.game_fail
			global_vars.last_message = global_vars.message
			global_vars.message_alert = "alert-danger"
			#buzzer = Buzzer(8)						# Init Buzzer
			#blink(5, .05, 7)	# nTimes, speed, pin
			#buzzer.play(2)		# 1 --> Sucess melody
				

def player_game_song(request, id_player):
	context = {'message_alert' : global_vars.message_alert}
	if global_vars.game_file != None:
		name, ext = global_vars.game_file.split('.')
		context['extension'] = ext 
	else:
		context['extension'] = None		
	context['image'] = global_vars.game_image
	context['file'] = global_vars.game_file
	context['id_player'] = id_player 

	global_vars.game_file = None
	"""	
	context['message_text'] = global_vars.message
	context['title'] = "%s Player Game" % player.name
	context['subtitle'] = "Select a list of songs"
	context['id_player'] = id_player 
	context['name_player'] = player.name 
	context['game_fail'] = global_vars.game_fail
	context['game_success'] = global_vars.game_success
	context['game_points'] = global_vars.game_points
	context['game_number_objects'] = global_vars.game_number_objects
	context['game_display'] = global_vars.game_display
	"""
	return render(request, 'player_game_song.html', context)

"""
def match_game_image(request, id_player):
	context = {'message_alert' : global_vars.message_alert}
	if global_vars.game_file != None:
		name, ext = global_vars.game_file.split('.')
		context['extension'] = ext 
	else:
	    context['extension'] = None		
	context['image'] = global_vars.game_image
	context['file'] = global_vars.game_file
	context['id_player'] = id_player 

	global_vars.game_file = None
	
	context['message_text'] = global_vars.message
	context['title'] = "%s Player Game" % player.name
	context['subtitle'] = "Select a list of songs"
	context['id_player'] = id_player 
	context['name_player'] = player.name 
	context['game_fail'] = global_vars.game_fail
	context['game_success'] = global_vars.game_success
	context['game_points'] = global_vars.game_points
	context['game_number_objects'] = global_vars.game_number_objects
	context['game_display'] = global_vars.game_display
	
	return render(request, 'match_game_image.html', context)
"""
		
def player_game(request, id_player):
	global_vars.cam = 0
	global_vars.message = 'Get close QR code to cam'
	global_vars.last_message = global_vars.message
	global_vars.message_alert = "alert-info"
	global_vars.game_image = "/files/static/Who.png"
	global_vars.game_image = ""
	global_vars.game_file = ""
	global_vars.game_display = "none"


	player = Player.objects.get(id=id_player)
	player = Profile.objects.get(online="yes")
	treat = Treatment.objects.filter(profile_id=player.id)
	treat = treat.filter(enabled=True)

		#treat = treat.filter(enabled=True)
		#tera = list()
		#tera2 = list()
		
	for i in treat:
		#tera = Asign_Therapy.objects.filter(treatment_id=i.id)
		if  Asign_Therapy.objects.filter(treatment_id=i.id):
			tera = Asign_Therapy.objects.filter(treatment_id=i.id)
			#itera=itera+1
		#itera = 0
		#tera2 = Therapy.objects.filter(id__in=tera.filter(treatment_id=tera.treatment_id)

	for i in tera:
		if  Therapy.objects.filter(id=i.treatment_id) != None:
			tera2 = Therapy.objects.filter(id=i.treatment_id)

	terapy = Therapy_Player.objects.all()
	for i in tera2:
		for j in terapy:
			if i.id == j.therapy.id:
				asgn_thera = i.get.all()
				therapyid = j.therapy.id

	thera_indi = Player_Indicator.objects.filter(player_id=id_player)
	start_cam()

	print(global_vars.message)

	game(id_player,asgn_thera,thera_indi)

	context = {'message_alert' : global_vars.message_alert}	
	context['image'] = global_vars.game_image
	context['file'] = global_vars.game_file
	context['message_text'] = global_vars.message
	context['title'] = "%s Player Game" % player.name
	context['subtitle'] = "Select a list of songs"
	context['id_player'] = id_player 
	context['name_player'] = player.name 
	context['game_fail'] = global_vars.game_fail
	context['game_success'] = global_vars.game_success
	context['game_points'] = global_vars.game_points
	context['game_number_objects'] = global_vars.game_number_objects
	context['game_display'] = global_vars.game_display
	
	return render(request, 'player_game.html', context)

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


	player = Player.objects.get(id=id_player)
	profile = Profile.objects.get(online="yes")
	global_vars.time = datetime.now()
	start_reader()

	#print(global_vars.message)
	print(global_vars.thera_indi)
	treat = Treatment.objects.filter(profile_id=profile.id)
	treat = treat.filter(enabled=True)
		
	for i in treat:
		if  Asign_Therapy.objects.filter(treatment_id=i.id):
			tera = Asign_Therapy.objects.filter(treatment_id=i.id)

	for i in tera:
		asgn_thera = tera.get(id_asign_therapy=i.id_asign_therapy)

	thera_indi = Player_Indicator.objects.filter(player_id=id_player)
	gamem(id_player,asgn_thera,thera_indi)

	context = {'message_alert' : global_vars.message_alert}	
	context['image'] = global_vars.game_image
	context['image_prev'] = global_vars.game_image_prev
	context['check'] = global_vars.match
	context['file'] = global_vars.game_file
	context['message_text'] = global_vars.message
	context['title'] = "%s Player Game" % player.name
	context['subtitle'] = "Search the correct card!!"
	context['id_player'] = id_player
	context['player_name'] = profile.name
	context['name_player'] = player.name 
	context['game_fail'] = global_vars.game_fail
	context['game_success'] = global_vars.game_success
	context['game_points'] = global_vars.game_points
	context['game_number_objects'] = global_vars.game_number_objects
	context['game_display'] = global_vars.game_display
<<<<<<< HEAD
	context['player'] = profile
=======
	#context['game_time'] = time.time() - global_vars.time
>>>>>>> 095192f6faba87468904e961a719516f910b185f
	context['correct'] = global_vars.correct
	context['fails'] = global_vars.fail
	
	return render(request, 'match_game.html', context)


def player_game_matching(request, id_player):

        player = Player.objects.get(id=id_player)
        profile = Profile.objects.get(online="yes")
        treat = Treatment.objects.filter(profile_id=profile.id)
        treat = treat.filter(enabled=True)
		
        for i in treat:
            if  Asign_Therapy.objects.filter(treatment_id=i.id):
                tera = Asign_Therapy.objects.filter(treatment_id=i.id)

        for i in tera:
            asgn_thera = tera.get(id_asign_therapy=i.id_asign_therapy)

        thera_indi = Therapy_Indicator.objects.filter(therapy_id=asgn_thera.therapy.id)
        start_cam()

        game(id_player,asgn_thera,thera_indi)

        context = {'message_alert' : global_vars.message_alert}
        context['image'] = global_vars.game_image  
        context['file'] = global_vars.game_file
        context['message_text'] = global_vars.message
        context['title'] = "%s Player Game" % player.name
        context['subtitle'] = "Select a list of songs"
        context['id_player'] = id_player
        context['name_player'] = player.name
        context['game_fail'] = global_vars.game_fail
        context['game_success'] = global_vars.game_success
        context['game_points'] = global_vars.game_points
        context['game_number_objects'] = global_vars.game_number_objects
        context['game_display'] = global_vars.game_display
        context['url'] = reverse('player_game_song', args=(id_player,)) if global_vars.game_image else None
        os.system('wmctrl -r zbar barcode reader -b add,above')

        return JsonResponse(context)

def match_game_matching(request, id_player):

        player = Player.objects.get(id=id_player)

        gamem(id_player,1,1)

        context = {'message_alert' : global_vars.message_alert}
        context['image'] = global_vars.game_image  
        context['file'] = global_vars.game_file
        context['message_text'] = global_vars.message
        context['title'] = "%s Player Game" % player.name
        context['subtitle'] = "Select a list of songs"
        context['id_player'] = id_player
        context['name_player'] = player.name
        context['game_fail'] = global_vars.game_fail
        context['game_success'] = global_vars.game_success
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
def Login(request):    
	context = {
		'message_alert' : 	'alert-info',
		'message_head'	:	'Info!',
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


@login_required
def Logout(request):
    logout(request)
    context = {
<<<<<<< HEAD
		'QRM_color' : "QRM_blue",
=======
>>>>>>> 095192f6faba87468904e961a719516f910b185f
    	'message_alert' : 	'alert-success',
    	'message_head'	:	'Success!',
    	'message_text'	:	'User logout correctly.',
    }
<<<<<<< HEAD
    return render(request, 'home.html', context)  
=======
    return HttpResponseRedirect('/')
>>>>>>> 095192f6faba87468904e961a719516f910b185f


# ======== Settings zone ========
class Settings(LoginRequiredMixin, TemplateView):
	template_name="settings.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	def get_context_data(self, **kwargs):
		context = super(Settings, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		context['message_alert'] = "alert-info"
		context['message_head'] = "Info, "
		context['message_text'] = "Select one to configure."
		context['title'] = "Settings"
		context['subtitle'] = "Configure your app"
		return context


class Game_settings(LoginRequiredMixin, TemplateView):
	template_name="game_settings.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	def get_context_data(self, **kwargs):
		context = super(Game_settings, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		context['message_alert'] = "alert-info"
		context['message_head'] = "Info, "
		context['message_text'] = "Select a list to configure it."
		context['title'] = "Game Settings"
		context['subtitle'] = "Configure your Games"
		return context

class Activity_settings(LoginRequiredMixin, TemplateView):
	template_name="activity_settings.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	def get_context_data(self, **kwargs):
		context = super(Activity_settings, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		context['message_alert'] = "alert-info"
		context['message_head'] = "Info, "
		context['message_text'] = "Select a manage activities or indicators to configure it."
		context['title'] = "Activity Settings"
		context['subtitle'] = "Configure your Activities"
		return context

class Indicators_list(LoginRequiredMixin, ListView):
	model = Player_Indicator
	template_name="indicators_list.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	def get_context_data(self, **kwargs):
		context = super(Indicators_list, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		context['message_alert'] = "alert-info"
		context['message_head'] = "Info, "
		context['message_text'] = "List of indicators."
		context['title'] = "Indicators"
		context['subtitle'] = "Configure your indicators"
		return context

class Therapy_player_list(LoginRequiredMixin, ListView):
	model = Therapy_Player
	template_name="therapy_player_list.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	def get_context_data(self, **kwargs):
		context = super(Therapy_player_list, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		context['message_alert'] = "alert-info"
		context['message_head'] = "Info, "
		context['message_text'] = "List of Therapies associated with activities."
		context['title'] = "Therapy-Activities"
		context['subtitle'] = "Configure your Therapies-Activities"
		return context

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
		context['player_content'] = Player_Content.objects.all()
		return context


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
			url = str(self.object.image.url)

		url = url[6:] # Deleting 'files/'
		
		if not os.path.exists('appQRMusical/files/temp/'):
			os.mkdir('appQRMusical/files/temp/')
		
		qrencode_command = "qrencode %s -o appQRMusical/files/temp/temp.png -s 6" % (url)
		context['qr'] = os.popen(qrencode_command)

		if context['qr']:
			print("QR code of %s make it!" % self.object.name)

		context['QRM_color'] = "QRM_orange"
		context['title'] = "QR code"
		context['subtitle'] = "QR of multimedia %s" % self.object.name

		img_thumb = square_thumbnail(self.object.image.path)
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


@login_required(login_url='login')
def upload_multimedia(request):

	context = {
		'message_alert' : 	'alert-info',
		'message_head'	:	'Info, ',
		'message_text'	:	'Select a File, and press Upload.',
	}

	if request.method == 'POST':
		context['form'] = UploadMultimediaForm(request.POST, request.FILES)
		if context['form'].is_valid():
			file_up = Multimedia()
			files = request.FILES
			data = request.POST
			file_up.image = files['image']

			if 'file' in files:
				file_up.file = files['file']
				file_up.name = file_up.file.name
			else:
				file_up.file = None
				file_up.name = file_up.image.name

			name, ext = file_up.name.rsplit('.', 1)
			file_up.name = name
			file_up.filetype = ext
			file_up.save()

			#if 'players' in dict(request.POST.iterlists()):
			#	file_up.players = dict((request.POST))['players']

			context['message_alert'] = "alert-success"
			context['message_head'] = "Success! "
			context['message_text'] = "File \"%s\" upload success" % (file_up.name)

	else:
		context['form'] = UploadMultimediaForm()

	return render(request, 'upload.html', context)	


class Multimedia_update(LoginRequiredMixin, UpdateView):
	model = Multimedia
	form_class = UploadMultimediaForm
	template_name = 'upload.html'
	login_url='/login/'
	redirect_field_name = "/login/"

	def get_success_url(self):
		return reverse('multimedia_update', kwargs={'pk': self.object.id_content})


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


class Players_list(LoginRequiredMixin, ListView):
	model = Player
	template_name="players_list.html"
	login_url='/login/'
	redirect_field_name = "/login/"

	def get_context_data(self, **kwargs):
		context = super(Players_list, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		context['message_alert'] = "alert-info"
		context['message_head'] = "Info, "
		context['message_text'] = "Setting player's game."
		context['title'] = "Players"
		context['category'] = Category_Player.objects.all()
		context['subtitle'] = "Configure your app"
		return context

class Match_list(LoginRequiredMixin, ListView):
	model = Player
	template_name="players_list.html"
	login_url='/login/'
	redirect_field_name = "/login/"

	def get_context_data(self, **kwargs):
		context = super(Match_list, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		context['message_alert'] = "alert-info"
		context['message_head'] = "Info, "
		context['message_text'] = "Settings for match list."
		context['title'] = "Lists"
		context['subtitle'] = "Configure your app"
		return context


class Users_list(LoginRequiredMixin, ListView):
	model = Profile
	template_name="users_list.html"
	login_url='/login/'
	redirect_field_name = "/login/"

	def get_context_data(self, **kwargs):
		context = super(Users_list, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		context['message_alert'] = "alert-info"
		context['message_head'] = "Info, "
		context['message_text'] = "Actual list of Users."
		context['title'] = "Users"
		context['subtitle'] = "Configure your app"
		return context

def Treatments_list(request):
	#model = Treatment
	req = request.user.id
	thera = Therapist.objects.get(user_id=req)
	sup = Supervise.objects.filter(therapist_id=thera)
	#for i in sup:
		#sup1 = sup.objects.get(id=i)
		#wanted_id = sup.treatment_id
	#treatments = Treatment.objects.filter(id=sup.treatment.id)
	template_name="treatments_list.html"
	login_url='/login/'
	redirect_field_name = "/login/"

	context = {
	'QRM_color' : "QRM_orange",
	'message_alert' : "alert-info",
	'message_head' : "Info, ",
	'message_text' : "Actual list of Treatments.",
	'title' : "Treatments",
	'subtitle' : "Configure your Treatments",
	'object_list' : Treatment.objects.all(),
	'thera' : thera,
    'supervise' :  Supervise.objects.all()
	}
	return render(request,'treatments_list.html',context)

def Therapies_list(request):
	req = request.user.id
	thera = Therapist.objects.get(user_id=req)
	asig_t = Therapist_Asign_Therapy.objects.filter(therapist_id=thera)
	template_name="therapies_list.html"
	login_url='/login/'
	redirect_field_name = "/login/"

	context = {
	'QRM_color' : "QRM_orange",
	'message_alert' : "alert-info",
	'message_head' : "Info, ",
	'message_text' : "Actual list of Therapies.",
	'title' : "Therapies",
	'subtitle' : "Configure your Therapies",
	'object_list' : Therapy.objects.all(),
	'asign_therapy' : Therapist_Asign_Therapy.objects.all(),
    'asign' : asig_t
	}
	return render(request,'therapies_list.html',context)

@login_required(login_url='login')
def Therapists_list(request):
	template_name="therapists_list.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	context = {
		'QRM_color': "QRM_orange",
		'message_alert' : "alert-info",
		'message_head' : "Info, ",
		'message_text' : "Actual list of Therapists.",
		'title' : "Therapists",
		'subtitle' : "Configure your app",
		'thera_list' : Therapist.objects.all(),
		'admin' : request.user.is_staff
	}
	return render(request,'therapists_list.html',context)

class Create_therapist(LoginRequiredMixin, CreateView):
	model = Profile
	form_class = UploadTherapistForm
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



class Create_user(LoginRequiredMixin, CreateView):
	model = Profile
	form_class = UploadUserForm
	template_name="user_detail.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	success_url = reverse_lazy('users_list')

	def get_context_data(self, **kwargs):
		context = super(Create_user, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		context['message_alert'] = "alert-info"
		context['message_head'] = "Info, "
		context['message_text'] = "Setting player's game."
		context['title'] = "Create Player"
		context['subtitle'] = "Create your player"
		context['btn_label'] = "Create"
		return context


class Update_user(LoginRequiredMixin, UpdateView):
	model = Profile
	form_class = UploadUserForm
	template_name="user_detail.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	success_url = reverse_lazy('users_list')

	def get_context_data(self, **kwargs):
		context = super(Update_user, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		context['message_alert'] = "alert-info"
		context['message_head'] = "Info, "
		context['message_text'] = "Update the information."
		context['title'] = "Update User"
		context['subtitle'] = "Update and Configure your User"
		#context['songs'] = Multimedia.objects.filter(players__in=[self.object])
		context['btn_label'] = 'Update'
		context['user_id'] = self.object.id
		return context


class User_delete(DeleteView):
	model = Profile
	success_url = '/settings/users_list/'
	def get_object(self):
		obj = super(User_delete, self).get_object()
		return obj	

class Delete_therapy_player(DeleteView):
	model = Therapy_Player
	success_url = '/settings/Activities/therapy-player/'
	def get_object(self):
		obj = super(Delete_therapy_player, self).get_object()
		return obj	


def ID_delete(request, pk):
    model = get_object_or_404(Profile, pk=pk)
    model.code = ''
    model.save()
    context = {
        'QRM_color' : "QRM_orange",
        'message_alert' : "alert-info",
        'message_head' : "Info, ",
        'message_text' : "Update the information.",
        'title' : "Update User",
        'subtitle' : "Update and Configure your User",
        'btn_label' : 'Update',
        'source' : '/files/static/success.png'
        }
    return render(request,'user_ID.html',context)

def User_ID(request, pk):
    model = get_object_or_404(Profile, pk=pk)
    users = Profile.objects.all()
    cards = Multimedia.objects.all()
    code = Identify_ID()

    context = {
        'QRM_color' : "QRM_orange",
        'message_alert' : "alert-info",
        'message_head' : "Info, ",
        'message_text' : "The information was updated succesfully.",
        'title' : "Info View",
        'subtitle' : "TASK DONE!!",
        'btn_label' : 'Update',
        'source' : '/files/static/success.png'
        }
    for i in users:
        if i.code == code:
            context = {
                'QRM_color' : "QRM_orange",
                'message_alert' : "alert-info",
                'message_head' : "Info, ",
                'message_text' : "Couldn't update the information.",
                'title' : "Info View",
                'subtitle' : "THE ID IS ALREADY IN USE, TRY A NEW ONE",
                'btn_label' : 'Update',
                'source' : '/files/static/error.png'
            }
            return render(request,'user_ID.html',context)

    for i in cards:
        if i.code == code:
            context = {
                'QRM_color' : "QRM_orange",
                'message_alert' : "alert-info",
                'message_head' : "Info, ",
                'message_text' : "Couldn't update the information.",
                'title' : "Info View",
                'subtitle' : "THE ID IS ALREADY IN USE IDENTIFYING A MUTIMEDIA FILE, TRY A NEW ONE",
                'btn_label' : 'Update',
                'source' : '/files/static/error.png'
            }
            return render(request,'user_ID.html',context)
     
    model.code = code
    model.save()
    return render(request,'user_ID.html',context)

def Multi_ID_delete(request, pk):
    model = get_object_or_404(Multimedia, pk=pk)
    model.code = ''
    model.save()
    context = {
        'QRM_color' : "QRM_orange",
        'message_alert' : "alert-info",
        'message_head' : "Info, ",
        'message_text' : "Update the information.",
        'title' : "Update Multimedia",
        'subtitle' : "Update and Configure your Multimedia",
        'btn_label' : 'Update',
        'source' : '/files/static/success.png'
        }
    return render(request,'card_ID.html',context)

def Multi_ID(request, pk):
    model = get_object_or_404(Multimedia, pk=pk)
    users = Profile.objects.all()
    cards = Multimedia.objects.all()
    code = Identify_ID()

    context = {
        'QRM_color' : "QRM_orange",
        'message_alert' : "alert-info",
        'message_head' : "Info, ",
        'message_text' : "The information was updated succesfully.",
        'title' : "Info View",
        'subtitle' : "TASK DONE!!",
        'btn_label' : 'Update',
        'source' : '/files/static/success.png'
        }
    for i in cards:
        if i.code == code:
            context = {
                'QRM_color' : "QRM_orange",
                'message_alert' : "alert-info",
                'message_head' : "Info, ",
                'message_text' : "Couldn't update the information.",
                'title' : "Info View",
                'subtitle' : "THE ID IS ALREADY IN USE IN ANOTHER MUTIMEDIA, TRY A NEW ONE",
                'btn_label' : 'Update',
                'source' : '/files/static/error.png'
            }
            return render(request,'card_ID.html',context)

    for i in users:
        if i.code == code:
            context = {
                'QRM_color' : "QRM_orange",
                'message_alert' : "alert-info",
                'message_head' : "Info, ",
                'message_text' : "Couldn't update the information.",
                'title' : "Info View",
                'subtitle' : "THE ID IS ALREADY IN USE IDENTIFYING AN USER, TRY A NEW ONE",
                'btn_label' : 'Update',
                'source' : '/files/static/error.png'
            }   
            return render(request,'card_ID.html',context)
    
    model.code = code
    model.save()
    return render(request,'card_ID.html',context)


class Update_player(LoginRequiredMixin, UpdateView):
	model = Player
	form_class = UploadPlayerForm
	template_name="player_detail.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	success_url = reverse_lazy('players_list')

	def get_context_data(self, **kwargs):
		context = super(Update_player, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		context['message_alert'] = "alert-info"
		context['message_head'] = "Info, "
		context['message_text'] = "Setting player's game."
		context['title'] = "Update the Activity"
		context['subtitle'] = "Update and Configure your activity"
		context['btn_label'] = 'Update'
		context['activities'] = Player_Content.objects.filter(player_id=self.object.id)
		context['player_id'] = self.object.id
		return context

class Add_category_player(LoginRequiredMixin, CreateView):
	model = Category_Player
	form_class = UploadCategoryPlayerForm
	template_name="playerc_detail.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	success_url = reverse_lazy('players_list')

	def get_context_data(self, **kwargs):
		context = super(Add_category_player, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		context['message_alert'] = "alert-info"
		context['message_head'] = "Info, "
		context['message_text'] = "Setting player's game."
		context['title'] = "Update the Activity"
		context['subtitle'] = "Update and Configure your activity"
		context['btn_label'] = 'Update'
		return context

class Add_therapy_player(LoginRequiredMixin, CreateView):
	model = Therapy_Player
	form_class = UploadTherapyPlayerForm
	template_name="therapy_player_detail.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	success_url = reverse_lazy('therapy_player')

	def get_context_data(self, **kwargs):
		context = super(Add_therapy_player, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		context['message_alert'] = "alert-info"
		context['message_head'] = "Info, "
		context['message_text'] = "Setting player's game."
		context['title'] = "Update the Activity"
		context['subtitle'] = "Update and Configure your activity"
		context['btn_label'] = 'Update'
		return context

class Create_player(LoginRequiredMixin, CreateView):
	model = Player
	form_class = UploadPlayerForm
	template_name="create_player.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	success_url = reverse_lazy('players_list')

	def get_context_data(self, **kwargs):
		context = super(Create_player, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		context['message_alert'] = "alert-info"
		context['message_head'] = "Info, "
		context['message_text'] = "Create an activity."
		context['title'] = "Create an Activity"
		context['subtitle'] = "Create your activity"
		context['btn_label'] = "Create"
		return context

class Create_indicator(LoginRequiredMixin, CreateView):
	model = Indicator
	form_class = UploadIndicatorForm
	template_name="indicator_details.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	success_url = reverse_lazy('indicators_list')

	def get_context_data(self, **kwargs):
		context = super(Create_indicator, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		context['message_alert'] = "alert-info"
		context['message_head'] = "Info, "
		context['message_text'] = "Creating an indicator."
		context['title'] = "Create an Indicator"
		context['subtitle'] = "Create your indicators"
		context['btn_label'] = "Create"
		return context

class Update_indicator(LoginRequiredMixin, UpdateView):
	model = Indicator
	form_class = UploadIndicatorForm
	template_name = 'indicator_details.html'
	login_url='/login/'
	redirect_field_name = "/login/"

	def get_success_url(self):
		return reverse('indicators_list')

class Indicator_delete(DeleteView):
	model = Indicator
	success_url = '/settings/activities/indicators'
	def get_object(self):
		obj = super(Indicator_delete, self).get_object()
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

def Create_treatment(request):
	context = {
		'message_alert' : 'alert-info',
		'message_head' : 'Info!',
		'message_text' : 'Create a Treatment.' 
	}

	if request.method == 'POST':
		context['form'] = UploadTreatmentForm(request.POST)
		if context['form'].is_valid():
			supervise = Supervise()
			req = request.user.id
			thera = Therapist.objects.get(user_id=req)
			Treatment = context['form'].save(commit=False)
			Treatment.profile = context['form'].cleaned_data['profile']
			Treatment.start_date = context['form'].cleaned_data['start_date']
			Treatment.end_date = context['form'].cleaned_data['end_date']
			Treatment.description = context['form'].cleaned_data['description']
			Treatment.enabled = context['form'].cleaned_data['enabled']
			Treatment.save()
			supervise.treatment = Treatment
			supervise.therapist = thera
			supervise.save()
			context['message_alert'] = 'alert-success'
			context['message_head'] = 'Success!!. '
			context['message_text'] = 'Changes saved successfully'
	else:
		context['form'] = UploadTreatmentForm()
	return render(request, 'treatment_details.html', context)

class Update_treatment(LoginRequiredMixin, UpdateView):
	model = Treatment
	form_class = UploadTreatmentForm
	template_name="treatment_details.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	success_url = reverse_lazy('treatments_list')

	def get_context_data(self, **kwargs):
		context = super(Update_treatment, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		context['message_alert'] = "alert-info"
		context['message_head'] = "Info, "
		context['message_text'] = "Update the information."
		context['title'] = "Update User"
		context['subtitle'] = "Update and Configure your User"
		context['btn_label'] = 'Update'
		return context

class Treatment_delete(DeleteView):
	model = Treatment
	success_url = '/settings/treatments_list/'
	def get_object(self):
		obj = super(Treatment_delete, self).get_object()
		return obj	

def Create_therapy(request):

	context = {
		'message_alert' : 'alert-info',
		'message_head' : 'Info!',
		'message_text' : 'Create a Therapy.', 
	}

	if request.method == 'POST':
		context['form'] = UploadTherapyForm(request.POST)
		context['form2'] = UploadAsignForm(request.POST)
		if context['form'].is_valid() & context['form2'].is_valid():
			TAT = Therapist_Asign_Therapy()
			req = request.user.id
			thera = Therapist.objects.get(user_id=req)
			Therapy = context['form'].save(commit=False)
			Asign_Therapy = context['form2'].save(commit=False)
			Therapy.profile = context['form'].cleaned_data['name']
			Therapy.description = context['form'].cleaned_data['description']
			Therapy.enabled = context['form'].cleaned_data['therapy_type']
			Therapy.save()
			Asign_Therapy.treatment = context['form2'].cleaned_data['treatment']
			Asign_Therapy.therapy = Therapy
			Asign_Therapy.save()
			TAT.asign_therapy = Asign_Therapy
			TAT.therapist = thera
			TAT.save()
			context['message_alert'] = 'alert-success'
			context['message_head'] = 'Success!!. '
			context['message_text'] = 'Changes saved successfully'
	else:
		context['form'] = UploadTherapyForm()
		context['form2'] = UploadAsignForm()
	return render(request, 'therapy_details.html', context)

class Update_therapy(LoginRequiredMixin, UpdateView):
	model = Therapy
	form_class = UploadTherapyForm
	template_name="therapy_details.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	success_url = reverse_lazy('therapies_list')

	def get_context_data(self, **kwargs):
		context = super(Update_therapy, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		context['message_alert'] = "alert-info"
		context['message_head'] = "Info, "
		context['message_text'] = "Update the information."
		context['title'] = "Update User"
		context['subtitle'] = "Update and Configure your therapy"
		context['btn_label'] = 'Update'
		return context

class Therapy_delete(DeleteView):
	model = Therapy
	success_url = '/settings/therapies_list/'
	def get_object(self):
		obj = super(Therapy_delete, self).get_object()
		return obj	


class Player_delete(DeleteView):
	model = Player
	success_url = '/settings/players_list/'
	def get_object(self):
		obj = super(Player_delete, self).get_object()
		return obj	

def Diagnostic_list(request, pk):
	login_url='/login/'
	redirect_field_name = "/login/"
	context = {
		'QRM_color' : "QRM_orange",
		'message_alert' : "alert-info",
		'message_head' : "Info, ",
		'message_text' : "Actual list of Therapies.",
		'title' : "Therapies",
		'ide' : pk,
		'object_list' : Diagnostic.objects.filter(profile_id=pk),
		'subtitle' : "Configure your Therapies"
	}
	return render(request, 'diagnostic_list.html', context)

class Categories_list(LoginRequiredMixin, ListView):
	model = Category
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

class Create_category(LoginRequiredMixin, CreateView):
	model = Indicator
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

class Update_category(LoginRequiredMixin, UpdateView):
	model = Category
	form_class = UploadCategoryForm
	template_name = 'category_details.html'
	login_url='/login/'
	redirect_field_name = "/login/"

	def get_success_url(self):
		return reverse('category_list')

class Category_delete(DeleteView):
	model = Category
	success_url = '/settings/Categories'
	def get_object(self):
		obj = super(Category_delete, self).get_object()
		return obj



@login_required(login_url='login')
def Create_diagnostic(request, pk):
	context = {
		'message_alert' : 'alert-info',
		'message_head' : 'Info!',
		'message_text' : 'Create a Treatment.' 
	}
	profile = Profile.objects.get(id=pk)

	if request.method == 'POST':
		context['form'] = UploadDiagnosticForm(request.POST)
		if context['form'].is_valid():
			diagnostic = Diagnostic()
			diagnostic.profile = profile
			diagnostic.assesment = context['form'].cleaned_data['assesment']
			diagnostic.notes = context['form'].cleaned_data['notes']
			diagnostic.save()
			context['message_alert'] = 'alert-success'
			context['message_head'] = 'Success!!. '
			context['message_text'] = 'Changes saved successfully'
	else:
		context['form'] = UploadDiagnosticForm()
	return render(request, 'diagnostic.html', context)

class Update_diagnostic(LoginRequiredMixin, UpdateView):
	model = Diagnostic
	form_class = UploadDiagnosticForm
	template_name="diagnostic.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	success_url = reverse_lazy('users_list')

	def get_context_data(self, **kwargs):
		context = super(Update_diagnostic, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		context['message_alert'] = "alert-info"
		context['message_head'] = "Info, "
		context['message_text'] = "Update the information."
		context['title'] = "Update User"
		context['subtitle'] = "Update and Configure your User"
		context['btn_label'] = 'Update'
		return context

class Delete_diagnostic(DeleteView):
	model = Diagnostic
	success_url = reverse_lazy('users_list')
	def get_object(self):
		obj = super(Delete_diagnostic, self).get_object()
		return obj	

@login_required(login_url='login')
def add_multimedia_to_player(request, id):
	objs = Player.objects.filter(id=id)
	listcont = Player_Content.objects.filter(player_id=id)
	content = Content.objects.all()
	content1 = list(content)
	for obj in content:
		for i in listcont:
			if i.content.id_content == obj.id_content:
				content1.remove(obj)
	context = { 
		'object_list' 	:content1,
		'object_list1' 	:listcont,
		'title' 		: objs[0],
		'activities'    : objs,
		'subtitle'		: "Add Content to the Activity %s" % objs[0],
		'QRM_color'		: "QRM_orange",
		'player_id'		: id
		}

	return render(request, 'add_multimedia_to_player.html', context)	


@login_required(login_url='login')
def add_multimedia_to_player_function(request, id_player, id_multimedia):
	player_to_add = Player.objects.get(id=id_player)
	mults = Content.objects.get(id_content=id_multimedia)
	new_content = Player_Content()
	new_content.player = player_to_add
	new_content.content = mults
	new_content.save()

	objs = Player.objects.filter(id=id_player)

	context = { 
		'object_list' 	: Player_Content.objects.exclude(player_id=id_player),
		'title' 		: objs[0],
		'subtitle'		: "Add Content to the Activity %s" % objs[0],
		'QRM_color'		: "QRM_orange",
		'player_id'		: id_player
		}
	return HttpResponseRedirect('/settings/players_list/%s/update/' % id_player)


@login_required(login_url='login')
def del_multimedia_of_player_function(request, id_player, id_multimedia):
	player_to_del = Player.objects.get(id=id_player)
	mults = Player_Content.objects.filter(content_id=id_multimedia)
	mults = mults.get(player_id=id_player)
	mults.delete()

	objs = Player.objects.filter(id=id_player)

	context = { 
		'object_list' 	:Player_Content.objects.exclude(player_id=id_player),
		'title' 		: objs[0],
		'subtitle'		: "Add songs to Player %s" % objs[0],
		'QRM_color'		: "QRM_orange",
		}

	return HttpResponseRedirect('/settings/players_list/%s/update/' % id_player)


@login_required(login_url='login')
def camera(request):    
	cam_width = global_vars.cam_width
	cam_height = global_vars.cam_height
	cam_refresh = global_vars.cam_refresh

	message_alert = 'alert-info'
	message_head = 'Info!'
	message_text = 'Configure the values of camera.' 

	if request.method == 'POST':

		cam_width = request.POST.get('Width')
		cam_height = request.POST.get('Height')
		cam_refresh = request.POST.get('Refresh')

		global_vars.cam_width = cam_width 
		global_vars.cam_height = cam_height
		global_vars.cam_refresh = cam_refresh
		
		message_alert = 'alert-success'
		message_head = 'Success!. '
		message_text = 'Changes saved successfully'

	context = {
		'message_alert' : 	message_alert,
		'message_head'	:	message_head,
		'message_text'	:	message_text,
		'cam_width'		:	cam_width,
		'cam_height'	: 	cam_height,
		'cam_refresh'	: 	cam_refresh,
	}

	return render(request, 'camera.html', context)  


class User(LoginRequiredMixin, TemplateView):
	template_name="user.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	success_url = reverse_lazy('user')
	def get_context_data(self, **kwargs):
		context = super(User, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		context['message_alert'] = "alert-info"
		context['message_head'] = "Info, "
		context['message_text'] = "Edit password or email"
		context['title'] = "User!"
		context['subtitle'] = "Settings in user"		
		return context

class Results(LoginRequiredMixin, ListView):
	template_name="results.html"
	model = Profile
	login_url='/login/'
	redirect_field_name = "/login/"
	success_url = reverse_lazy('settings')
	def get_context_data(self, **kwargs):
		context = super(Results , self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		context['message_alert'] = "alert-info"
		context['message_head'] = "Info, "
		context['message_text'] = "Edit password or email"
		context['title'] = "User!"
		context['subtitle'] = "Settings in user"		
		return context

def Results_details(request, pk):
	#model = Result_Session.objects.filter(session__in=Session.objects.filter(id_session=pk))
	#objects = Treatment()
	#objects = Treatment.objects.filter(profile_id=pk)
	#objects = Asign_Therapy.objects.filter(treatment_id=Treatment.objects.filter(profile_id=pk))
	objects = Result_Session.objects.filter(session_id__in=Session.objects.filter(asign_therapy_id__in=Asign_Therapy.objects.filter(treatment_id__in=Treatment.objects.filter(profile_id=pk))))
	success = objects.filter(indicator_id=2)
	fail = objects.filter(indicator_id=3)
	timing = objects.filter(indicator_id=1)
	context = {
		'QRM_color' : "QRM_orange",
		'message_alert' : "alert-info",
		'message_head' : "Info, ",
		'message_text' : "Result table.",
		'title' : "Results",
		'success' : success,
		'failures' : fail,
		'time' : timing,
		#'data' : data,
		'objects' : objects,
		'subtitle' : "Add the data that you want"
	}	
	return render(request, 'results_details.html', context)  

@login_required(login_url='login')
def edit_name(request):
	context = {
<<<<<<< HEAD
		'QRM_color'		: "QRM_blue",
=======
>>>>>>> 095192f6faba87468904e961a719516f910b185f
		'message_alert' : 'alert-info',
		'message_head' : 'Info!',
		'message_text' : 'Change your name/surname.' 
	}

	if request.method == 'POST':
		context['form'] = EditNameForm(request.POST, request=request)
		if context['form'].is_valid():
			req = request.user.id
			therapist = Therapist.objects.get(user_id=req)
			request.user.first_name = context['form'].cleaned_data['name']
			request.user.last_name = context['form'].cleaned_data['surname']
			therapist.name = context['form'].cleaned_data['name']
			therapist.surname = context['form'].cleaned_data['surname']
			request.user.save()
			therapist.save()
			context['message_alert'] = 'alert-success'
			context['message_head'] = 'Success!!. '
			context['message_text'] = 'Changes saved successfully'
	else:
		context['form'] = EditNameForm(
		request=request,
		initial={'name': request.user.first_name,'surname': request.user.last_name})
	return render(request, 'userForms.html', context)

@login_required(login_url='login')
def edit_email(request):
	context = {
<<<<<<< HEAD
		'QRM_color'		: "QRM_blue",
=======
>>>>>>> 095192f6faba87468904e961a719516f910b185f
		'message_alert' : 'alert-info',
		'message_head' : 'Info!',
		'message_text' : 'Change your mail.' 
	}

	if request.method == 'POST':
		context['form'] = EditEmailForm(request.POST, request=request)
		if context['form'].is_valid():
			req = request.user.id
			therapist = Therapist.objects.get(user_id=req)
			request.user.email = context['form'].cleaned_data['email']
			therapist.email = context['form'].cleaned_data['email']
			request.user.save()
			therapist.save()
			context['message_alert'] = 'alert-success'
			context['message_head'] = 'Success!!. '
			context['message_text'] = 'Changes saved successfully'
	else:
		context['form'] = EditEmailForm(
		request=request,
		initial={'email': request.user.email})
	return render(request, 'userForms.html', context)


@login_required(login_url='login')
def edit_password(request):
	context = {
<<<<<<< HEAD
		'QRM_color'		: "QRM_blue",
=======
>>>>>>> 095192f6faba87468904e961a719516f910b185f
		'message_alert' : 'alert-info',
		'message_head' : 'Info!',
		'message_text' : 'Change your password.' 
	}	

	if request.method == 'POST':
		context['form'] = EditPassForm(request.POST)
		if context['form'].is_valid():
			request.user.password = make_password(context['form'].cleaned_data['password'])
			request.user.save()
			context['message_alert'] = 'alert-success'
			context['message_head'] = 'Success!!. '
			context['message_text'] = 'Changes saved successfully'
	else:
		context['form'] = EditPassForm()
	return render(request, 'userForms.html', context) 
