from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .models import Passenger, Driver, Viaje
from .forms import VehicleForm, ViajeForm
from django.core.exceptions import ObjectDoesNotExist
from .models import Vehicle

# Create your views here.
def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm()
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            username = request.POST['username']
            password = request.POST['password1']
            role = request.POST['role']  # Obtener el rol del formulario
            
            try:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                
                # Crear el Passenger o Driver según el rol
                if role == 'passenger':
                    Passenger.objects.create(user=user)
                    login(request, user)
                    return redirect('crear_viaje')  # Redirigir a la página de crear viaje si es pasajero
                elif role == 'driver':
                    Driver.objects.create(user=user)
                    login(request, user)
                    return redirect('vehiculos')  # Redirigir a la página de vehículos si es conductor
                
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm(),
                    'error': 'Username already exists'
                })
                
        return render(request, 'signup.html', {
            'form': UserCreationForm(),
            'error': 'Passwords do not match'
        })


def vehiculos(request):
    if request.method == 'GET':
        form = VehicleForm()
        return render(request, 'vehiculos.html', {
            'form': form
        })
    else:
        form = VehicleForm(request.POST)
        if form.is_valid():
            new_vehicle = form.save(commit=False)
            try:
                # Obtener el Driver asociado al usuario que está logueado
                driver = Driver.objects.get(user=request.user)
                new_vehicle.driver = driver  # Asigna el conductor al vehículo
                new_vehicle.save()  # Guardar el vehículo
                print(new_vehicle)
                return redirect('vehiculos')
            except ObjectDoesNotExist:
                return render(request, 'vehiculos.html', {
                    'form': form,
                    'error': 'No se encontró el conductor asociado a este usuario.'
                })
            except Exception as e:
                return render(request, 'vehiculos.html', {
                    'form': form,
                    'error': f'Ocurrió un error al guardar el vehículo: {str(e)}'
                })
        else:
            return render(request, 'vehiculos.html', {
                'form': form,
                'error': 'Error en el formulario.'
            })


def vehicles(request):
    if request.user.is_authenticated:
        try:
            # Obtén el objeto Driver relacionado con el usuario logueado
            driver = Driver.objects.get(user=request.user)
            vehicles = Vehicle.objects.filter(driver=driver)  # Filtra los vehículos por el Driver
        except Driver.DoesNotExist:
            vehicles = Vehicle.objects.none()  # Si no hay Driver, no muestra vehículos
    else:
        vehicles = Vehicle.objects.none()  # No muestra vehículos si no hay usuario autenticado

    return render(request, 'vehiculos_creados.html', {'vehicles': vehicles, 'user': request.user})
      

def viajes(request):
    return render(request,'viajes.html')


def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm()
        })
    else: 
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is None:
                return render(request, 'signin.html', {
                    'form': form,
                    'error': 'Username or password is incorrect'
                })
            else: 
                login(request, user)

                # Verificar el rol del usuario y redirigir
                try:
                    # Verificar si el usuario es un pasajero
                    Passenger.objects.get(user=user)
                    return redirect('crear_viaje')  # Redirigir a la página de crear viaje si es pasajero
                except Passenger.DoesNotExist:
                    try:
                        # Verificar si el usuario es un conductor
                        Driver.objects.get(user=user)
                        return redirect('vehiculos')  # Redirigir a la página de vehículos si es conductor
                    except Driver.DoesNotExist:
                        return redirect('rol')  # Redirigir a una página predeterminada si no tiene rol

        else:
            return render(request, 'signin.html', {
                'form': form,
            })


from django.shortcuts import render
from .models import Viaje, Driver

def viajes_pendientes(request):
    if request.user.is_authenticated:
        try:
            driver = Driver.objects.get(user=request.user)
            # Filtrar viajes pendientes para el conductor
            viajes = Viaje.objects.filter(driver=driver, estado='pendiente')
            return render(request, 'viajes_pendientes.html', {'viajes': viajes})
        except Driver.DoesNotExist:
            # Manejar el caso en que no existe el conductor
            return render(request, 'error.html', {'error': 'No se encontró el conductor.'})
    else:
        return redirect('signin')  # Redirigir a la página de inicio de sesión si no está autenticado


# Crear un nuevo viaje
def crear_viaje(request):
    if request.method == 'POST':
        form = ViajeForm(request.POST)
        if form.is_valid():
            # Obtener el pasajero del usuario logueado
            passenger = Passenger.objects.get(user=request.user)

            # Crear el viaje
            nuevo_viaje = form.save(commit=False)  # No guardar aún
            nuevo_viaje.passenger = passenger  # Asignar el pasajero
            nuevo_viaje.save()  # Ahora guarda el viaje

            return redirect('crear_viaje')  # Redirigir a la misma vista
    else:
        form = ViajeForm()  # Crear un nuevo formulario vacío para el método GET

    passenger_name = request.user.username  # Obtener el nombre del pasajero
    return render(request, 'crear_viaje.html', {'form': form, 'passenger_name': passenger_name})

