from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from django.utils import timezone
from datetime import date, datetime
from .models import Prestamo
from .forms import PrestamoForm
from usuarios.models import Usuario
from libros.models import Libro


class PrestamoModelTest(TestCase):
    """Tests para el modelo Prestamo"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.usuario = Usuario.objects.create(
            nombre="Juan Pérez",
            correo="juan@test.com",
            edad=25,
            activo=True
        )
        
        self.libro = Libro.objects.create(
            titulo="El Quijote",
            autor="Miguel de Cervantes",
            fecha_publicacion=date(1605, 1, 16),
            en_prestamo=False
        )
        
        self.prestamo = Prestamo.objects.create(
            usuario=self.usuario,
            libro=self.libro,
            fecha_prestamo=timezone.now()
        )
    
    def test_prestamo_creation(self):
        """Test de creación de préstamo"""
        self.assertEqual(self.prestamo.usuario, self.usuario)
        self.assertEqual(self.prestamo.libro, self.libro)
        self.assertIsNotNone(self.prestamo.fecha_prestamo)
        self.assertIsNone(self.prestamo.fecha_devolucion)
    
    def test_prestamo_relationships(self):
        """Test de relaciones del préstamo"""
        # Test de relación con usuario
        self.assertIn(self.prestamo, self.usuario.prestamos.all())
        
        # Test de relación con libro
        self.assertIn(self.prestamo, self.libro.prestamos.all())
    
    def test_meta_verbose_name_plural(self):
        """Test del nombre plural en Meta"""
        self.assertEqual(Prestamo._meta.verbose_name_plural, "Prestamos")
    
    def test_prestamo_devolucion(self):
        """Test de proceso de devolución"""
        # Inicialmente sin fecha de devolución
        self.assertIsNone(self.prestamo.fecha_devolucion)
        
        # Realizar devolución
        self.prestamo.fecha_devolucion = timezone.now()
        self.prestamo.save()
        
        # Verificar que la devolución se registró
        self.prestamo.refresh_from_db()
        self.assertIsNotNone(self.prestamo.fecha_devolucion)
    
    def test_prestamo_foreign_key_restrict(self):
        """Test que las relaciones son RESTRICT"""
        # El modelo usa on_delete=RESTRICT, lo que significa que no se puede
        # eliminar un usuario o libro si tiene préstamos asociados
        field_usuario = Prestamo._meta.get_field('usuario')
        field_libro = Prestamo._meta.get_field('libro')
        
        self.assertEqual(field_usuario.remote_field.on_delete.__name__, 'RESTRICT')
        self.assertEqual(field_libro.remote_field.on_delete.__name__, 'RESTRICT')


class PrestamoFormTest(TestCase):
    """Tests para el formulario PrestamoForm"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.usuario_activo = Usuario.objects.create(
            nombre="Usuario Activo",
            correo="activo@test.com",
            edad=25,
            activo=True
        )
        
        self.usuario_inactivo = Usuario.objects.create(
            nombre="Usuario Inactivo",
            correo="inactivo@test.com",
            edad=25,
            activo=False
        )
        
        self.libro_disponible = Libro.objects.create(
            titulo="Libro Disponible",
            autor="Autor Test",
            fecha_publicacion=date.today(),
            en_prestamo=False
        )
        
        self.libro_en_prestamo = Libro.objects.create(
            titulo="Libro en Préstamo",
            autor="Autor Test",
            fecha_publicacion=date.today(),
            en_prestamo=True
        )
    
    def test_form_only_shows_active_users(self):
        """Test que el formulario solo muestra usuarios activos"""
        form = PrestamoForm()
        usuarios_disponibles = form.fields['usuario'].queryset
        
        self.assertIn(self.usuario_activo, usuarios_disponibles)
        self.assertNotIn(self.usuario_inactivo, usuarios_disponibles)
    
    def test_form_only_shows_available_books(self):
        """Test que el formulario solo muestra libros disponibles"""
        form = PrestamoForm()
        libros_disponibles = form.fields['libro'].queryset
        
        self.assertIn(self.libro_disponible, libros_disponibles)
        self.assertNotIn(self.libro_en_prestamo, libros_disponibles)
    
    def test_valid_form(self):
        """Test con datos válidos"""
        form_data = {
            'usuario': self.usuario_activo.id,
            'libro': self.libro_disponible.id
        }
        form = PrestamoForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_form_missing_required_fields(self):
        """Test con campos requeridos faltantes"""
        form_data = {
            'usuario': '',
            'libro': self.libro_disponible.id
        }
        form = PrestamoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('usuario', form.errors)
    
    def test_form_save(self):
        """Test de guardado del formulario"""
        form_data = {
            'usuario': self.usuario_activo.id,
            'libro': self.libro_disponible.id
        }
        form = PrestamoForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        prestamo = form.save()
        self.assertEqual(prestamo.usuario, self.usuario_activo)
        self.assertEqual(prestamo.libro, self.libro_disponible)


class PrestamoViewTest(TestCase):
    """Tests para las vistas de Prestamo"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.client = Client()
        
        self.usuario = Usuario.objects.create(
            nombre="Test User",
            correo="test@test.com",
            edad=30,
            activo=True
        )
        
        self.libro = Libro.objects.create(
            titulo="Test Book",
            autor="Test Author",
            fecha_publicacion=date.today(),
            en_prestamo=False
        )
        
        self.prestamo = Prestamo.objects.create(
            usuario=self.usuario,
            libro=self.libro,
            fecha_prestamo=timezone.now()
        )
    
    def test_prestamos_list_view(self):
        """Test de la vista de lista de préstamos"""
        response = self.client.get(reverse('prestamos:prestamos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.usuario.nombre)
        self.assertContains(response, self.libro.titulo)
        
        # Verificar que los préstamos están ordenados por id
        prestamos = response.context['prestamos']
        self.assertEqual(list(prestamos), [self.prestamo])
    
    def test_crear_prestamo_get(self):
        """Test GET de la vista de crear préstamo"""
        response = self.client.get(reverse('prestamos:crear_prestamo'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], PrestamoForm)
    
    def test_crear_prestamo_post_valid(self):
        """Test POST válido para crear préstamo"""
        # Crear un libro disponible para el nuevo préstamo
        libro_nuevo = Libro.objects.create(
            titulo="Nuevo Libro",
            autor="Nuevo Autor",
            fecha_publicacion=date.today(),
            en_prestamo=False
        )
        
        data = {
            'usuario': self.usuario.id,
            'libro': libro_nuevo.id
        }
        response = self.client.post(reverse('prestamos:crear_prestamo'), data)
        
        # Debe redirigir tras crear exitosamente
        self.assertEqual(response.status_code, 302)
        
        # Verificar que el préstamo se creó
        prestamo_nuevo = Prestamo.objects.filter(libro=libro_nuevo).first()
        self.assertIsNotNone(prestamo_nuevo)
        self.assertIsNotNone(prestamo_nuevo.fecha_prestamo)
        
        # Verificar que el libro cambió a en_prestamo=True
        libro_nuevo.refresh_from_db()
        self.assertTrue(libro_nuevo.en_prestamo)
        
        # Verificar mensaje de éxito
        messages = list(get_messages(response.wsgi_request))
        self.assertIn("Préstamo creado exitosamente", str(messages[0]))
        self.assertIn(libro_nuevo.titulo, str(messages[0]))
    
    def test_crear_prestamo_post_invalid(self):
        """Test POST inválido para crear préstamo"""
        data = {
            'usuario': '',  # Campo requerido vacío
            'libro': self.libro.id
        }
        response = self.client.post(reverse('prestamos:crear_prestamo'), data)
        
        # No debe redirigir, debe mostrar errores
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], PrestamoForm)
        self.assertFalse(response.context['form'].is_valid())
    
    def test_realizar_devolucion(self):
        """Test de realizar devolución"""
        # Marcar libro como en préstamo
        self.libro.en_prestamo = True
        self.libro.save()
        
        # Verificar estado inicial
        self.assertIsNone(self.prestamo.fecha_devolucion)
        self.assertTrue(self.libro.en_prestamo)
        
        url = reverse('prestamos:realizar_devolucion', kwargs={'id': self.prestamo.id})
        response = self.client.get(url)
        
        # Debe redirigir tras realizar devolución
        self.assertEqual(response.status_code, 302)
        
        # Verificar que la devolución se registró
        self.prestamo.refresh_from_db()
        self.assertIsNotNone(self.prestamo.fecha_devolucion)
        
        # Verificar que el libro cambió a en_prestamo=False
        self.libro.refresh_from_db()
        self.assertFalse(self.libro.en_prestamo)
        
        # Verificar mensaje de éxito
        messages = list(get_messages(response.wsgi_request))
        self.assertIn("Devolución realizada exitosamente", str(messages[0]))
        self.assertIn(self.libro.titulo, str(messages[0]))
    
    def test_realizar_devolucion_not_found(self):
        """Test realizar devolución de préstamo que no existe"""
        url = reverse('prestamos:realizar_devolucion', kwargs={'id': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_prestamo_workflow_complete(self):
        """Test del flujo completo de préstamo y devolución"""
        # Crear libro disponible
        libro_test = Libro.objects.create(
            titulo="Libro Flujo Test",
            autor="Autor Test",
            fecha_publicacion=date.today(),
            en_prestamo=False
        )
        
        # 1. Crear préstamo
        data = {
            'usuario': self.usuario.id,
            'libro': libro_test.id
        }
        response = self.client.post(reverse('prestamos:crear_prestamo'), data)
        self.assertEqual(response.status_code, 302)
        
        # Verificar que el libro está en préstamo
        libro_test.refresh_from_db()
        self.assertTrue(libro_test.en_prestamo)
        
        # Obtener el préstamo creado
        prestamo_test = Prestamo.objects.filter(libro=libro_test).first()
        self.assertIsNotNone(prestamo_test.fecha_prestamo)
        self.assertIsNone(prestamo_test.fecha_devolucion)
        
        # 2. Realizar devolución
        url = reverse('prestamos:realizar_devolucion', kwargs={'id': prestamo_test.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        
        # Verificar estado final
        prestamo_test.refresh_from_db()
        libro_test.refresh_from_db()
        
        self.assertIsNotNone(prestamo_test.fecha_devolucion)
        self.assertFalse(libro_test.en_prestamo)
    
    def test_prestamo_select_related_optimization(self):
        """Test que la vista de lista use select_related para optimización"""
        response = self.client.get(reverse('prestamos:prestamos'))
        
        # Verificar que la consulta incluye select_related
        prestamos = response.context['prestamos']
        
        # Esta verificación indirecta comprueba que select_related funciona
        # Al acceder a usuario y libro no debería generar consultas adicionales
        with self.assertNumQueries(0):
            for prestamo in prestamos:
                _ = prestamo.usuario.nombre
                _ = prestamo.libro.titulo
