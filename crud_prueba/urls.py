"""
URL configuration for crud_prueba project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from aplicacion import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('vehiculos/', views.vehiculos, name='vehiculos'),
    path('viajes/', views.viajes, name='viajes'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('vehiculos/creados/', views.vehicles, name='vehiculos_creados'),
    path('crear/viaje/', views.crear_viaje, name='crear_viaje'),
    path('viajes/pendientes/', views.viajes_pendientes, name='viajes_pendientes'),
    
    
    
]
