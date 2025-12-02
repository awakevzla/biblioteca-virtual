#!/bin/bash

# Script para ejecutar tests del proyecto Biblioteca Virtual

echo "🧪 Ejecutando tests del proyecto Biblioteca Virtual"
echo "=================================================="

# Navegar al directorio del proyecto Django
cd biblioteca_virtual

echo ""
echo "📋 Resumen de tests:"
echo "- Usuarios: Models, Forms, Views"
echo "- Libros: Models, Forms, Views"  
echo "- Préstamos: Models, Forms, Views"
echo ""

# Ejecutar todos los tests con verbose
echo "▶️  Ejecutando todos los tests..."
python manage.py test --verbosity=2

# Verificar si los tests pasaron
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Todos los tests pasaron exitosamente!"
    echo ""
    echo "📊 Para ver coverage, instala coverage y ejecuta:"
    echo "   pip install coverage"
    echo "   coverage run --source='.' manage.py test"
    echo "   coverage report"
    echo "   coverage html  # Para reporte HTML"
else
    echo ""
    echo "❌ Algunos tests fallaron. Revisa los errores arriba."
    exit 1
fi

echo ""
echo "🔍 Comandos útiles para testing:"
echo "  python manage.py test usuarios                    # Solo tests de usuarios"
echo "  python manage.py test libros                      # Solo tests de libros"
echo "  python manage.py test prestamos                   # Solo tests de préstamos"
echo "  python manage.py test usuarios.tests.UsuarioModelTest  # Test específico"
echo "  python manage.py test --keepdb                    # Mantener DB de test"
echo "  python manage.py test --debug-mode                # Modo debug"
