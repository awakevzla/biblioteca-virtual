from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Usuario
from .forms import UsuarioForm

def home(request):
  return render(request, 'home.html')

def users(request):
  return render(request, 'users.html', {'users': Usuario.objects.all()})

def create_user(request):
  if request.method == "POST":
    form = UsuarioForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request, "Usuario registrado con éxito")
      return redirect("usuarios:usuarios")
  else:
    form = UsuarioForm()

  return render(request, "user_create.html", {"form": form})

def edit_user(request, id):
  user = get_object_or_404(Usuario, id=id)
  
  if request.method == "POST":
    form = UsuarioForm(request.POST, instance=user)
    if form.is_valid():
      form.save()
      messages.success(request, "Usuario actualizado con éxito")
      return redirect("usuarios:usuarios")
  else:
    form = UsuarioForm(instance=user)
  
  return render(request, 'user_edit.html', {'user': user, 'form': form})

def delete_user(request, id):
  user = get_object_or_404(Usuario, id=id)
  user_prestamos = user.prestamos.all()
  if len(user_prestamos) > 0:
    messages.warning(request, "El usuario no puede ser eliminado debido a que tiene información relacionada.")
    return redirect("usuarios:usuarios")
  else:
    user.delete()
    messages.success(request, "Usuario eliminado con éxito")
    return redirect("usuarios:usuarios")
