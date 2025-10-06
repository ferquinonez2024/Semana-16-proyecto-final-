# 🛠️ Guía de Instalación - Sistema de Gestión de Biblioteca

## 📋 Requisitos Previos

Antes de instalar el sistema, asegúrate de tener:

- **Python 3.8+** instalado
- **MySQL 8.0+** instalado y ejecutándose
- **pip** (gestor de paquetes de Python)
- **Git** para clonar el repositorio

## 🚀 Instalación Paso a Paso

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/sistema-biblioteca.git
cd sistema-biblioteca
```

### 2. Crear Entorno Virtual

**En Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**En Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar MySQL

#### 4.1 Crear la Base de Datos

```sql
-- Conectarse a MySQL como root
mysql -u root -p

-- Crear la base de datos
CREATE DATABASE biblioteca_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Crear usuario específico (opcional pero recomendado)
CREATE USER 'biblioteca_user'@'localhost' IDENTIFIED BY 'tu_password_aqui';
GRANT ALL PRIVILEGES ON biblioteca_db.* TO 'biblioteca_user'@'localhost';
FLUSH PRIVILEGES;

-- Salir de MySQL
EXIT;
```

#### 4.2 Ejecutar el Script de Creación

```bash
# Importar el script SQL
mysql -u root -p biblioteca_db < database/biblioteca_db.sql
```

### 5. Configurar la Aplicación

#### 5.1 Editar Configuración de Base de Datos

Abrir `app.py` y modificar la configuración de la base de datos:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'tu_usuario_mysql',      # Cambiar por tu usuario
    'password': 'tu_password_mysql',  # Cambiar por tu contraseña
    'database': 'biblioteca_db'
}
```

#### 5.2 Configurar Variables de Entorno (Opcional)

Crear archivo `.env` en la raíz del proyecto:

```env
FLASK_ENV=development
DB_HOST=localhost
DB_USER=biblioteca_user
DB_PASSWORD=tu_password_aqui
DB_NAME=biblioteca_db
SECRET_KEY=tu_clave_secreta_muy_segura
```

### 6. Verificar la Instalación

#### 6.1 Probar Conexión a la Base de Datos

```bash
python -c "from app import get_db_connection; conn = get_db_connection(); print('✅ Conexión exitosa' if conn else '❌ Error de conexión')"
```

#### 6.2 Ejecutar la Aplicación

```bash
python run.py
```

### 7. Acceder al Sistema

1. Abrir navegador en: `http://localhost:5000`
2. Usar credenciales de prueba:
   - **Admin**: admin@biblioteca.com / admin123
   - **Bibliotecario**: maria.bibliotecaria@biblioteca.com / biblio123
   - **Usuario**: juan.perez@email.com / user123

## 🔧 Solución de Problemas Comunes

### Error: "No module named 'mysql.connector'"

```bash
pip install mysql-connector-python
```

### Error: "Access denied for user"

1. Verificar usuario y contraseña en `app.py`
2. Asegurarse de que MySQL esté ejecutándose
3. Verificar permisos del usuario en MySQL

### Error: "Unknown database 'biblioteca_db'"

```sql
-- Crear la base de datos
mysql -u root -p
CREATE DATABASE biblioteca_db;
```

### Error: "Port 5000 already in use"

```bash
# Cambiar puerto en run.py o usar:
FLASK_RUN_PORT=5001 python run.py
```

### Error de Codificación de Caracteres

1. Asegurarse de que MySQL use UTF8MB4
2. Verificar que los archivos tengan codificación UTF-8

## 🏗️ Configuración para Producción

### 1. Configurar Variables de Entorno

```bash
export FLASK_ENV=production
export SECRET_KEY="clave_super_secreta_para_produccion"
export DB_HOST="servidor_mysql"
export DB_USER="usuario_produccion"
export DB_PASSWORD="password_seguro"
```

### 2. Usar un Servidor WSGI

```bash
# Instalar Gunicorn
pip install gunicorn

# Ejecutar con Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### 3. Configurar Nginx (Opcional)

```nginx
server {
    listen 80;
    server_name tu-dominio.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /static {
        alias /path/to/sistema-biblioteca/static;
    }
}
```

## 📚 Datos de Prueba

El sistema incluye datos de prueba:

- **5 usuarios** (1 admin, 1 bibliotecario, 3 usuarios)
- **10 categorías** de libros
- **15 libros** de ejemplo
- **6 préstamos** (3 activos, 3 devueltos)

## 🔄 Actualizaciones

### Actualizar el Sistema

```bash
git pull origin main
pip install -r requirements.txt
# Ejecutar nuevos scripts de BD si los hay
```

### Backup de la Base de Datos

```bash
mysqldump -u root -p biblioteca_db > backup_biblioteca_$(date +%Y%m%d).sql
```

### Restaurar Backup

```bash
mysql -u root -p biblioteca_db < backup_biblioteca_20251006.sql
```

## 📞 Soporte

Si tienes problemas con la instalación:

1. Verificar que todos los requisitos estén instalados
2. Revisar los logs de error en la consola
3. Comprobar la configuración de la base de datos
4. Asegurarse de que los puertos no estén ocupados

## ✅ Lista de Verificación Post-Instalación

- [ ] Python 3.8+ instalado
- [ ] MySQL ejecutándose
- [ ] Base de datos creada
- [ ] Dependencias instaladas
- [ ] Configuración de BD correcta
- [ ] Aplicación ejecutándose
- [ ] Login funcionando
- [ ] CRUD operativo

¡Listo! El sistema debe estar funcionando correctamente. 🎉
