from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import Prestamo
from .forms import PrestamoForm

def prestamos(request):
  prestamos = Prestamo.objects.select_related('usuario', 'libro').order_by("id")
  return render(request, 'listar_prestamos.html', {'prestamos': prestamos})

def crear_prestamo(request):
  if request.method == 'POST':
    form = PrestamoForm(request.POST)
    if form.is_valid():
      prestamo = form.save()
      prestamo.fecha_prestamo = timezone.now()
      prestamo.save()
      libro = prestamo.libro
      libro.en_prestamo = True
      libro.save()

      messages.success(request, f'Préstamo creado exitosamente. El libro "{libro.titulo}" ahora está en préstamo.')
      return redirect('prestamos:prestamos')
  else:
    form = PrestamoForm()
    
    return render(request, 'crear_prestamo.html', {'form': form})

def realizar_devolucion(request, id):
  prestamo = get_object_or_404(Prestamo, id=id)

  libro = prestamo.libro
  prestamo.fecha_devolucion = timezone.now()
  prestamo.save()
  libro.en_prestamo = False
  libro.save()

  messages.success(request, f'Devolución realizada exitosamente. El libro "{libro.titulo}" está disponible.')
  return redirect('prestamos:prestamos')