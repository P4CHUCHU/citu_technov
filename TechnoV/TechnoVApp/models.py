from enum import unique
from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.

class Registered(models.Model):
    #personal data
	idnumber= models.CharField(max_length=50)
	firstname = models.CharField(max_length=50)
	middlename = models.CharField(max_length=50)
	lastname = models.CharField(max_length=50)
	classification = models.CharField(max_length=50)#student/admin/staff/parentOrGuardianRelative
	department = models.CharField(max_length=500)#engineering/IT/elementary/juniorhigh/seniorhigh 
	courseyr = models.CharField(max_length=25)
	Ownerfname = models.CharField(max_length=50)
	Ownermname = models.CharField(max_length=50)
	Ownerlname = models.CharField(max_length=50)
	address = models.CharField(max_length=100)
	mobnum = models.CharField(max_length=50)
	landline = models.CharField(max_length=50)
	relation = models.CharField(max_length=50)#parent/guardian
	identifier = models.CharField(max_length=25) #parking/dropoff/guest
    #vehicle data
	brand = models.CharField(max_length=50)
	platenumber = models.CharField(max_length=50)
	vehicleType = models.CharField(max_length=50)#2-Wheels/4-Wheels
	color = models.CharField(max_length=50)
	prevStickerNo = models.CharField(max_length=50)

	class meta:
	    db_table = 'Registered'

class User(models.Model):
    #security log in data
	username= models.CharField(max_length=50)
	password = models.CharField(max_length=50)

	class meta:
		db_table = 'User'


class Admin(models.Model):
	#admin log in data
	username= models.CharField(max_length=50,default="admin")
	password = models.CharField(max_length=50, default="admin")

	class meta:
		db_table = 'Admin'


class ParkingRecords(models.Model):
	platenumber = models.CharField(max_length=50,default=True)
	date_in = models.DateField(max_length=50,default=True)
	time_in = models.TimeField(max_length=50,default=True)
	date_out = models.DateField(max_length=50,null=True)
	time_out = models.TimeField(max_length=50,null=True)
	#count = models.IntegerField()#para sa ihap kung pila ka vehicles naa sa sulod sa cit

	class meta:
		db_table = "ParkingRecords"


#include dailyRecords table for another table in database
'''
class dailyRecords(models.Model):
	date = models.DateField()
	timeIn = models.TimeField()
	timeOut = models.TimeField()
	plateNumber = models.ForeignKey
	count = models.IntegerField()#para sa ihap kung pila ka vehicles naa sa sulod sa cit

	class meta:
		db_table = "dailyRecords"
'''



######################################################################
'''
class Guest(models.Model):
	#personal data
	idnumber= models.CharField(max_length=50)
	firstname = models.CharField(max_length=50)
	middlename = models.CharField(max_length=50)
	lastname = models.CharField(max_length=50)
	classification = models.CharField(max_length=50)
	department = models.CharField(max_length=500)
	courseyr = models.CharField(max_length=25)
	Ownerfname = models.CharField(max_length=50)
	Ownermname = models.CharField(max_length=50)
	Ownerlname = models.CharField(max_length=50)
	address = models.CharField(max_length=100)
	mobnum = models.CharField(max_length=50)
	landline = models.CharField(max_length=50)
	relation = models.CharField(max_length=50)
    #vehicle data
	brand = models.CharField(max_length=50)
	platenumber = models.CharField(max_length=50)
	vehicleType = models.CharField(max_length=50)
	color = models.CharField(max_length=50)
	prevStickerNo = models.CharField(max_length=50)

	class meta:
	    db_table = 'Guest'

class DropOff(models.Model):
    #personal data
	idnumber= models.CharField(max_length=50)
	firstname = models.CharField(max_length=50)
	middlename = models.CharField(max_length=50)
	lastname = models.CharField(max_length=50)
	classification = models.CharField(max_length=50)
	department = models.CharField(max_length=500)
	courseyr = models.CharField(max_length=25)
	Ownerfname = models.CharField(max_length=50)
	Ownermname = models.CharField(max_length=50)
	Ownerlname = models.CharField(max_length=50)
	address = models.CharField(max_length=100)
	mobnum = models.CharField(max_length=50)
	landline = models.CharField(max_length=50)
	relation = models.CharField(max_length=50)
    #vehicle data
	brand = models.CharField(max_length=50)
	platenumber = models.CharField(max_length=50)
	vehicleType = models.CharField(max_length=50)
	color = models.CharField(max_length=50)
	prevStickerNo = models.CharField(max_length=50)

	class meta:
	    db_table = 'DropOff'
'''

