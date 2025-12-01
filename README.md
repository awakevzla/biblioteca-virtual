# Biblioteca Virtual - Sistema de Gestión de Libros

Sistema web desarrollado en Django para la gestión de una biblioteca virtual que permite administrar usuarios, libros y préstamos.

## 📋 Características

- **Gestión de Usuarios**: Registro, edición y administración de usuarios
- **Catálogo de Libros**: CRUD completo de libros con información detallada
- **Sistema de Préstamos**: Control de préstamos y devoluciones
- **Panel de Administración**: Interfaz administrativa de Django
- **Base de Datos**: PostgreSQL para almacenamiento robusto

## 🛠️ Tecnologías

- **Backend**: Django 4.2.26
- **Base de Datos**: PostgreSQL (con psycopg2-binary)
- **Frontend**: HTML, CSS, Django Templates
- **Containerización**: Docker & Docker Compose
- **Configuración**: python-dotenv para variables de entorno

## 📁 Estructura del Proyecto

```
biblioteca_virtual/
├── biblioteca_virtual/        # Configuración principal del proyecto
│   ├── settings.py           # Configuración de Django
│   ├── urls.py              # URLs principales
│   └── wsgi.py              # Configuración WSGI
├── usuarios/                 # App de gestión de usuarios
├── libros/                  # App de gestión de libros
├── prestamos/               # App de gestión de préstamos
├── templates/               # Templates globales
└── manage.py               # Comando de gestión de Django
```

## 🚀 Instalación y Ejecución

### Opción 1: Con Docker (Recomendado)

Esta es la forma más rápida y sencilla de ejecutar el proyecto:

1. **Prerrequisitos**
   - Docker
   - Docker Compose

2. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd django-curso-2
   ```

3. **Ejecutar con Docker**
   ```bash
   docker-compose up --build
   ```

4. **Acceder a la aplicación**
   - **Aplicación**: http://localhost:8000
   - **Admin**: http://localhost:8000/admin
     - Usuario: `admin`
     - Contraseña: `admin123`

5. **Detener los servicios**
   ```bash
   docker-compose down
   ```

> 📖 **Documentación completa de Docker**: Ver [README-Docker.md](README-Docker.md) para comandos adicionales y troubleshooting.

### Opción 2: Instalación Local

1. **Prerrequisitos**
   - Python 3.11+
   - PostgreSQL

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar base de datos**
   - Crear base de datos PostgreSQL llamada `biblioteca_virtual`
   - Copiar `.env.example` a `.env` y configurar variables

5. **Ejecutar migraciones**
   ```bash
   cd biblioteca_virtual
   python manage.py migrate
   ```

6. **Crear superusuario**
   ```bash
   python manage.py createsuperuser
   ```

7. **Ejecutar servidor**
   ```bash
   python manage.py runserver
   ```

## 🗃️ Configuración de Base de Datos

El proyecto está configurado para usar PostgreSQL. Las variables de entorno necesarias son:

```bash
DJANGO_SECRET_KEY=tu-clave-secreta
DEBUG=True
DB_ENGINE=django.db.backends.postgresql
DB_NAME=biblioteca_virtual
DB_USER=postgres
DB_PASSWORD=tu-password
DB_HOST=localhost
DB_PORT=5432
DB_TIMEOUT=20
```

## 🧪 Testing

El proyecto incluye un conjunto completo de tests unitarios para todos los componentes:

### Ejecutar Tests

**Con Docker:**
```bash
# Ejecutar todos los tests
docker-compose exec web python biblioteca_virtual/manage.py test

# Ejecutar tests específicos
docker-compose exec web python biblioteca_virtual/manage.py test usuarios
docker-compose exec web python biblioteca_virtual/manage.py test libros
docker-compose exec web python biblioteca_virtual/manage.py test prestamos

# Usar el script runner
docker-compose exec web bash run_tests.sh
```

**Instalación Local:**
```bash
# Ejecutar todos los tests
cd biblioteca_virtual
python manage.py test

# O usar el script runner
./run_tests.sh
```

### Cobertura de Tests

Los tests cubren:

- **Modelos**: Creación, validaciones, métodos y relaciones
- **Formularios**: Validación de datos y guardado
- **Vistas**: GET/POST, redirecciones, mensajes y manejo de errores
- **Integración**: Flujos completos de usuario

**Apps con tests:**
- `usuarios/tests.py` - 15+ casos de test
- `libros/tests.py` - 15+ casos de test  
- `prestamos/tests.py` - 15+ casos de test

### Coverage Report

Para generar un reporte de cobertura:

```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Genera reporte HTML en htmlcov/
```

## 📝 Apps del Proyecto

### 1. Usuarios
- Gestión de usuarios del sistema
- CRUD de perfiles de usuario
- Templates: `user_create.html`, `user_edit.html`, `users.html`

### 2. Libros
- Catálogo completo de libros
- Control de disponibilidad
- Templates: `create_libro.html`, `edit_libro.html`, `listar_libros.html`

### 3. Préstamos
- Sistema de préstamos y devoluciones
- Historial de préstamos por usuario
- Templates: `crear_prestamo.html`, `listar_prestamos.html`

## 🔧 Comandos Útiles

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Acceder al shell de Django
python manage.py shell

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor de desarrollo
python manage.py runserver
```

## 🐳 Docker

El proyecto incluye una configuración completa de Docker para desarrollo:

- **Dockerfile**: Imagen de Python 3.11 con dependencias
- **docker-compose.yml**: Orquestación de Django + PostgreSQL
- **entrypoint.sh**: Script de inicialización automática

Ver documentación completa en [README-Docker.md](README-Docker.md).

## 🔄 CI/CD

El proyecto incluye un pipeline simple de GitHub Actions que:

✅ **Se ejecuta automáticamente** en Pull Requests y commits a main/develop  
✅ **Configura PostgreSQL** para tests realistas  
✅ **Ejecuta todas las pruebas** del proyecto  
✅ **Valida las migraciones** de Django  

### **Configuración:**
1. Fork/clone el repositorio
2. Actualiza el badge en README.md con tu usuario/repo
3. ¡Listo! Los tests se ejecutarán automáticamente en PRs

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 📞 Soporte

Si tienes problemas con la configuración:

1. **Docker**: Consulta [README-Docker.md](README-Docker.md)
2. **Issues**: Abre un issue en este repositorio
3. **Logs**: Revisa los logs con `docker-compose logs` para Docker o los logs del servidor para instalación local
