#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de verificación para el Sistema de Gestión de Biblioteca
Autor: MiniMax Agent
Fecha: 2025-10-06

Este script verifica que todos los componentes del sistema estén funcionando correctamente.
"""

import os
import sys
import mysql.connector
from datetime import datetime

def print_header(title):
    """Imprimir encabezado con formato"""
    print("\n" + "="*60)
    print(f"🔍 {title}")
    print("="*60)

def print_check(description, status, details=""):
    """Imprimir resultado de verificación"""
    icon = "✅" if status else "❌"
    print(f"{icon} {description}")
    if details:
        print(f"   📝 {details}")

def check_python_version():
    """Verificar versión de Python"""
    print_header("VERIFICACIÓN DE PYTHON")
    
    version = sys.version_info
    required_version = (3, 8)
    
    is_valid = version >= required_version
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    print_check(
        f"Versión de Python: {version_str}",
        is_valid,
        f"Requerido: Python {required_version[0]}.{required_version[1]}+"
    )
    
    return is_valid

def check_dependencies():
    """Verificar dependencias instaladas"""
    print_header("VERIFICACIÓN DE DEPENDENCIAS")
    
    dependencies = [
        ("Flask", "flask"),
        ("MySQL Connector", "mysql.connector"), 
        ("Werkzeug", "werkzeug.security")
    ]
    
    all_ok = True
    
    for name, module in dependencies:
        try:
            __import__(module)
            print_check(f"{name}", True, "Instalado correctamente")
        except ImportError:
            print_check(f"{name}", False, "No instalado")
            all_ok = False
    
    return all_ok

def check_files_structure():
    """Verificar estructura de archivos"""
    print_header("VERIFICACIÓN DE ESTRUCTURA DE ARCHIVOS")
    
    required_files = [
        "app.py",
        "run.py", 
        "requirements.txt",
        "README.md",
        "database/biblioteca_db.sql",
        "templates/base.html",
        "templates/login.html",
        "templates/dashboard.html",
        "static/css/custom.css",
        "static/js/biblioteca.js"
    ]
    
    required_dirs = [
        "templates",
        "templates/usuarios",
        "templates/categorias", 
        "templates/libros",
        "templates/prestamos",
        "static",
        "static/css",
        "static/js",
        "database"
    ]
    
    all_ok = True
    
    # Verificar directorios
    for directory in required_dirs:
        exists = os.path.exists(directory)
        print_check(f"Directorio: {directory}", exists)
        if not exists:
            all_ok = False
    
    # Verificar archivos
    for file_path in required_files:
        exists = os.path.exists(file_path)
        print_check(f"Archivo: {file_path}", exists)
        if not exists:
            all_ok = False
    
    return all_ok

def check_database_connection():
    """Verificar conexión a la base de datos"""
    print_header("VERIFICACIÓN DE BASE DE DATOS")
    
    try:
        # Importar configuración desde app.py
        sys.path.append('.')
        from app import DB_CONFIG
        
        # Intentar conexión
        connection = mysql.connector.connect(**DB_CONFIG)
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Verificar que la base de datos existe
            cursor.execute("SELECT DATABASE()")
            db_name = cursor.fetchone()[0]
            print_check(f"Conexión a MySQL", True, f"Base de datos: {db_name}")
            
            # Verificar tablas requeridas
            required_tables = ['usuarios', 'categorias', 'libros', 'prestamos']
            cursor.execute("SHOW TABLES")
            existing_tables = [table[0] for table in cursor.fetchall()]
            
            for table in required_tables:
                exists = table in existing_tables
                print_check(f"Tabla: {table}", exists)
                
                if exists:
                    # Contar registros
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    print_check(f"  Registros en {table}", count > 0, f"{count} registros")
            
            cursor.close()
            connection.close()
            return True
            
    except mysql.connector.Error as e:
        print_check("Conexión a MySQL", False, f"Error: {e}")
        return False
    except Exception as e:
        print_check("Conexión a MySQL", False, f"Error inesperado: {e}")
        return False

def check_app_configuration():
    """Verificar configuración de la aplicación"""
    print_header("VERIFICACIÓN DE CONFIGURACIÓN")
    
    try:
        from app import app, DB_CONFIG
        
        # Verificar configuración de Flask
        print_check("Aplicación Flask", True, "Configurada correctamente")
        print_check("Secret Key", bool(app.secret_key), "Configurada")
        
        # Verificar configuración de BD
        required_config = ['host', 'user', 'database']
        config_ok = all(key in DB_CONFIG for key in required_config)
        print_check("Configuración de BD", config_ok)
        
        return config_ok
        
    except Exception as e:
        print_check("Configuración de la app", False, f"Error: {e}")
        return False

def test_basic_functionality():
    """Probar funcionalidad básica del sistema"""
    print_header("PRUEBA DE FUNCIONALIDAD BÁSICA")
    
    try:
        from app import get_db_connection
        
        conn = get_db_connection()
        if not conn:
            print_check("Conexión de prueba", False, "No se pudo conectar")
            return False
        
        cursor = conn.cursor(dictionary=True)
        
        # Probar consulta de usuarios
        cursor.execute("SELECT COUNT(*) as count FROM usuarios")
        users_count = cursor.fetchone()['count']
        print_check(f"Usuarios en sistema", users_count > 0, f"{users_count} usuarios")
        
        # Probar consulta de libros
        cursor.execute("SELECT COUNT(*) as count FROM libros")
        books_count = cursor.fetchone()['count']
        print_check(f"Libros en catálogo", books_count > 0, f"{books_count} libros")
        
        # Probar consulta con JOIN
        cursor.execute("""
            SELECT COUNT(*) as count 
            FROM libros l 
            JOIN categorias c ON l.categoria_id = c.id
        """)
        join_count = cursor.fetchone()['count']
        print_check("Relaciones entre tablas", join_count > 0, "JOINs funcionando")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print_check("Funcionalidad básica", False, f"Error: {e}")
        return False

def generate_report():
    """Generar reporte de verificación"""
    print_header("RESUMEN DE VERIFICACIÓN")
    
    checks = [
        ("Python", check_python_version()),
        ("Dependencias", check_dependencies()),
        ("Estructura de archivos", check_files_structure()),
        ("Base de datos", check_database_connection()),
        ("Configuración", check_app_configuration()),
        ("Funcionalidad", test_basic_functionality())
    ]
    
    passed = sum(1 for _, status in checks if status)
    total = len(checks)
    
    print(f"\n📊 RESULTADO: {passed}/{total} verificaciones pasaron")
    
    if passed == total:
        print("🎉 ¡SISTEMA COMPLETAMENTE FUNCIONAL!")
        print("\n💡 Para iniciar el sistema ejecuta:")
        print("   python run.py")
        print("\n🌐 Luego abre: http://localhost:5000")
        print("\n👤 Credenciales de prueba:")
        print("   Admin: admin@biblioteca.com / admin123")
    else:
        print("⚠️  SISTEMA CON PROBLEMAS")
        print("\n🔧 Revisa los errores marcados arriba")
        print("📖 Consulta INSTALL.md para instrucciones detalladas")
    
    return passed == total

def main():
    """Función principal"""
    print("🔍 VERIFICADOR DEL SISTEMA DE GESTIÓN DE BIBLIOTECA")
    print(f"📅 Ejecutado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        system_ok = generate_report()
        sys.exit(0 if system_ok else 1)
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Verificación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado durante la verificación: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
