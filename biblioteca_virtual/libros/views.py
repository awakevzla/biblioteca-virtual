from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Libro
from .forms import LibroForm

def libros(request):
  return render(request, 'listar_libros.html', {'libros': Libro.objects.all().order_by("id")})

def create_libro(request):
  if request.method == "POST":
    form = LibroForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request, "Usuario registrado...")
      return redirect("libros:libros")
  else:
    form = LibroForm()

  return render(request, "create_libro.html", {"form": form})

def edit_libro(request, id):
  libro = get_object_or_404(Libro, id=id)
  
  if request.method == "POST":
    form = LibroForm(request.POST, instance=libro)
    if form.is_valid():
      form.save()
      messages.success(request, "Libro actualizado...")
      return redirect("libros:libros")
  else:
    form = LibroForm(instance=libro)
  
  return render(request, 'edit_libro.html', {'libro': libro, 'form': form})

def delete_libro(request, id):
  user = get_object_or_404(Libro, id=id)
  user.delete()
  return redirect("libros:libros")
