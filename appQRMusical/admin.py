# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Player, Multimedia, Profile, Therapist, Therapy, Treatment, Asign_Therapy, Therapist_Asign_Therapy, Supervise, Diagnostic, Session, Indicator, Player_Indicator, Therapy_Player, Therapy_Indicator, Result_Session, Category, Category_Player, Content, Text, Player_Content

# Register your models here.
admin.site.register(Player)
admin.site.register(Multimedia)
admin.site.register(Profile)
admin.site.register(Therapist)
admin.site.register(Therapy)
admin.site.register(Treatment)
admin.site.register(Asign_Therapy)
admin.site.register(Therapist_Asign_Therapy)
admin.site.register(Supervise)
admin.site.register(Diagnostic)
admin.site.register(Session)
admin.site.register(Indicator)
admin.site.register(Player_Indicator)
admin.site.register(Therapy_Player)
admin.site.register(Therapy_Indicator)
admin.site.register(Result_Session)
admin.site.register(Category)
admin.site.register(Category_Player)
admin.site.register(Content)
admin.site.register(Text)
admin.site.register(Player_Content)
