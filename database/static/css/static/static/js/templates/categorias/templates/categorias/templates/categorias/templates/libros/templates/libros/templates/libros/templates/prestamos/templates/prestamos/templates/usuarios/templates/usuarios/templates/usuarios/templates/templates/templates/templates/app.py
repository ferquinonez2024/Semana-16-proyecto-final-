from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from datetime import datetime, date
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # Cambiar por una clave más segura

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Ajustar según tu configuración
    'database': 'biblioteca_db'
}

def get_db_connection():
    """Crear conexión a la base de datos"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as e:
        print(f"Error conectando a la base de datos: {e}")
        return None

def login_required(f):
    """Decorador para rutas que requieren autenticación"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ========== RUTAS DE AUTENTICACIÓN ==========

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login de usuarios"""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            user = cursor.fetchone()
            
            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['user_name'] = user['nombre']
                session['user_role'] = user['rol']
                flash('¡Bienvenido!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Email o contraseña incorrectos', 'error')
            
            cursor.close()
            conn.close()
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Cerrar sesión"""
    session.clear()
    flash('Sesión cerrada correctamente', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Panel principal después del login"""
    conn = get_db_connection()
    stats = {}
    
    if conn:
        cursor = conn.cursor()
        
        # Estadísticas básicas
        cursor.execute("SELECT COUNT(*) FROM libros")
        stats['total_libros'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE rol = 'usuario'")
        stats['total_usuarios'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM prestamos WHERE fecha_devolucion IS NULL")
        stats['prestamos_activos'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM categorias")
        stats['total_categorias'] = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
    
    return render_template('dashboard.html', stats=stats)

# ========== CRUD USUARIOS ==========

@app.route('/usuarios')
@login_required
def usuarios():
    """Listar todos los usuarios"""
    conn = get_db_connection()
    usuarios = []
    
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios ORDER BY nombre")
        usuarios = cursor.fetchall()
        cursor.close()
        conn.close()
    
    return render_template('usuarios/index.html', usuarios=usuarios)

@app.route('/usuarios/crear', methods=['GET', 'POST'])
@login_required
def crear_usuario():
    """Crear nuevo usuario"""
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        rol = request.form['rol']
        
        hashed_password = generate_password_hash(password)
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO usuarios (nombre, email, password, telefono, direccion, rol) VALUES (%s, %s, %s, %s, %s, %s)",
                    (nombre, email, hashed_password, telefono, direccion, rol)
                )
                conn.commit()
                flash('Usuario creado exitosamente', 'success')
                return redirect(url_for('usuarios'))
            except mysql.connector.Error as e:
                flash(f'Error al crear usuario: {e}', 'error')
            finally:
                cursor.close()
                conn.close()
    
    return render_template('usuarios/crear.html')

@app.route('/usuarios/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_usuario(id):
    """Editar usuario existente"""
    conn = get_db_connection()
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        rol = request.form['rol']
        
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "UPDATE usuarios SET nombre=%s, email=%s, telefono=%s, direccion=%s, rol=%s WHERE id=%s",
                    (nombre, email, telefono, direccion, rol, id)
                )
                conn.commit()
                flash('Usuario actualizado exitosamente', 'success')
                return redirect(url_for('usuarios'))
            except mysql.connector.Error as e:
                flash(f'Error al actualizar usuario: {e}', 'error')
            finally:
                cursor.close()
                conn.close()
    
    # GET request - mostrar formulario con datos actuales
    usuario = None
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()
    
    return render_template('usuarios/editar.html', usuario=usuario)

@app.route('/usuarios/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_usuario(id):
    """Eliminar usuario"""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
            conn.commit()
            flash('Usuario eliminado exitosamente', 'success')
        except mysql.connector.Error as e:
            flash(f'Error al eliminar usuario: {e}', 'error')
        finally:
            cursor.close()
            conn.close()
    
    return redirect(url_for('usuarios'))

# ========== CRUD CATEGORÍAS ==========

@app.route('/categorias')
@login_required
def categorias():
    """Listar todas las categorías"""
    conn = get_db_connection()
    categorias = []
    
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM categorias ORDER BY nombre")
        categorias = cursor.fetchall()
        cursor.close()
        conn.close()
    
    return render_template('categorias/index.html', categorias=categorias)

@app.route('/categorias/crear', methods=['GET', 'POST'])
@login_required
def crear_categoria():
    """Crear nueva categoría"""
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO categorias (nombre, descripcion) VALUES (%s, %s)",
                    (nombre, descripcion)
                )
                conn.commit()
                flash('Categoría creada exitosamente', 'success')
                return redirect(url_for('categorias'))
            except mysql.connector.Error as e:
                flash(f'Error al crear categoría: {e}', 'error')
            finally:
                cursor.close()
                conn.close()
    
    return render_template('categorias/crear.html')

@app.route('/categorias/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_categoria(id):
    """Editar categoría existente"""
    conn = get_db_connection()
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "UPDATE categorias SET nombre=%s, descripcion=%s WHERE id=%s",
                    (nombre, descripcion, id)
                )
                conn.commit()
                flash('Categoría actualizada exitosamente', 'success')
                return redirect(url_for('categorias'))
            except mysql.connector.Error as e:
                flash(f'Error al actualizar categoría: {e}', 'error')
            finally:
                cursor.close()
                conn.close()
    
    # GET request
    categoria = None
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM categorias WHERE id = %s", (id,))
        categoria = cursor.fetchone()
        cursor.close()
        conn.close()
    
    return render_template('categorias/editar.html', categoria=categoria)

@app.route('/categorias/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_categoria(id):
    """Eliminar categoría"""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM categorias WHERE id = %s", (id,))
            conn.commit()
            flash('Categoría eliminada exitosamente', 'success')
        except mysql.connector.Error as e:
            flash(f'Error al eliminar categoría: {e}', 'error')
        finally:
            cursor.close()
            conn.close()
    
    return redirect(url_for('categorias'))

# ========== CRUD LIBROS ==========

@app.route('/libros')
@login_required
def libros():
    """Listar todos los libros"""
    conn = get_db_connection()
    libros = []
    
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT l.*, c.nombre as categoria_nombre 
            FROM libros l 
            JOIN categorias c ON l.categoria_id = c.id 
            ORDER BY l.titulo
        """)
        libros = cursor.fetchall()
        cursor.close()
        conn.close()
    
    return render_template('libros/index.html', libros=libros)

@app.route('/libros/crear', methods=['GET', 'POST'])
@login_required
def crear_libro():
    """Crear nuevo libro"""
    conn = get_db_connection()
    categorias = []
    
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM categorias ORDER BY nombre")
        categorias = cursor.fetchall()
        
        if request.method == 'POST':
            titulo = request.form['titulo']
            autor = request.form['autor']
            isbn = request.form['isbn']
            categoria_id = request.form['categoria_id']
            año_publicacion = request.form['año_publicacion']
            editorial = request.form['editorial']
            cantidad_disponible = request.form['cantidad_disponible']
            
            try:
                cursor.execute(
                    "INSERT INTO libros (titulo, autor, isbn, categoria_id, año_publicacion, editorial, cantidad_disponible) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (titulo, autor, isbn, categoria_id, año_publicacion, editorial, cantidad_disponible)
                )
                conn.commit()
                flash('Libro creado exitosamente', 'success')
                return redirect(url_for('libros'))
            except mysql.connector.Error as e:
                flash(f'Error al crear libro: {e}', 'error')
        
        cursor.close()
        conn.close()
    
    return render_template('libros/crear.html', categorias=categorias)

@app.route('/libros/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_libro(id):
    """Editar libro existente"""
    conn = get_db_connection()
    libro = None
    categorias = []
    
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM categorias ORDER BY nombre")
        categorias = cursor.fetchall()
        
        if request.method == 'POST':
            titulo = request.form['titulo']
            autor = request.form['autor']
            isbn = request.form['isbn']
            categoria_id = request.form['categoria_id']
            año_publicacion = request.form['año_publicacion']
            editorial = request.form['editorial']
            cantidad_disponible = request.form['cantidad_disponible']
            
            try:
                cursor.execute(
                    "UPDATE libros SET titulo=%s, autor=%s, isbn=%s, categoria_id=%s, año_publicacion=%s, editorial=%s, cantidad_disponible=%s WHERE id=%s",
                    (titulo, autor, isbn, categoria_id, año_publicacion, editorial, cantidad_disponible, id)
                )
                conn.commit()
                flash('Libro actualizado exitosamente', 'success')
                return redirect(url_for('libros'))
            except mysql.connector.Error as e:
                flash(f'Error al actualizar libro: {e}', 'error')
        
        # GET request
        cursor.execute("SELECT * FROM libros WHERE id = %s", (id,))
        libro = cursor.fetchone()
        
        cursor.close()
        conn.close()
    
    return render_template('libros/editar.html', libro=libro, categorias=categorias)

@app.route('/libros/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_libro(id):
    """Eliminar libro"""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM libros WHERE id = %s", (id,))
            conn.commit()
            flash('Libro eliminado exitosamente', 'success')
        except mysql.connector.Error as e:
            flash(f'Error al eliminar libro: {e}', 'error')
        finally:
            cursor.close()
            conn.close()
    
    return redirect(url_for('libros'))

# ========== CRUD PRÉSTAMOS ==========

@app.route('/prestamos')
@login_required
def prestamos():
    """Listar todos los préstamos"""
    conn = get_db_connection()
    prestamos = []
    
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.*, u.nombre as usuario_nombre, l.titulo as libro_titulo
            FROM prestamos p
            JOIN usuarios u ON p.usuario_id = u.id
            JOIN libros l ON p.libro_id = l.id
            ORDER BY p.fecha_prestamo DESC
        """)
        prestamos = cursor.fetchall()
        cursor.close()
        conn.close()
    
    return render_template('prestamos/index.html', prestamos=prestamos)

@app.route('/prestamos/crear', methods=['GET', 'POST'])
@login_required
def crear_prestamo():
    """Crear nuevo préstamo"""
    conn = get_db_connection()
    usuarios = []
    libros = []
    
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE rol = 'usuario' ORDER BY nombre")
        usuarios = cursor.fetchall()
        
        cursor.execute("SELECT * FROM libros WHERE cantidad_disponible > 0 ORDER BY titulo")
        libros = cursor.fetchall()
        
        if request.method == 'POST':
            usuario_id = request.form['usuario_id']
            libro_id = request.form['libro_id']
            fecha_prestamo = datetime.now().date()
            
            try:
                # Crear préstamo
                cursor.execute(
                    "INSERT INTO prestamos (usuario_id, libro_id, fecha_prestamo) VALUES (%s, %s, %s)",
                    (usuario_id, libro_id, fecha_prestamo)
                )
                
                # Reducir cantidad disponible del libro
                cursor.execute(
                    "UPDATE libros SET cantidad_disponible = cantidad_disponible - 1 WHERE id = %s",
                    (libro_id,)
                )
                
                conn.commit()
                flash('Préstamo creado exitosamente', 'success')
                return redirect(url_for('prestamos'))
            except mysql.connector.Error as e:
                flash(f'Error al crear préstamo: {e}', 'error')
        
        cursor.close()
        conn.close()
    
    return render_template('prestamos/crear.html', usuarios=usuarios, libros=libros)

@app.route('/prestamos/<int:id>/devolver', methods=['POST'])
@login_required
def devolver_libro(id):
    """Marcar libro como devuelto"""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # Obtener información del préstamo
            cursor.execute("SELECT libro_id FROM prestamos WHERE id = %s", (id,))
            resultado = cursor.fetchone()
            
            if resultado:
                libro_id = resultado[0]
                fecha_devolucion = datetime.now().date()
                
                # Actualizar préstamo
                cursor.execute(
                    "UPDATE prestamos SET fecha_devolucion = %s WHERE id = %s",
                    (fecha_devolucion, id)
                )
                
                # Aumentar cantidad disponible del libro
                cursor.execute(
                    "UPDATE libros SET cantidad_disponible = cantidad_disponible + 1 WHERE id = %s",
                    (libro_id,)
                )
                
                conn.commit()
                flash('Libro devuelto exitosamente', 'success')
            else:
                flash('Préstamo no encontrado', 'error')
                
        except mysql.connector.Error as e:
            flash(f'Error al devolver libro: {e}', 'error')
        finally:
            cursor.close()
            conn.close()
    
    return redirect(url_for('prestamos'))

if __name__ == '__main__':
    app.run(debug=True)
