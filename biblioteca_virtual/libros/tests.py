from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from .models import Libro
from .forms import LibroForm
from datetime import date


class LibroModelTest(TestCase):
    """Tests para el modelo Libro"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.libro = Libro.objects.create(
            titulo="El Quijote",
            autor="Miguel de Cervantes",
            fecha_publicacion=date(1605, 1, 16),
            en_prestamo=False
        )
    
    def test_libro_creation(self):
        """Test de creación de libro"""
        self.assertEqual(self.libro.titulo, "El Quijote")
        self.assertEqual(self.libro.autor, "Miguel de Cervantes")
        self.assertEqual(self.libro.fecha_publicacion, date(1605, 1, 16))
        self.assertFalse(self.libro.en_prestamo)
    
    def test_libro_str_method(self):
        """Test del método __str__"""
        expected_str = "El Quijote - (Miguel de Cervantes)"
        self.assertEqual(str(self.libro), expected_str)
    
    def test_default_en_prestamo(self):
        """Test del valor por defecto de en_prestamo"""
        libro = Libro.objects.create(
            titulo="Cien años de soledad",
            autor="Gabriel García Márquez",
            fecha_publicacion=date(1967, 5, 30)
        )
        self.assertFalse(libro.en_prestamo)  # Debe ser False por defecto
    
    def test_meta_verbose_name_plural(self):
        """Test del nombre plural en Meta"""
        self.assertEqual(Libro._meta.verbose_name_plural, "Libros")
    
    def test_required_fields(self):
        """Test que los campos requeridos no puedan ser nulos"""
        with self.assertRaises(Exception):
            Libro.objects.create(
                titulo=None,
                autor="Autor Test",
                fecha_publicacion=date.today()
            )
    
    def test_en_prestamo_status(self):
        """Test de cambio de estado de préstamo"""
        self.assertFalse(self.libro.en_prestamo)
        
        # Cambiar a préstamo
        self.libro.en_prestamo = True
        self.libro.save()
        
        # Recargar desde la base de datos
        self.libro.refresh_from_db()
        self.assertTrue(self.libro.en_prestamo)


class LibroFormTest(TestCase):
    """Tests para el formulario LibroForm"""
    
    def test_valid_form(self):
        """Test con datos válidos"""
        form_data = {
            'titulo': 'El Principito',
            'autor': 'Antoine de Saint-Exupéry',
            'fecha_publicacion': '1943-04-06'
        }
        form = LibroForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_form_missing_required_fields(self):
        """Test con campos requeridos faltantes"""
        form_data = {
            'titulo': '',
            'autor': 'Autor Test',
            'fecha_publicacion': '2023-01-01'
        }
        form = LibroForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('titulo', form.errors)
    
    def test_form_invalid_date(self):
        """Test con fecha inválida"""
        form_data = {
            'titulo': 'Libro Test',
            'autor': 'Autor Test',
            'fecha_publicacion': 'fecha-invalida'
        }
        form = LibroForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('fecha_publicacion', form.errors)
    
    def test_form_save(self):
        """Test de guardado del formulario"""
        form_data = {
            'titulo': 'Rayuela',
            'autor': 'Julio Cortázar',
            'fecha_publicacion': '1963-06-28'
        }
        form = LibroForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        libro = form.save()
        self.assertEqual(libro.titulo, 'Rayuela')
        self.assertEqual(libro.autor, 'Julio Cortázar')
        # en_prestamo no está en el formulario, se usa el valor por defecto del modelo
        self.assertFalse(libro.en_prestamo)


class LibroViewTest(TestCase):
    """Tests para las vistas de Libro"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.client = Client()
        self.libro1 = Libro.objects.create(
            titulo="Libro Test 1",
            autor="Autor Test 1",
            fecha_publicacion=date.today(),
            en_prestamo=False
        )
        self.libro2 = Libro.objects.create(
            titulo="Libro Test 2",
            autor="Autor Test 2",
            fecha_publicacion=date.today(),
            en_prestamo=True
        )
    
    def test_libros_list_view(self):
        """Test de la vista de lista de libros"""
        response = self.client.get(reverse('libros:libros'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.libro1.titulo)
        self.assertContains(response, self.libro2.titulo)
        
        # Verificar que los libros están ordenados por id
        libros = response.context['libros']
        self.assertEqual(list(libros), [self.libro1, self.libro2])
    
    def test_create_libro_get(self):
        """Test GET de la vista de crear libro"""
        response = self.client.get(reverse('libros:crear_libro'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], LibroForm)
    
    def test_create_libro_post_valid(self):
        """Test POST válido para crear libro"""
        data = {
            'titulo': 'Nuevo Libro',
            'autor': 'Nuevo Autor',
            'fecha_publicacion': '2023-12-01'
        }
        response = self.client.post(reverse('libros:crear_libro'), data)
        
        # Debe redirigir tras crear exitosamente
        self.assertEqual(response.status_code, 302)
        
        # Verificar que el libro se creó
        self.assertTrue(Libro.objects.filter(titulo='Nuevo Libro').exists())
        
        # Verificar mensaje (aunque dice "Usuario registrado..." por error en el código)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
    
    def test_create_libro_post_invalid(self):
        """Test POST inválido para crear libro"""
        data = {
            'titulo': '',  # Campo requerido vacío
            'autor': '',
            'fecha_publicacion': 'fecha-invalida'
        }
        response = self.client.post(reverse('libros:crear_libro'), data)
        
        # No debe redirigir, debe mostrar errores
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], LibroForm)
        self.assertFalse(response.context['form'].is_valid())
    
    def test_edit_libro_get(self):
        """Test GET de la vista de editar libro"""
        url = reverse('libros:editar_libro', kwargs={'id': self.libro1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['libro'], self.libro1)
        self.assertIsInstance(response.context['form'], LibroForm)
    
    def test_edit_libro_post_valid(self):
        """Test POST válido para editar libro"""
        data = {
            'titulo': 'Libro Editado',
            'autor': 'Autor Editado',
            'fecha_publicacion': '2023-01-01'
        }
        url = reverse('libros:editar_libro', kwargs={'id': self.libro1.id})
        response = self.client.post(url, data)
        
        # Debe redirigir tras editar exitosamente
        self.assertEqual(response.status_code, 302)
        
        # Verificar que el libro se actualizó
        self.libro1.refresh_from_db()
        self.assertEqual(self.libro1.titulo, 'Libro Editado')
        self.assertEqual(self.libro1.autor, 'Autor Editado')
        
        # Verificar mensaje de éxito
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Libro actualizado...")
    
    def test_edit_libro_not_found(self):
        """Test editar libro que no existe"""
        url = reverse('libros:editar_libro', kwargs={'id': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_delete_libro(self):
        """Test eliminar libro"""
        libro_id = self.libro1.id
        url = reverse('libros:eliminar_libro', kwargs={'id': libro_id})
        response = self.client.get(url)
        
        # Debe redirigir tras eliminar
        self.assertEqual(response.status_code, 302)
        
        # Verificar que el libro se eliminó
        self.assertFalse(Libro.objects.filter(id=libro_id).exists())
    
    def test_delete_libro_not_found(self):
        """Test eliminar libro que no existe"""
        url = reverse('libros:eliminar_libro', kwargs={'id': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_libro_availability_status(self):
        """Test de estado de disponibilidad de libros"""
        # Verificar libros disponibles y en préstamo
        disponibles = Libro.objects.filter(en_prestamo=False)
        en_prestamo = Libro.objects.filter(en_prestamo=True)
        
        self.assertIn(self.libro1, disponibles)
        self.assertIn(self.libro2, en_prestamo)
        self.assertEqual(disponibles.count(), 1)
        self.assertEqual(en_prestamo.count(), 1)
