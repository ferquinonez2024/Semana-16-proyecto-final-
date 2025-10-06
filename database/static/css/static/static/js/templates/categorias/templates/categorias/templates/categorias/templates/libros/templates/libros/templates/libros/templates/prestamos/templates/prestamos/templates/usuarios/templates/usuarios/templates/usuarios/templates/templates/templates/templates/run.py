#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de ejecución para el Sistema de Gestión de Biblioteca
Autor: MiniMax Agent
Fecha: 2025-10-06
"""

import os
import sys
from app import app

def main():
    """
    Función principal para ejecutar la aplicación Flask
    """
    try:
        # Configuración para desarrollo
        app.config['ENV'] = 'development'
        app.config['DEBUG'] = True
        
        # Configurar host y puerto
        host = os.environ.get('HOST', '127.0.0.1')
        port = int(os.environ.get('PORT', 5000))
        
        print("="*60)
        print("📚 SISTEMA DE GESTIÓN DE BIBLIOTECA")
        print("="*60)
        print(f"🌐 Servidor iniciando en: http://{host}:{port}")
        print("📝 Modo: Desarrollo (DEBUG=True)")
        print("⚡ Recarga automática: Activada")
        print("="*60)
        print("\n🔑 USUARIOS DE PRUEBA:")
        print("┌─────────────────────────────────────────────┐")
        print("│ ADMINISTRADOR:                              │")
        print("│ Email: admin@biblioteca.com                 │")
        print("│ Password: admin123                          │")
        print("├─────────────────────────────────────────────┤")
        print("│ BIBLIOTECARIO:                              │")
        print("│ Email: maria.bibliotecaria@biblioteca.com   │")
        print("│ Password: biblio123                         │")
        print("├─────────────────────────────────────────────┤")
        print("│ USUARIO:                                    │")
        print("│ Email: juan.perez@email.com                 │")
        print("│ Password: user123                           │")
        print("└─────────────────────────────────────────────┘")
        print("\n💡 Presiona Ctrl+C para detener el servidor")
        print("="*60)
        
        # Iniciar la aplicación
        app.run(
            host=host,
            port=port,
            debug=True,
            use_reloader=True,
            use_debugger=True
        )
        
    except KeyboardInterrupt:
        print("\n\n🛑 Servidor detenido por el usuario")
        print("👋 ¡Gracias por usar el Sistema de Biblioteca!")
        sys.exit(0)
        
    except Exception as e:
        print(f"\n❌ Error al iniciar el servidor: {e}")
        print("\n🔧 SOLUCIONES POSIBLES:")
        print("1. Verificar que MySQL esté ejecutándose")
        print("2. Comprobar la configuración de la base de datos en app.py")
        print("3. Ejecutar el script SQL: database/biblioteca_db.sql")
        print("4. Instalar dependencias: pip install -r requirements.txt")
        sys.exit(1)

def check_dependencies():
    """
    Verificar que las dependencias estén instaladas
    """
    try:
        import flask
        import mysql.connector
        from werkzeug.security import generate_password_hash
    except ImportError as e:
        print(f"❌ Error: Dependencia faltante - {e}")
        print("\n📦 Para instalar las dependencias ejecuta:")
        print("pip install -r requirements.txt")
        sys.exit(1)

def check_database_connection():
    """
    Verificar conexión a la base de datos
    """
    try:
        from app import get_db_connection
        conn = get_db_connection()
        if conn:
            conn.close()
            print("✅ Conexión a la base de datos: OK")
        else:
            print("⚠️  Advertencia: No se pudo conectar a la base de datos")
            print("   El servidor se iniciará, pero necesitarás configurar MySQL")
    except Exception as e:
        print(f"⚠️  Advertencia: Error de conexión a BD - {e}")
        print("   Asegúrate de que MySQL esté ejecutándose y la BD esté creada")

if __name__ == '__main__':
    # Verificaciones previas
    check_dependencies()
    check_database_connection()
    
    # Iniciar aplicación
    main()
