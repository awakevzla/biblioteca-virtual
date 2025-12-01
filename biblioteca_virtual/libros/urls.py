from django.urls import path
from . import views

app_name = 'libros'

urlpatterns = [
    path('', views.libros, name='libros'),
    path('create/', views.create_libro, name='crear_libro'),
    path('<int:id>/', views.edit_libro, name='editar_libro'),
    path('delete/<int:id>/', views.delete_libro, name='eliminar_libro')
]
