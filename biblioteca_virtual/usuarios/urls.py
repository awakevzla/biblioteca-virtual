from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('', views.users, name='usuarios'),
    path('create/', views.create_user, name='crear_usuario'),
    path('<int:id>/', views.edit_user, name='editar_usuario'),
    path('delete/<int:id>/', views.delete_user, name='eliminar_usuario')
]
