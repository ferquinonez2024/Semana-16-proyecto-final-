# -*- coding: utf-8 -*-
"""
Archivo de configuración para el Sistema de Gestión de Biblioteca
Autor: MiniMax Agent
Fecha: 2025-10-06
"""

import os
from datetime import timedelta

class Config:
    """
    Configuración base de la aplicación
    """
    # Configuración básica de Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tu_clave_secreta_muy_segura_aqui_2025'
    
    # Configuración de la base de datos
    DB_HOST = os.environ.get('DB_HOST') or 'localhost'
    DB_USER = os.environ.get('DB_USER') or 'root'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or ''
    DB_NAME = os.environ.get('DB_NAME') or 'biblioteca_db'
    DB_PORT = int(os.environ.get('DB_PORT', 3306))
    
    # Configuración de sesiones
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    
    # Configuración de seguridad
    WTF_CSRF_ENABLED = True
    
    # Configuración de uploads (si se implementa en el futuro)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
    UPLOAD_FOLDER = 'static/uploads'
    
    # Configuración de paginación
    POSTS_PER_PAGE = 10
    
    @staticmethod
    def get_db_config():
        """
        Retorna la configuración de la base de datos como diccionario
        """
        return {
            'host': Config.DB_HOST,
            'user': Config.DB_USER,
            'password': Config.DB_PASSWORD,
            'database': Config.DB_NAME,
            'port': Config.DB_PORT,
            'charset': 'utf8mb4',
            'autocommit': False
        }

class DevelopmentConfig(Config):
    """
    Configuración para el entorno de desarrollo
    """
    DEBUG = True
    ENV = 'development'
    
class ProductionConfig(Config):
    """
    Configuración para el entorno de producción
    """
    DEBUG = False
    ENV = 'production'
    
    # En producción, usar variables de entorno obligatoriamente
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for production environment")

class TestingConfig(Config):
    """
    Configuración para testing
    """
    TESTING = True
    DEBUG = True
    DB_NAME = 'biblioteca_test_db'
    WTF_CSRF_ENABLED = False

# Diccionario de configuraciones
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# Configuración actual basada en variable de entorno
current_config = config.get(os.environ.get('FLASK_ENV', 'default'))
