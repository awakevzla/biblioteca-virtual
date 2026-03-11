from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from .models import Usuario
from .forms import UsuarioForm
from datetime import datetime


class UsuarioModelTest(TestCase):
    """Tests para el modelo Usuario"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.usuario = Usuario.objects.create(
            nombre="Juan Pérez",
            correo="juan@test.com",
            edad=25,
            activo=True
        )
    
    def test_usuario_creation(self):
        """Test de creación de usuario"""
        self.assertEqual(self.usuario.nombre, "Juan Pérez")
        self.assertEqual(self.usuario.correo, "juan@test.com")
        self.assertEqual(self.usuario.edad, 25)
        self.assertTrue(self.usuario.activo)
        self.assertIsInstance(self.usuario.fecha_registro, datetime)
    
    def test_usuario_str_method(self):
        """Test del método __str__"""
        expected_str = "Juan Pérez (juan@test.com)"
        self.assertEqual(str(self.usuario), expected_str)
    
    def test_correo_unique(self):
        """Test que el correo sea único"""
        with self.assertRaises(Exception):
            Usuario.objects.create(
                nombre="María García",
                correo="juan@test.com",  # Mismo correo
                edad=30,
                activo=True
            )
    
    def test_default_values(self):
        """Test de valores por defecto"""
        usuario = Usuario.objects.create(
            nombre="Ana López",
            correo="ana@test.com",
            edad=28
        )
        self.assertTrue(usuario.activo)  # Debe ser True por defecto
    
    def test_meta_verbose_name_plural(self):
        """Test del nombre plural en Meta"""
        self.assertEqual(Usuario._meta.verbose_name_plural, "Usuarios")


class UsuarioFormTest(TestCase):
    """Tests para el formulario UsuarioForm"""
    
    def test_valid_form(self):
        """Test con datos válidos"""
        form_data = {
            'nombre': 'Pedro Martínez',
            'correo': 'pedro@test.com',
            'edad': 22,
            'activo': True
        }
        form = UsuarioForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_form_missing_required_fields(self):
        """Test con campos requeridos faltantes"""
        form_data = {
            'nombre': '',
            'correo': 'test@test.com',
            'edad': 25
        }
        form = UsuarioForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)
    
    def test_form_invalid_email(self):
        """Test con email inválido"""
        form_data = {
            'nombre': 'Test User',
            'correo': 'invalid-email',
            'edad': 25,
            'activo': True
        }
        form = UsuarioForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('correo', form.errors)
    
    def test_form_save(self):
        """Test de guardado del formulario"""
        form_data = {
            'nombre': 'Luis Rodríguez',
            'correo': 'luis@test.com',
            'edad': 35,
            'activo': False
        }
        form = UsuarioForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        usuario = form.save()
        self.assertEqual(usuario.nombre, 'Luis Rodríguez')
        self.assertEqual(usuario.correo, 'luis@test.com')
        self.assertEqual(usuario.edad, 35)
        self.assertFalse(usuario.activo)


class UsuarioViewTest(TestCase):
    """Tests para las vistas de Usuario"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.client = Client()
        self.usuario = Usuario.objects.create(
            nombre="Test User",
            correo="test@test.com",
            edad=30,
            activo=True
        )
    
    def test_home_view(self):
        """Test de la vista home"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
    
    def test_users_list_view(self):
        """Test de la vista de lista de usuarios"""
        response = self.client.get(reverse('usuarios:usuarios'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.usuario.nombre)
        self.assertContains(response, self.usuario.correo)
    
    def test_create_user_get(self):
        """Test GET de la vista de crear usuario"""
        response = self.client.get(reverse('usuarios:crear_usuario'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], UsuarioForm)
    
    def test_create_user_post_valid(self):
        """Test POST válido para crear usuario"""
        data = {
            'nombre': 'Nuevo Usuario',
            'correo': 'nuevo@test.com',
            'edad': 25,
            'activo': True
        }
        response = self.client.post(reverse('usuarios:crear_usuario'), data)
        
        # Debe redirigir tras crear exitosamente
        self.assertEqual(response.status_code, 302)
        
        # Verificar que el usuario se creó
        self.assertTrue(Usuario.objects.filter(correo='nuevo@test.com').exists())
        
        # Verificar mensaje de éxito
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Usuario registrado con éxito")
    
    def test_create_user_post_invalid(self):
        """Test POST inválido para crear usuario"""
        data = {
            'nombre': '',  # Campo requerido vacío
            'correo': 'invalid-email',
            'edad': 'abc'  # Edad inválida
        }
        response = self.client.post(reverse('usuarios:crear_usuario'), data)
        
        # No debe redirigir, debe mostrar errores
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], UsuarioForm)
        self.assertFalse(response.context['form'].is_valid())
    
    def test_edit_user_get(self):
        """Test GET de la vista de editar usuario"""
        url = reverse('usuarios:editar_usuario', kwargs={'id': self.usuario.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'], self.usuario)
        self.assertIsInstance(response.context['form'], UsuarioForm)
    
    def test_edit_user_post_valid(self):
        """Test POST válido para editar usuario"""
        data = {
            'nombre': 'Usuario Editado',
            'correo': self.usuario.correo,  # Mantener el mismo correo
            'edad': 35,
            'activo': False
        }
        url = reverse('usuarios:editar_usuario', kwargs={'id': self.usuario.id})
        response = self.client.post(url, data)
        
        # Debe redirigir tras editar exitosamente
        self.assertEqual(response.status_code, 302)
        
        # Verificar que el usuario se actualizó
        self.usuario.refresh_from_db()
        self.assertEqual(self.usuario.nombre, 'Usuario Editado')
        self.assertEqual(self.usuario.edad, 35)
        self.assertFalse(self.usuario.activo)
    
    def test_edit_user_not_found(self):
        """Test editar usuario que no existe"""
        url = reverse('usuarios:editar_usuario', kwargs={'id': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_delete_user_without_loans(self):
        """Test eliminar usuario sin préstamos"""
        usuario_id = self.usuario.id
        url = reverse('usuarios:eliminar_usuario', kwargs={'id': usuario_id})
        response = self.client.get(url)
        
        # Debe redirigir tras eliminar
        self.assertEqual(response.status_code, 302)
        
        # Verificar que el usuario se eliminó
        self.assertFalse(Usuario.objects.filter(id=usuario_id).exists())
        
        # Verificar mensaje de éxito
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Usuario eliminado con éxito")
    
    def test_delete_user_with_loans(self):
        """Test eliminar usuario con préstamos (debe fallar)"""
        # Crear un préstamo para el usuario
        from libros.models import Libro
        from prestamos.models import Prestamo
        from datetime import date
        
        libro = Libro.objects.create(
            titulo="Libro Test",
            autor="Autor Test",
            fecha_publicacion=date.today()
        )
        
        Prestamo.objects.create(
            usuario=self.usuario,
            libro=libro
        )
        
        usuario_id = self.usuario.id
        url = reverse('usuarios:eliminar_usuario', kwargs={'id': usuario_id})
        response = self.client.get(url)
        
        # Debe redirigir pero no eliminar
        self.assertEqual(response.status_code, 302)
        
        # Verificar que el usuario NO se eliminó
        self.assertTrue(Usuario.objects.filter(id=usuario_id).exists())
        
        # Verificar mensaje de advertencia
        messages = list(get_messages(response.wsgi_request))
        self.assertIn("no puede ser eliminado", str(messages[0]))
    
    def test_delete_user_not_found(self):
        """Test eliminar usuario que no existe"""
        url = reverse('usuarios:eliminar_usuario', kwargs={'id': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
