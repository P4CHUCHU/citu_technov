"""TechnoV URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from TechnoVApp import views
from django.conf.urls.static import static
from TechnoV import settings

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('',views.LandingPageView.as_view(),name="landing_page_view"),
    path('loginoptions',views.LogInOptionsPageView.as_view(),name="loginoptions_page_view"),

    path('login',views.LogInPageView.as_view(),name="login_page_view"),
    path('optionstoscan',views.OptionsToScanPageView,name="optionstoscan_page_view"),
    path('register',views.RegisterPageView,name="register_page_view"),
    path('userDashboard',views.UserDashboardPageView.as_view(),name="userDashboard_page_view"),
    path('timeIn',views.vehicleTimeInPageView,name="vehicleTimeIn_page_view"),
    path('timeOut',views.vehicleTimeOutPageView,name="vehicleTimeOut_page_view"),    
    path('userInputSearch',views.userInputSearchPageView.as_view(),name="userInputSearch_page_view"),
    path('parkingRecords',views.ParkingRecordPageView.as_view(),name="parkingRecords_page_view"),
    path('registeredVehicle',views.RegisteredVehiclePageView.as_view(),name="registeredVehicle_page_view"),
    path('scan',views.ScanningPageView.as_view(),name="scanning_page_view"),
    path('today',views.RecordsTodayPageView.as_view(),name="today_page_view"),
    path('month',views.RecordsMonthPageView.as_view(),name="month_page_view"),
     
    path('admin/login',views.AdminLogInPageView.as_view(),name="adminLogin_page_view"),
    path('admin/Dashboard',views.AdminDashboardPageView.as_view(),name="adminDashboard_page_view"),
    path('admin/createAccount',views.CreateAccountPageView,name="createAccount_page_view"),
    path('admin/registeredVehicle',views.AdminRegisteredVehiclePageView.as_view(),name="admin_registeredVehicle_page_view"),
    path('admin/parkingRecords',views.AdminParkingRecordPageView.as_view(),name="admin_parkingRecords_page_view"),
    path('admin/userRecords',views.AdminUserRecordPageView.as_view(),name="admin_userRecord_page_view"),
    path('admin/today',views.AdminRecordsTodayPageView.as_view(),name="today_page_view"),
    path('admin/month',views.AdminRecordsMonthPageView.as_view(),name="month_page_view"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
