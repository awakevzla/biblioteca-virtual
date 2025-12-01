from django.urls import path

from . import views

app_name = 'prestamos'

urlpatterns = [
    path('', views.prestamos, name='prestamos'),
    path('create/', views.crear_prestamo, name='crear_prestamo'),
    path('devolvolver/<int:id>/', views.realizar_devolucion, name='realizar_devolucion')
]
