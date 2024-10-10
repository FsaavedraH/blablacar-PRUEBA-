from django.db import models
from django.contrib.auth.models import User

class Passenger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Vehicle(models.Model):
    marca = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    license_plate = models.CharField(max_length=10, unique=True)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='vehicles', null=True)  # Permitir null

    def __str__(self):
        return f"{self.marca} {self.model} ({self.year})"


class Viaje(models.Model):
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)  # Relación con Passenger
    origen = models.CharField(max_length=100)  # Origen del viaje
    destino = models.CharField(max_length=100)  # Destino del viaje
    fecha = models.DateTimeField()  # Fecha y hora del viaje
    estado = models.CharField(max_length=20, choices=[
        ('pendiente', 'Pendiente'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ], default='pendiente')  # Estado del viaje

    def __str__(self):
        return f"Viaje de {self.passenger.user.username} de {self.origen} a {self.destino}"