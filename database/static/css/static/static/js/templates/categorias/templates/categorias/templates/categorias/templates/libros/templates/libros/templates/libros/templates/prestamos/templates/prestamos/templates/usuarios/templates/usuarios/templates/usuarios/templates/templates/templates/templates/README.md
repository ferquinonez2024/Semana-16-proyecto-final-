# 📚 Sistema de Gestión de Biblioteca

## Descripción del Proyecto
Sistema web desarrollado en Flask para la gestión completa de una biblioteca. Incluye funcionalidades de autenticación, CRUD completo para múltiples entidades relacionadas y una interfaz web intuitiva.

## 🚀 Características Principales

### Funcionalidades Implementadas
- ✅ **Sistema de Autenticación**: Login/logout seguro con hash de contraseñas
- ✅ **CRUD Completo de Usuarios**: Crear, leer, actualizar y eliminar usuarios
- ✅ **CRUD Completo de Categorías**: Gestión de categorías de libros
- ✅ **CRUD Completo de Libros**: Administración del catálogo de libros
- ✅ **CRUD Completo de Préstamos**: Control de préstamos y devoluciones
- ✅ **Dashboard con Estadísticas**: Panel principal con métricas importantes
- ✅ **Interfaz Responsiva**: Diseño moderno con Bootstrap

### Tecnologías Utilizadas
- **Backend**: Flask (Python)
- **Base de Datos**: MySQL
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Autenticación**: Werkzeug Security

## 📊 Estructura de la Base de Datos

### Tablas Relacionadas
1. **usuarios**: Información de usuarios del sistema
2. **categorias**: Categorías de libros (ficción, ciencia, etc.)
3. **libros**: Catálogo de libros (relacionado con categorías)
4. **prestamos**: Registro de préstamos (relacionado con usuarios y libros)

### Relaciones
- `libros.categoria_id` → `categorias.id` (Muchos a Uno)
- `prestamos.usuario_id` → `usuarios.id` (Muchos a Uno)
- `prestamos.libro_id` → `libros.id` (Muchos a Uno)

## 🛠️ Instalación y Configuración

### Prerrequisitos
- Python 3.8+
- MySQL 8.0+
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/sistema-biblioteca.git
cd sistema-biblioteca
```

2. **Crear entorno virtual**
```bash
python -m venv venv

# En Windows
venv\Scripts\activate

# En Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar la base de datos**
- Crear una base de datos MySQL llamada `biblioteca_db`
- Ejecutar el script SQL ubicado en `database/biblioteca_db.sql`
- Ajustar las credenciales de conexión en `app.py` (líneas 14-19)

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'tu_usuario',
    'password': 'tu_contraseña',
    'database': 'biblioteca_db'
}
```

5. **Ejecutar la aplicación**
```bash
python app.py
```

6. **Acceder a la aplicación**
- Abrir navegador en: `http://localhost:5000`
- Usar credenciales de prueba:
  - **Email**: admin@biblioteca.com
  - **Contraseña**: admin123

## 📱 Uso de la Aplicación

### Panel de Administración
1. **Login**: Autenticación segura para acceder al sistema
2. **Dashboard**: Vista general con estadísticas importantes
3. **Gestión de Usuarios**: CRUD completo para administrar usuarios
4. **Gestión de Categorías**: Administrar categorías de libros
5. **Gestión de Libros**: Catálogo completo con información detallada
6. **Gestión de Préstamos**: Control de préstamos y devoluciones

### Funcionalidades por Módulo

#### 👥 Usuarios
- Crear nuevos usuarios (bibliotecarios y lectores)
- Editar información personal
- Eliminar usuarios
- Listar todos los usuarios

#### 📂 Categorías
- Crear categorías de libros
- Editar nombres y descripciones
- Eliminar categorías
- Visualizar todas las categorías

#### 📖 Libros
- Agregar nuevos libros al catálogo
- Editar información (título, autor, ISBN, etc.)
- Asignar categorías
- Control de inventario (cantidad disponible)
- Eliminar libros

#### 📋 Préstamos
- Registrar nuevos préstamos
- Marcar devoluciones
- Historial completo de préstamos
- Control automático de disponibilidad

## 🗂️ Estructura del Proyecto

```
sistema-biblioteca/
│
├── app.py                 # Aplicación principal Flask
├── requirements.txt       # Dependencias del proyecto
├── README.md             # Documentación
│
├── database/
│   └── biblioteca_db.sql  # Script de creación de BD
│
├── templates/            # Plantillas HTML
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── dashboard.html
│   ├── usuarios/
│   ├── categorias/
│   ├── libros/
│   └── prestamos/
│
└── static/              # Archivos estáticos
    ├── css/
    ├── js/
    └── img/
```

## 🎯 Características Técnicas

### Seguridad
- Contraseñas hasheadas con Werkzeug
- Protección de rutas con decorador `@login_required`
- Validación de sesiones
- Prevención de inyección SQL con consultas parametrizadas

### Base de Datos
- Relaciones correctas entre tablas
- Integridad referencial
- Índices para optimización
- Datos de prueba incluidos

### Frontend
- Diseño responsivo con Bootstrap 5
- Interfaz intuitiva y moderna
- Mensajes flash para feedback del usuario
- Formularios validados

## 🚀 Demostración

### Para Presentación en Clase
1. **Mostrar el login** con credenciales de prueba
2. **Navegar por el dashboard** explicando las estadísticas
3. **Demostrar CRUD completo**:
   - Crear una nueva categoría
   - Agregar un libro a esa categoría
   - Crear un usuario
   - Realizar un préstamo
   - Devolver el libro
4. **Mostrar las relaciones** entre tablas en la interfaz
5. **Explicar la estructura** del código y la base de datos

### Video Alternativo (3-5 minutos)
Si necesitas grabar un video, incluye:
1. **Introducción** (30 seg): Explicar qué es el sistema
2. **Login y navegación** (1 min): Mostrar autenticación y dashboard
3. **CRUD en acción** (2-3 min): Demostrar todas las operaciones
4. **Conclusión** (30 seg): Resaltar características técnicas

## 📝 Notas para el Desarrollador

### Configuración de Desarrollo
- Debug mode activado en `app.py`
- Cambiar `secret_key` por una más segura en producción
- Ajustar configuración de BD según tu entorno

### Posibles Mejoras Futuras
- Paginación en listas largas
- Búsqueda y filtros avanzados
- Reportes en PDF
- API REST
- Sistema de multas

## 👨‍💻 Autor
**MiniMax Agent**
- Proyecto desarrollado para demostración académica
- Sistema completo con todas las funcionalidades requeridas

---

### 📞 Soporte
Para dudas o problemas con la instalación, revisar:
1. Configuración de la base de datos
2. Instalación de dependencias
3. Permisos de Python y MySQL

**¡Listo para presentar! 🎉**
