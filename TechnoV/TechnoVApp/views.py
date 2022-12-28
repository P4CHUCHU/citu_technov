from django.shortcuts import render
from hashlib import md5
from django.shortcuts import render
from django.views.generic import View
import mysql.connector
from django.contrib import messages
from .forms import *
from .models import *
from operator import itemgetter
from django.shortcuts import render, redirect
from TechnoVApp.models import User
from TechnoVApp.models import Registered
from django.http import Http404
from django.http import HttpResponse
from django.http.response import HttpResponse
from django.db.models import Count
from datetime import date

import cv2
from PIL import Image
from pytesseract import pytesseract
camera=cv2.VideoCapture(0)
import pytesseract
from io import StringIO
import sys
import time

# Create your views here.
class IndexPageView(View):
    def get(self, request):
        return render(request,'index.html')

class LandingPageView(View):
    def get(self, request):
        return render(request,'pages-landing.html')

class LogInOptionsPageView(View):
    def get(self, request):
        check = Admin.objects.count()
        if check ==0:
            s = Admin.objects.create()
            s.save()
            return render(request,'pages-loginoptions.html')
        else:
            return render(request,'pages-loginoptions.html')

class LogInPageView(View):
    def get(self, request):
        return render (request,'pages-login.html', {})	
        
    def post(self, request):
        username = request.POST.get("username")
        pw = request.POST.get("password")
        user = authenticate(request,username=username, password=pw)
        if user is not None:
            login(request, user)
            return redirect('userDashboard_page_view')
        else:
            messages.info(request,"*Check Id Number or Password*")
            return redirect('login_page_view')

class AdminLogInPageView(View):
    def get(self, request):
        return render (request,'admin-login.html', {})	
        
    def post(self, request):
        username = request.POST.get("username")
        pw = request.POST.get("password")
        check = Admin.objects.filter(username = username).count() and Admin.objects.filter(password=pw).count()
        if check==1:
            return redirect('adminDashboard_page_view')
        else:
            messages.info(request,"*Check Id Number or Password*")
            return redirect('adminLogin_page_view')
'''
def AdminLogInPageView(request):
    con = mysql.connector.connect(host="localhost",user="root",passwd="", database="technov")
    cursor=con.cursor()
    con2 = mysql.connector.connect(host="localhost",user="root",passwd="", database="technov")
    cursor2=con2.cursor()
    sqlcommand="SELECT username from technovapp_admin"
    sqlcommand2="SELECT password from technovapp_admin"
    cursor.execute(sqlcommand)
    cursor2.execute(sqlcommand2)
    u=[]
    p=[]

    for i in cursor:
        u.append(i)

    for j in cursor2:
        p.append(j)

    res= list(map(itemgetter(0),u))
    res2= list(map(itemgetter(0),p))


    if request.method=="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        i=0
        k=len(res2)
        while i<k:
            if res[i]==username and res2[i]==password:
                return redirect('adminDashboard_page_view')
                break
            i+=1
        else:
            messages.info(request,"*Check Id Number or Password*")

    return render(request,'admin-login.html')
'''

class UserDashboardPageView(View):
    def get(self, request):
        vehicle = Registered.objects.all().count()
        records = ParkingRecords.objects.filter(date_in =date.today()).filter(date_out=None).all().values_list('platenumber',flat=True).distinct().count()
        context = {
            'vehicle': vehicle, 'records':records
         }
        return render(request,'index.html',context)

class AdminDashboardPageView(View):
    def get(self, request):
        vehicle = Registered.objects.all().count()
        records = ParkingRecords.objects.filter(date_in =date.today()).filter(date_out=None).all().values_list('platenumber',flat=True).distinct().count()
        user = DjangoUser.objects.count()
        context = {
           'vehicle': vehicle, 'records':records, 'user': user
        }
        return render(request,'pages-dashboardAdmin.html', context)

class vehicleTimeInPageView(View):
    def get(self, request):
        return render(request,'pages-timeIn.html')

class vehicleTimeOutPageView(View):
    def get(self, request):
        return render(request,'pages-timeOut.html')

from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth import authenticate, login, logout

def CreateAccountPageView(request):
    if request.method=="POST":
        account= User()

        username= request.POST.get("username")
        password = request.POST.get("password")

        account.username = username
        account.password = password
        email=""

        # return redirect("registered")
        lCount=0
        uCount=0
        nCount=0
        length=len(password)
        for i in range(0, length):
            if password[i]>="a" and password[i]<="z":
                lCount+=1
            if password[i]>="A" and password[i]<="Z":
                uCount+=1
            if password[i]>="0" and password[i]<="9":
                nCount+=1
        if lCount>=1 and uCount>=1 and nCount>=1:
            if not len(password) < 8:
                account.save()
                messages.info(request, 'User Account Created!')
                DjangoUser.objects.create_user(username,email,password)
                if  account.username=="" or account.password=="" :
                    messages.info(request,'Some Fields are Empty')
        else:
            messages.info(request,'Password must be minimum of 8 characters!')
            messages.info(request,'Must contain atleast one Lowercase!')
            messages.info(request,'Must contain atleast one Uppercase!')
            messages.info(request,'Must contain atleast one Number!')

    return render(request,'create-account.html')
       
    

#Registration of Vehicles into the System
def RegisterPageView(request):
    if request.method=="POST":
        registered=Registered()

        # personal data
        idnumber= request.POST.get("idnumber")
        firstname = request.POST.get("firstname")
        middlename = request.POST.get("middlename")
        lastname = request.POST.get("lastname")
        classification = request.POST.get("classification")#student/admin/staff/parentOrGuardianRelative
        department = request.POST.get("department")#engineering/IT/elementary/juniorhigh/seniorhigh 
        courseyr = request.POST.get("courseyr")
        Ownerfname = request.POST.get("Ownerfname")
        Ownermname = request.POST.get("Ownermname")
        Ownerlname = request.POST.get("Ownerlname")
        address = request.POST.get("address")
        mobnum = request.POST.get("mobnum")
        landline = request.POST.get("landline")
        relation = request.POST.get("relation")#parent/guardian
        identifier = request.POST.get("identifier") #parking/dropoff/guest
        # vehicle data
        brand = request.POST.get("brand")
        platenumber = request.POST.get("platenumber")
        vehicleType = request.POST.get("vehicleType")#2-Wheels/4-Wheels
        color = request.POST.get("color")
        prevStickerNo = request.POST.get("prevStickerNo")

        # personal data
        registered.idnumber = idnumber
        registered.firstname = firstname
        registered.middlename = middlename
        registered.lastname = lastname        
        registered.classification= classification
        registered.department = department
        registered.courseyr = courseyr
        registered.Ownerfname = Ownerfname
        registered.Ownermname = Ownermname
        registered.Ownerlname = Ownerlname
        registered.address = address        
        registered.mobnum= mobnum
        registered.landline = landline
        registered.relation = relation
        registered.identifier = identifier

        # vehicle data
        registered.brand = brand
        registered.platenumber = platenumber        
        registered.vehicleType= vehicleType
        registered.color = color
        registered.prevStickerNo = prevStickerNo

        if  registered.idnumber=="" or registered.firstname=="" or registered.middlename=="" or registered.lastname=="" or registered.classification=="" or registered.department=="" or registered.courseyr=="" or registered.Ownerfname=="" or registered.Ownermname=="" or registered.Ownerlname=="" or registered.address=="" or registered.mobnum=="" or registered.landline=="" or registered.relation=="" or registered.identifier=="" or registered.brand=="" or registered.platenumber=="" or registered.vehicleType=="" or registered.color=="" or registered.prevStickerNo=="":
            messages.info(request,'Some Fields are Empty')

        else:
            registered.save()
            messages.info(request, 'Successfully Registered!')
       
    return render(request,'pages-register.html')

# List of Registered Vehicle
class RegisteredVehiclePageView(View):
    def get(self, request):
        register = Registered.objects.all()
        context = {
            'register': register
        }
        return render(request,'pages-registeredVehicles.html',context)

    def post(self, request):
        
        if request.method == 'POST':
            
            if 'btnUpdate' in request.POST: 
                print('update profile button clicked')
                id = request.POST.get("id")
                idnumber= request.POST.get("idnumber")
                firstname = request.POST.get("firstname")
                middlename = request.POST.get("middlename")
                lastname = request.POST.get("lastname")
                classification = request.POST.get("classification")#student/admin/staff/parentOrGuardianRelative
                department = request.POST.get("department")#engineering/IT/elementary/juniorhigh/seniorhigh 
                courseyr = request.POST.get("courseyr")
                Ownerfname = request.POST.get("Ownerfname")
                Ownermname = request.POST.get("Ownermname")
                Ownerlname = request.POST.get("Ownerlname")
                address = request.POST.get("address")
                mobnum = request.POST.get("mobnum")
                landline = request.POST.get("landline")
                relation = request.POST.get("relation")#parent/guardian
                identifier = request.POST.get("identifier") #parking/dropoff/guest
                # vehicle data
                brand = request.POST.get("brand")
                platenumber = request.POST.get("platenumber")
                vehicleType = request.POST.get("vehicleType")#2-Wheels/4-Wheels
                color = request.POST.get("color")
                prevStickerNo = request.POST.get("prevStickerNo")
             
                
                update_user = Registered.objects.filter(id = id).update(id = id, idnumber = idnumber, firstname = firstname, middlename=middlename ,lastname = lastname, classification = classification, department = department, courseyr = courseyr, Ownerfname=Ownerfname, Ownermname=Ownermname, Ownerlname=Ownerlname, address=address, mobnum=mobnum, landline=landline, relation=relation, identifier=identifier,brand=brand, platenumber=platenumber, vehicleType=vehicleType, color=color, prevStickerNo=prevStickerNo)
                print(update_user)
                print('profile updated')
                return redirect('registeredVehicle_page_view')
            elif 'btnDelete' in request.POST:
                print('delete button clicked')
                id = request.POST.get("id")
                userdel = Registered.objects.filter(id=id).delete()
                print('record deleted')
                return redirect('registeredVehicle_page_view')

class userInputSearchPageView(View):
    def get(self, request):
        register = Registered.objects.all()
        
        return render(request,'pages-userInputSearch.html')

    def post(self, request):
        today = date.today()
        if request.method == 'POST':
            if 'btnSearch' in request.POST:
                platenumber = request.POST.get('platenumber')
                registered = Registered.objects.filter(platenumber__icontains=platenumber) or Registered.objects.filter(prevStickerNo__icontains=platenumber)
                return render(request,'pages-userInputSearch.html', {'platenumber':platenumber,'registered':registered})
                    
            elif 'btnIn' in request.POST:
                parkingRecords=ParkingRecords()
                
                platenumber = request.POST.get('platenumber')
                time_in = time.strftime("%H:%M")
                date_in = today.strftime("%Y-%m-%d")

                parkingRecords.platenumber = platenumber 
                parkingRecords.date_in = date_in
                parkingRecords.time_in = time_in
                parkingRecords.save()
                messages.info(request, 'Successfully Timed In!')
                return redirect('parkingRecords_page_view')

            elif 'btnOut' in request.POST:
                parkingRecords=ParkingRecords()
                
                platenumber = request.POST.get("platenumber")
                time_out = time.strftime("%H:%M")
                date_out = today.strftime("%Y-%m-%d")

                parkingRecords.platenumber = platenumber 
                parkingRecords.date_out = date_out
                parkingRecords.time_out = time_out
                update_user = ParkingRecords.objects.filter(date_out__isnull=True).filter(platenumber=platenumber).update(date_out=date_out, time_out=time_out)
                print(update_user)
                messages.info(request, 'Successfully Timed Out!')
                return redirect('parkingRecords_page_view')



class ScanningPageView(View):
    def get(self, request):
        camera=cv2.VideoCapture(0)    
        #address="https://192.168.68.106:8080/video"
        #camera.open(address)

        while True:
            _,image=camera.read()
            cv2.imshow('image',image)
            if cv2.waitKey(1)& 0xFF==ord(' '):
                cv2.imwrite('media/test1.jpg',image)
                break
        camera.release()
        cv2.destroyAllWindows()
        buffer = StringIO()
        sys.stdout = buffer
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

        image_path = "media/test1.jpg"
        print(pytesseract.image_to_string(Image.open(image_path)))#SAM
        print_output = buffer.getvalue()
        sys.stdout = sys.__stdout__
        print('', print_output)
        context = {
           'plate': print_output
        }

        return render(request,'pages-optionstoscan.html', context)

    def post(self, request):
        today = date.today()
        if request.method == 'POST':

            if 'btnScan' in request.POST:
                platenumber =request.POST.get('platenumber')
                scan = Registered.objects.filter(platenumber__contains=platenumber) or Registered.objects.filter(prevStickerNo__contains=platenumber)
                return render(request,'pages-optionstoscan.html', {'scan':scan})

            elif 'btnIn' in request.POST:
                parkingRecords=ParkingRecords()
                
                platenumber = request.POST.get('platenumber')
                time_in = time.strftime("%H:%M")
                date_in = today.strftime("%Y-%m-%d")

                parkingRecords.platenumber = platenumber 
                parkingRecords.date_in = date_in
                parkingRecords.time_in = time_in
                parkingRecords.save()
                messages.info(request, 'Successfully Timed In!')
                return redirect('parkingRecords_page_view')

            elif 'btnOut' in request.POST:
                parkingRecords=ParkingRecords()
                
                platenumber = request.POST.get("platenumber")
                time_out = time.strftime("%H:%M")
                date_out = today.strftime("%Y-%m-%d")

                parkingRecords.platenumber = platenumber 
                parkingRecords.date_out = date_out
                parkingRecords.time_out = time_out
                update_user = ParkingRecords.objects.filter(date_out__isnull=True).filter(platenumber=platenumber).update(date_out=date_out, time_out=time_out)
                print(update_user)
                messages.info(request, 'Successfully Timed Out!')
                return redirect('parkingRecords_page_view')

class ParkingRecordPageView(View):
    def get(self, request):
        records = ParkingRecords.objects.all()
        parked = ParkingRecords.objects.filter(date_in =date.today()).filter(date_out=None).all().values_list('platenumber',flat=True).distinct().count()
        register = Registered.objects.all()
        context = {
           'records': records,'register': register,'parked': parked,
        }

        return render(request,'pages-parkingRecord.html',context)

    def post(self, request):
        if request.method == 'POST':
            if request.method == 'POST':
                platenumber = request.POST.get('platenumber')
                registered = Registered.objects.filter(platenumber=platenumber) or Registered.objects.filter(prevStickerNo=platenumber)
                return render(request,'pages-driverInfo.html', {'platenumber':platenumber,'registered':registered})
                #return redirect('registeredVehicle_page_view')
            elif 'btnDelete' in request.POST:
                print('delete button clicked')
                id = request.POST.get("id")
                userdel = ParkingRecords.objects.filter(id=id).delete()
                print('record deleted')
                return redirect('parkingRecords_page_view')

import datetime
class RecordsTodayPageView(View):
    def get(self, request):
        today = datetime.date.today()
        records = ParkingRecords.objects.filter(date_in = date.today()).all
        parked = ParkingRecords.objects.filter(date_in =date.today()).filter(date_out=None).all().values_list('platenumber',flat=True).distinct().count()
        
        context = {
           'records': records, 'parked':parked
        }

        return render(request,'pages-ParkingRecordToday.html',context)

    def post(self, request):
        if request.method == 'POST':
            if request.method == 'POST':
                platenumber = request.POST.get('platenumber')
                registered = Registered.objects.filter(platenumber=platenumber) or Registered.objects.filter(prevStickerNo=platenumber)
                return render(request,'pages-driverInfo.html', {'platenumber':platenumber,'registered':registered})
            elif 'btnDelete' in request.POST:
                print('delete button clicked')
                id = request.POST.get("id")
                userdel = Registered.objects.filter(id=id).delete()
                print('record deleted')
                return redirect('registeredVehicle_page_view')


class RecordsMonthPageView(View):
    def get(self, request):
        today = datetime.date.today()
        records = ParkingRecords.objects.filter(date_in__year=today.year,
                           date_in__month=today.month)
        parked = ParkingRecords.objects.filter(date_in =date.today()).filter(date_out=None).all().values_list('platenumber',flat=True).distinct().count()
        
        context = {
           'records': records,'parked':parked
        }

        return render(request,'pages-parkingRecordMonth.html',context)

    def post(self, request):
        if request.method == 'POST':
            if request.method == 'POST':
                platenumber = request.POST.get('platenumber')
                registered = Registered.objects.filter(platenumber=platenumber) or Registered.objects.filter(prevStickerNo=platenumber)
                return render(request,'pages-driverInfo.html', {'platenumber':platenumber,'registered':registered})
            elif 'btnDelete' in request.POST:
                print('delete button clicked')
                id = request.POST.get("id")
                userdel = Registered.objects.filter(id=id).delete()
                print('record deleted')
                return redirect('registeredVehicle_page_view')


def vehicleTimeInPageView(request):
    if request.method=="POST":
        platenumber = request.POST.get("platenumber")
        check = Registered.objects.filter(platenumber=platenumber).count() or Registered.objects.filter(prevStickerNo=platenumber).count()
        if check == 1:
            parkingRecords=ParkingRecords()
            platenumber = request.POST.get("platenumber")
            date_in = request.POST.get("date")
            time_in = request.POST.get("time")

                # personal data

                # vehicle data
            parkingRecords.platenumber = platenumber 
            parkingRecords.date_in = date_in
            parkingRecords.time_in = time_in
            parkingRecords.save()
            messages.info(request, 'Successfully Timed In!')
            return redirect('parkingRecords_page_view')
        else:
            messages.info(request,"Vehicle Not Registered!")

    return render(request,'pages-timeIn.html')

from datetime import date
def vehicleTimeOutPageView(request):
    if request.method=="POST":
        platenumber = request.POST.get("platenumber")
        date_in=date.today()
        check = ParkingRecords.objects.filter(platenumber=platenumber).filter(date_in =date.today()).filter(date_out=None).count()
        print(check)
        if check ==1:
            parkingRecords=ParkingRecords()
                
            platenumber = request.POST.get("platenumber")
            date_out = request.POST.get("date")
            time_out = request.POST.get("time")
            parkingRecords.platenumber = platenumber 
            parkingRecords.date_out = date_out
            parkingRecords.time_out = time_out
            update_user = ParkingRecords.objects.filter(date_out__isnull=True).filter(platenumber=platenumber).update(date_out=date_out, time_out=time_out)
            print(update_user)
            messages.info(request, 'Successfully Timed Out!')
            return redirect('parkingRecords_page_view')
        else:
            messages.info(request,"Vehicle Not Timed In!")

    return render(request,'pages-timeOut.html')

import numpy as np
import pytesseract
from PIL import Image
import base64

def OptionsToScanPageView(request):
    if request.method == "POST":
        try:
            image = request.FILES["imagefile"]
            image_base64 = base64.b64encode(image.read()).decode("utf-8")
        except:
            messages.add_message(
                    request, messages.ERROR, "No image selected or uploaded"
            )
            return render(request, "pages-optionstoscan.html")
        img = np.array(Image.open(image))
        custom_config = r'--oem 3 --psm 6 outputbase digits'
        text = pytesseract.image_to_string(img)
        return render(request, "pages-optionstoscan.html", {"ocr": text, "image": image_base64})

    return render(request, "pages-optionstoscan.html")


class AdminRegisteredVehiclePageView(View):
    def get(self, request):
        register = Registered.objects.all()
        context = {
            'register': register
        }
        return render(request,'pages-adminRegisteredVehicles.html',context)

    def post(self, request):
        
        if request.method == 'POST':
            
            if 'btnUpdate' in request.POST: 
                print('update profile button clicked')
                id = request.POST.get("id")
                idnumber= request.POST.get("idnumber")
                firstname = request.POST.get("firstname")
                middlename = request.POST.get("middlename")
                lastname = request.POST.get("lastname")
                classification = request.POST.get("classification")#student/admin/staff/parentOrGuardianRelative
                department = request.POST.get("department")#engineering/IT/elementary/juniorhigh/seniorhigh 
                courseyr = request.POST.get("courseyr")
                Ownerfname = request.POST.get("Ownerfname")
                Ownermname = request.POST.get("Ownermname")
                Ownerlname = request.POST.get("Ownerlname")
                address = request.POST.get("address")
                mobnum = request.POST.get("mobnum")
                landline = request.POST.get("landline")
                relation = request.POST.get("relation")#parent/guardian
                identifier = request.POST.get("identifier") #parking/dropoff/guest
                # vehicle data
                brand = request.POST.get("brand")
                platenumber = request.POST.get("platenumber")
                vehicleType = request.POST.get("vehicleType")#2-Wheels/4-Wheels
                color = request.POST.get("color")
                prevStickerNo = request.POST.get("prevStickerNo")
             
                
                update_user = Registered.objects.filter(id = id).update(id = id, idnumber = idnumber, firstname = firstname, middlename=middlename ,lastname = lastname, classification = classification, department = department, courseyr = courseyr, Ownerfname=Ownerfname, Ownermname=Ownermname, Ownerlname=Ownerlname, address=address, mobnum=mobnum, landline=landline, relation=relation, identifier=identifier,brand=brand, platenumber=platenumber, vehicleType=vehicleType, color=color, prevStickerNo=prevStickerNo)
                print(update_user)
                print('profile updated')
                return redirect('admin_registeredVehicle_page_view')
            elif 'btnDelete' in request.POST:
                print('delete button clicked')
                id = request.POST.get("id")
                userdel = Registered.objects.filter(id=id).delete()
                print('record deleted')
                return redirect('admin_registeredVehicle_page_view')


class AdminParkingRecordPageView(View):
    def get(self, request):
        records = ParkingRecords.objects.all()
        parked = ParkingRecords.objects.filter(date_in =date.today()).filter(date_out=None).all().values_list('platenumber',flat=True).distinct().count()
        register = Registered.objects.all()
        context = {
           'records': records,'register': register,'parked': parked,
        }

        return render(request,'pages-adminParkingRecord.html',context)

    def post(self, request):
        if request.method == 'POST':
            if request.method == 'POST':
                platenumber = request.POST.get('platenumber')
                registered = Registered.objects.filter(platenumber=platenumber) or Registered.objects.filter(prevStickerNo=platenumber)
                return render(request,'pages-adminDriverInfo.html', {'platenumber':platenumber,'registered':registered})
            elif 'btnDelete' in request.POST:
                print('delete button clicked')
                id = request.POST.get("id")
                userdel = Registered.objects.filter(id=id).delete()
                print('record deleted')
                return redirect('admin_parkingRecords_page_view')

class AdminUserRecordPageView(View):
    def get(self, request):
        records = DjangoUser.objects.all()
        context = {
           'records': records
        }

        return render(request,'pages-adminUserRecord.html',context)

    def post(self, request):
        if request.method == 'POST':
            if request.method == 'POST':
                platenumber = request.POST.get('platenumber')
                registered = Registered.objects.filter(platenumber=platenumber) or Registered.objects.filter(prevStickerNo=platenumber)
                return render(request,'pages-adminDriverInfo.html', {'platenumber':platenumber,'registered':registered})
            elif 'btnDelete' in request.POST:
                print('delete button clicked')
                id = request.POST.get("id")
                userdel = Registered.objects.filter(id=id).delete()
                print('record deleted')
                return redirect('admin_parkingRecords_page_view')

import datetime
class AdminRecordsTodayPageView(View):
    def get(self, request):
        today = datetime.date.today()
        records = ParkingRecords.objects.filter(date_in = date.today()).all
        parked = ParkingRecords.objects.filter(date_in =date.today()).filter(date_out=None).all().values_list('platenumber',flat=True).distinct().count()
        
        context = {
           'records': records, 'parked':parked
        }

        return render(request,'pages-adminParkingRecordToday.html',context)

    def post(self, request):
        if request.method == 'POST':
            if request.method == 'POST':
                platenumber = request.POST.get('platenumber')
                registered = Registered.objects.filter(platenumber=platenumber) or Registered.objects.filter(prevStickerNo=platenumber)
                return render(request,'pages-adminDriverInfo.html', {'platenumber':platenumber,'registered':registered})
            elif 'btnDelete' in request.POST:
                print('delete button clicked')
                id = request.POST.get("id")
                userdel = Registered.objects.filter(id=id).delete()
                print('record deleted')
                return redirect('registeredVehicle_page_view')


class AdminRecordsMonthPageView(View):
    def get(self, request):
        today = datetime.date.today()
        records = ParkingRecords.objects.filter(date_in__year=today.year,
                           date_in__month=today.month)
        parked = ParkingRecords.objects.filter(date_in =date.today()).filter(date_out=None).all().values_list('platenumber',flat=True).distinct().count()
        
        context = {
           'records': records,'parked':parked
        }

        return render(request,'pages-adminParkingRecordMonth.html',context)

    def post(self, request):
        if request.method == 'POST':
            if request.method == 'POST':
                platenumber = request.POST.get('platenumber')
                registered = Registered.objects.filter(platenumber=platenumber) or Registered.objects.filter(prevStickerNo=platenumber)
                return render(request,'pages-adminDriverInfo.html', {'platenumber':platenumber,'registered':registered})
            elif 'btnDelete' in request.POST:
                print('delete button clicked')
                id = request.POST.get("id")
                userdel = Registered.objects.filter(id=id).delete()
                print('record deleted')
                return redirect('registeredVehicle_page_view')