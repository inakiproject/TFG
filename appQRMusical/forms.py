# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from .models import Multimedia, Player, Profile, Therapist, Treatment, Diagnostic, Therapy, Asign_Therapy, Indicator, Content, Category, Category_Player, Player_Indicator, Therapy_Player
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

YEARS= [x for x in range(1990,2021)]

# Create your tests here.

class UploadMultimediaForm(forms.ModelForm):	
	class Meta:
		model = Multimedia
		fields = ['file', 'image']

	def __init__(self, *args, **kwargs):
		super(UploadMultimediaForm, self).__init__(*args, **kwargs)
		self.fields['file'].widget.attrs.update({'class' : 'form-control'})
		self.fields['image'].widget.attrs.update({'class' : 'form-control btn btn-default btn-file'})


class UploadPlayerForm(forms.ModelForm):	
	class Meta:
		model = Player
		fields = ['name', 'description','purpose']

	def __init__(self, *args, **kwargs):
		super(UploadPlayerForm, self).__init__(*args, **kwargs)
		self.fields['name'].widget.attrs.update({'class' : 'form-control'})
		self.fields['description'].widget.attrs.update({'class' : 'form-control'})
		self.fields['purpose'].widget.attrs.update({'class' : 'form-control'})


class UploadUserForm(forms.ModelForm):	
	class Meta:
		model = Profile
		fields = ['name', 'surname','date_of_birth','age','gender','level']

	def __init__(self, *args, **kwargs):
		super(UploadUserForm, self).__init__(*args, **kwargs)
		self.fields['name'].widget.attrs.update({'class' : 'form-control'})
		self.fields['surname'].widget.attrs.update({'class' : 'form-control'})
		self.fields['date_of_birth'].widget=forms.SelectDateWidget(years=YEARS)
		self.fields['age'].widget.attrs.update({'class' : 'form-control'})
		self.fields['level'].widget.attrs.update({'class' : 'selectpicker', 'id' : 'select'})
		self.fields['gender'].widget.attrs.update({'class' : 'selectpicker', 'id' : 'select'})


class UploadTherapistForm(UserCreationForm):
    model = User
    fields = ('username', 'password1', 'password2', )

class UploadTreatmentForm(forms.ModelForm):	
	class Meta:
		model = Treatment
		fields = ['profile', 'start_date','end_date','description','enabled']

	def __init__(self, *args, **kwargs):
		super(UploadTreatmentForm, self).__init__(*args, **kwargs)
		self.fields['profile'].widget.attrs.update({'class' : 'selectpicker', 'id' : 'select'})
		self.fields['start_date'].widget=forms.SelectDateWidget(years=YEARS)
		self.fields['end_date'].widget=forms.SelectDateWidget(years=YEARS)
		self.fields['description'].widget.attrs.update({'class' : 'form-control'})
		self.fields['enabled'].widget.attrs.update({'class' : 'custom-control-input'})

class UploadTherapyForm(forms.ModelForm):	
	class Meta:
		model = Therapy
		fields = ['name','description','therapy_type']

	def __init__(self, *args, **kwargs):
		super(UploadTherapyForm, self).__init__(*args, **kwargs)
		self.fields['name'].widget.attrs.update({'class' : 'selectpicker', 'id' : 'select'})
		self.fields['description'].widget.attrs.update({'class' : 'form-control'})
		self.fields['therapy_type'].widget.attrs.update({'class' : 'custom-control-input'})

class UploadAsignForm(forms.ModelForm):
    class Meta:
        model = Asign_Therapy
        fields = ['treatment']

    def __init__(self, *args, **kwargs):
        super(UploadAsignForm, self).__init__(*args, **kwargs)
        self.fields['treatment'].widget.attrs.update({'class' : 'selectpicker', 'id' : 'select'})

class UploadIndicatorForm(forms.ModelForm):	
	class Meta:
		model = Player_Indicator
		fields = ['player','indicator']

	def __init__(self, *args, **kwargs):
		super(UploadIndicatorForm, self).__init__(*args, **kwargs)
		self.fields['player'].widget.attrs.update({'class' : 'form-control'})
		self.fields['indicator'].widget.attrs.update({'class' : 'form-control'})

class UploadDiagnosticForm(forms.ModelForm):	
	class Meta:
		model = Diagnostic
		fields = ['assesment','notes']

	def __init__(self, *args, **kwargs):
		super(UploadDiagnosticForm, self).__init__(*args, **kwargs)
		self.fields['assesment'].widget.attrs.update({'class' : 'form-control'})
		self.fields['notes'].widget.attrs.update({'class' : 'form-control'})

class UploadCategoryForm(forms.ModelForm):	
	class Meta:
		model = Category
		fields = ['category']

	def __init__(self, *args, **kwargs):
		super(UploadCategoryForm, self).__init__(*args, **kwargs)
		self.fields['category'].widget.attrs.update({'class' : 'form-control'})

class UploadCategoryPlayerForm(forms.ModelForm):	
	class Meta:
		model = Category_Player
		fields = ['player','category']

	def __init__(self, *args, **kwargs):
		super(UploadCategoryPlayerForm, self).__init__(*args, **kwargs)
		self.fields['player'].widget.attrs.update({'class' : 'selectpicker', 'id' : 'select'})
		self.fields['category'].widget.attrs.update({'class' : 'selectpicker', 'id' : 'select'})

class UploadTherapyPlayerForm(forms.ModelForm):	
	class Meta:
		model = Therapy_Player
		fields = ['player','therapy']

	def __init__(self, *args, **kwargs):
		super(UploadTherapyPlayerForm, self).__init__(*args, **kwargs)
		self.fields['player'].widget.attrs.update({'class' : 'selectpicker', 'id' : 'select'})
		self.fields['therapy'].widget.attrs.update({'class' : 'selectpicker', 'id' : 'select'})


class EditNameForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    surname = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        """Get request"""
        self.request = kwargs.pop('request')
        return super(EditNameForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data['name']
        return name
    def clean_surname(self):
        surname = self.cleaned_data['surname']
        return surname

class EditEmailForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        """Get request"""
        self.request = kwargs.pop('request')
        return super(EditEmailForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']
        # Change email?
        last_email = self.request.user.email
        username = self.request.user.username
        if email != last_email:
            # If doesnt exists in BD
            exists = User.objects.filter(email=email).exclude(username=username)
            if exists:
                raise forms.ValidationError('This emails is already registed.')
        return email


class EditPassForm(forms.Form):
    last_password = forms.CharField(
        label='Last password',
        min_length=5,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password = forms.CharField(
        label='New password',
        min_length=5,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password2 = forms.CharField(
        label='Repeat new password',
        min_length=5,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_password2(self):
        """Match pass1 & pass2."""
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('The passwords doesn\'t be equal.')
        return password2
