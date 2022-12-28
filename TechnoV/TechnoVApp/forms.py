from django import forms
from .models import *

class RegistrationForm(forms.ModelForm):

    class Meta:
        model = Registered
        fields= "__all__"

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields= "__all__"
            
class AdminForm(forms.ModelForm):

    class Meta:
        model = Admin
        fields= "__all__"
        
#include
'''
class RecordsForm(forms.ModelForm):

    class Meta:
        model = dailyRecords
        fields= "__all__"
'''



######################################################################
'''
class GuestsForm(forms.ModelForm):

    class Meta:
        model = Guest
        fields= "__all__"

class DropOffForm(forms.ModelForm):

    class Meta:
        model = DropOff
        fields= "__all__"
'''
