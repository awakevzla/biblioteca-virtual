# Biblioteca Virtual - Configuración Docker (Desarrollo)

Este proyecto Django ha sido dockerizado con PostgreSQL como base de datos para desarrollo.

## Prerrequisitos

- Docker
- Docker Compose

## Inicio Rápido

1. **Navegar al directorio del proyecto**
   ```bash
   cd django-curso-2
   ```

2. **Construir y ejecutar con docker-compose**
   ```bash
   docker-compose up --build
   ```

3. **Acceder a la aplicación**
   - Aplicación Django: http://localhost:8000
   - Interfaz de administración: http://localhost:8000/admin (admin/admin123)
   - PostgreSQL: localhost:5432

## Comandos Útiles

```bash
# Iniciar servicios
docker-compose up

# Iniciar en segundo plano
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down

# Reconstruir e iniciar
docker-compose up --build
```

## Operaciones de Base de Datos

```bash
# Acceder al shell de Django
docker-compose exec web python biblioteca_virtual/manage.py shell

# Ejecutar migraciones
docker-compose exec web python biblioteca_virtual/manage.py migrate

# Crear superusuario
docker-compose exec web python biblioteca_virtual/manage.py createsuperuser

# Acceder a PostgreSQL
docker-compose exec db psql -U postgres -d biblioteca_virtual
```

## Limpieza

```bash
# Detener y remover contenedores, redes
docker-compose down

# Remover volúmenes (ADVERTENCIA: Esto eliminará tus datos)
docker-compose down -v

# Remover imágenes
docker-compose down --rmi all
```

## Estructura del Proyecto

```
.
├── Dockerfile                 # Contenedor de la aplicación Django
├── docker-compose.yml        # Configuración de desarrollo
├── entrypoint.sh             # Script de inicialización del contenedor
├── .dockerignore             # Archivos a excluir del build de Docker
└── biblioteca_virtual/       # Proyecto Django
```

## Solución de Problemas

### Problemas de Conexión a Base de Datos
- Asegurar que el contenedor de PostgreSQL esté saludable: `docker-compose ps`
- Revisar logs: `docker-compose logs db`

### Problemas de Permisos
- El contenedor corre como usuario no-root `appuser`
- Si encuentras problemas de permisos, verifica la propiedad de archivos

### Conflictos de Puerto
- Si el puerto 8000 o 5432 está en uso, modifica los puertos en docker-compose.yml

## Notas

- El script entrypoint ejecuta automáticamente las migraciones y crea un superusuario por defecto (admin/admin123)
- Los datos se mantienen persistentes en volúmenes de Docker
- Todas las variables de entorno están configuradas directamente en docker-compose.yml
