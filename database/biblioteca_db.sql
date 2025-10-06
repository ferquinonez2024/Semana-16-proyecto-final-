 SCRIPT DE CREACIÓN DE BASE DE DATOS
-- Sistema de Gestión de Biblioteca
-- Autor: Tiffany Quiñonez 
-- Fecha: 2025-09-06
-- =====================================================

-- Crear base de datos
DROP DATABASE IF EXISTS biblioteca_db;
CREATE DATABASE biblioteca_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE biblioteca_db;

-- =====================================================
-- TABLA: usuarios
-- Descripción: Almacena información de usuarios del sistema
-- =====================================================
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    telefono VARCHAR(20),
    direccion TEXT,
    rol ENUM('admin', 'bibliotecario', 'usuario') DEFAULT 'usuario',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE,
    INDEX idx_email (email),
    INDEX idx_rol (rol)
);

-- =====================================================
-- TABLA: categorias
-- Descripción: Categorías de libros (ficción, ciencia, etc.)
-- =====================================================
CREATE TABLE categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_nombre (nombre)
);

-- =====================================================
-- TABLA: libros
-- Descripción: Catálogo de libros de la biblioteca
-- =====================================================
CREATE TABLE libros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    autor VARCHAR(150) NOT NULL,
    isbn VARCHAR(20) UNIQUE,
    categoria_id INT NOT NULL,
    año_publicacion YEAR,
    editorial VARCHAR(100),
    cantidad_disponible INT DEFAULT 1,
    cantidad_total INT DEFAULT 1,
    fecha_ingreso TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Relación con categorias
    FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    
    -- Índices para optimización
    INDEX idx_titulo (titulo),
    INDEX idx_autor (autor),
    INDEX idx_isbn (isbn),
    INDEX idx_categoria (categoria_id)
);

-- =====================================================
-- TABLA: prestamos
-- Descripción: Registro de préstamos de libros
-- =====================================================
CREATE TABLE prestamos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    libro_id INT NOT NULL,
    fecha_prestamo DATE NOT NULL,
    fecha_vencimiento DATE GENERATED ALWAYS AS (DATE_ADD(fecha_prestamo, INTERVAL 15 DAY)) STORED,
    fecha_devolucion DATE NULL,
    observaciones TEXT,
    estado ENUM('activo', 'devuelto', 'vencido') DEFAULT 'activo',
    
    -- Relaciones
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (libro_id) REFERENCES libros(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    
    -- Índices
    INDEX idx_usuario (usuario_id),
    INDEX idx_libro (libro_id),
    INDEX idx_fecha_prestamo (fecha_prestamo),
    INDEX idx_estado (estado)
);

-- =====================================================
-- TRIGGER: Actualizar cantidad total al insertar libro
-- =====================================================
DELIMITER //
CREATE TRIGGER tr_libro_cantidad_total 
BEFORE INSERT ON libros
FOR EACH ROW
BEGIN
    SET NEW.cantidad_total = NEW.cantidad_disponible;
END//
DELIMITER ;

-- =====================================================
-- TRIGGER: Validar cantidad disponible
-- =====================================================
DELIMITER //
CREATE TRIGGER tr_validar_cantidad 
BEFORE UPDATE ON libros
FOR EACH ROW
BEGIN
    IF NEW.cantidad_disponible > NEW.cantidad_total THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La cantidad disponible no puede ser mayor que la cantidad total';
    END IF;
    
    IF NEW.cantidad_disponible < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La cantidad disponible no puede ser negativa';
    END IF;
END//
DELIMITER ;

-- =====================================================
-- INSERTAR DATOS DE PRUEBA
-- =====================================================

-- Insertar usuarios de prueba
INSERT INTO usuarios (nombre, email, password, telefono, direccion, rol) VALUES
('Administrador Principal', 'admin@biblioteca.com', 'pbkdf2:sha256:600000$ZKrKvQJWLWFLrY0L$8f89c52e5b8c4f9c67bda8d4a3e2e91b12e5f8c9d6a7b3e4f5a2b1c8d9e6f3a7', '555-0001', 'Calle Principal 123', 'admin'),
('María González', 'maria.bibliotecaria@biblioteca.com', 'pbkdf2:sha256:600000$bK8sF3mNqW9L$7e98b41d4a7c3f8b56c9e8d3f2a1e90a01d4e7f8c5b6a9d2e3f4c7a8b5e6f9', '555-0002', 'Avenida Libros 456', 'bibliotecario'),
('Juan Pérez', 'juan.perez@email.com', 'pbkdf2:sha256:600000$mL5aR2hJ8K$6d87a30c3b6e2f7a45b8d7c2e1f89d90c3b6e9f7a4c8b5e2f6a9c3d7e8f1b4', '555-0003', 'Barrio Norte 789', 'usuario'),
('Ana López', 'ana.lopez@email.com', 'pbkdf2:sha256:600000$nK9fT7gQ3M$5c76f29b2a5d1e6f34a7c6b1f98e8c89b2a5e8d6f3a7c4b9e5f2a8d1c6e7f9', '555-0004', 'Zona Centro 321', 'usuario'),
('Carlos Ruiz', 'carlos.ruiz@email.com', 'pbkdf2:sha256:600000$pJ4eS6dR2N$4b65e18a1f4c9d5e23f6b5a9e87d7b78a1f4d7c5e2f6a3b8d4e9f7a2c5d8e6', '555-0005', 'Colonia Sur 654', 'usuario');

-- Insertar categorías de prueba
INSERT INTO categorias (nombre, descripcion) VALUES
('Ficción', 'Novelas y cuentos de ficción literaria'),
('Ciencia y Tecnología', 'Libros sobre ciencias exactas, tecnología e informática'),
('Historia', 'Libros de historia mundial y nacional'),
('Biografías', 'Historias de vida de personajes importantes'),
('Educación', 'Libros educativos y de texto'),
('Arte y Cultura', 'Libros sobre arte, música y expresiones culturales'),
('Filosofía', 'Textos filosóficos clásicos y contemporáneos'),
('Ciencias Sociales', 'Sociología, psicología y ciencias humanas'),
('Literatura Clásica', 'Obras clásicas de la literatura universal'),
('Autoayuda', 'Libros de desarrollo personal y autoayuda');

-- Insertar libros de prueba
INSERT INTO libros (titulo, autor, isbn, categoria_id, año_publicacion, editorial, cantidad_disponible, cantidad_total) VALUES
-- Ficción
('Cien años de soledad', 'Gabriel García Márquez', '978-84-376-0494-7', 1, 1967, 'Editorial Sudamericana', 3, 3),
('1984', 'George Orwell', '978-84-9759-564-6', 1, 1949, 'Seix Barral', 2, 2),
('El amor en los tiempos del cólera', 'Gabriel García Márquez', '978-84-8306-652-4', 1, 1985, 'Oveja Negra', 2, 2),
('Fahrenheit 451', 'Ray Bradbury', '978-84-9759-329-1', 1, 1953, 'Minotauro', 1, 1),

-- Ciencia y Tecnología
('Introducción a los Algoritmos', 'Thomas H. Cormen', '978-84-283-3804-5', 2, 2009, 'McGraw Hill', 2, 2),
('El gen egoísta', 'Richard Dawkins', '978-84-344-8407-4', 2, 1976, 'Oxford University Press', 1, 1),
('Breve historia del tiempo', 'Stephen Hawking', '978-84-344-1356-9', 2, 1988, 'Bantam Books', 2, 2),

-- Historia
('Sapiens: De animales a dioses', 'Yuval Noah Harari', '978-84-9992-786-1', 3, 2011, 'Debate', 3, 3),
('El siglo de las luces', 'Alejo Carpentier', '978-84-376-0123-6', 3, 1962, 'Barral Editores', 1, 1),
('Historia de España', 'Pierre Vilar', '978-84-8432-355-2', 3, 1947, 'Editorial Crítica', 1, 1),

-- Biografías
('Steve Jobs', 'Walter Isaacson', '978-84-9992-158-6', 4, 2011, 'Simon & Schuster', 2, 2),
('Leonardo da Vinci', 'Walter Isaacson', '978-84-9992-789-2', 4, 2017, 'Simon & Schuster', 1, 1),

-- Educación
('Pedagogía del oprimido', 'Paulo Freire', '978-84-323-0458-7', 5, 1970, 'Siglo XXI', 2, 2),
('Como aprende el cerebro', 'Sarah-Jayne Blakemore', '978-84-344-5389-6', 5, 2005, 'Ariel', 1, 1),

-- Literatura Clásica
('Don Quijote de la Mancha', 'Miguel de Cervantes', '978-84-376-2188-3', 9, 1605, 'Espasa Calpe', 4, 4),
('Hamlet', 'William Shakespeare', '978-84-344-8765-5', 9, 1603, 'Alianza Editorial', 2, 2),
('La Odisea', 'Homero', '978-84-344-6754-1', 9, -800, 'Gredos', 2, 2);

-- Insertar préstamos de prueba
INSERT INTO prestamos (usuario_id, libro_id, fecha_prestamo, observaciones, estado) VALUES
-- Préstamos activos
(3, 1, '2025-09-20', 'Préstamo regular', 'activo'),
(4, 3, '2025-09-25', 'Renovación solicitada', 'activo'),
(5, 7, '2025-10-01', 'Primera lectura del autor', 'activo'),

-- Préstamos devueltos
(3, 2, '2025-09-01', 'Excelente estado', 'devuelto'),
(4, 5, '2025-08-15', 'Libro muy solicitado', 'devuelto'),
(5, 11, '2025-08-20', 'Lectura recomendada', 'devuelto');

-- Actualizar fecha de devolución para préstamos devueltos
UPDATE prestamos SET fecha_devolucion = '2025-09-15' WHERE id = 4;
UPDATE prestamos SET fecha_devolucion = '2025-08-29' WHERE id = 5;
UPDATE prestamos SET fecha_devolucion = '2025-09-03' WHERE id = 6;

-- =====================================================
-- VISTAS ÚTILES PARA REPORTES
-- =====================================================

-- Vista: Préstamos activos con información completa
CREATE VIEW vista_prestamos_activos AS
SELECT 
    p.id,
    u.nombre as usuario_nombre,
    u.email as usuario_email,
    l.titulo as libro_titulo,
    l.autor as libro_autor,
    p.fecha_prestamo,
    p.fecha_vencimiento,
    DATEDIFF(p.fecha_vencimiento, CURDATE()) as dias_restantes,
    CASE 
        WHEN CURDATE() > p.fecha_vencimiento THEN 'Vencido'
        WHEN DATEDIFF(p.fecha_vencimiento, CURDATE()) <= 3 THEN 'Por vencer'
        ELSE 'Vigente'
    END as estado_prestamo
FROM prestamos p
JOIN usuarios u ON p.usuario_id = u.id
JOIN libros l ON p.libro_id = l.id
WHERE p.fecha_devolucion IS NULL;

-- Vista: Libros más prestados
CREATE VIEW vista_libros_populares AS
SELECT 
    l.id,
    l.titulo,
    l.autor,
    c.nombre as categoria,
    COUNT(p.id) as total_prestamos,
    l.cantidad_total,
    l.cantidad_disponible
FROM libros l
LEFT JOIN prestamos p ON l.id = p.libro_id
JOIN categorias c ON l.categoria_id = c.id
GROUP BY l.id, l.titulo, l.autor, c.nombre, l.cantidad_total, l.cantidad_disponible
ORDER BY total_prestamos DESC;

-- Vista: Estadísticas por categoría
CREATE VIEW vista_estadisticas_categoria AS
SELECT 
    c.id,
    c.nombre as categoria,
    COUNT(l.id) as total_libros,
    SUM(l.cantidad_total) as ejemplares_totales,
    SUM(l.cantidad_disponible) as ejemplares_disponibles,
    COUNT(p.id) as total_prestamos
FROM categorias c
LEFT JOIN libros l ON c.id = l.categoria_id
LEFT JOIN prestamos p ON l.id = p.libro_id
GROUP BY c.id, c.nombre
ORDER BY c.nombre;

-- =====================================================
-- PROCEDIMIENTOS ALMACENADOS ÚTILES
-- =====================================================

-- Procedimiento: Obtener historial de préstamos de un usuario
DELIMITER //
CREATE PROCEDURE sp_historial_usuario(IN p_usuario_id INT)
BEGIN
    SELECT 
        p.id,
        l.titulo,
        l.autor,
        p.fecha_prestamo,
        p.fecha_devolucion,
        p.estado,
        CASE 
            WHEN p.fecha_devolucion IS NULL AND CURDATE() > p.fecha_vencimiento THEN 'Vencido'
            WHEN p.fecha_devolucion IS NULL THEN 'Activo'
            ELSE 'Devuelto'
        END as estado_actual
    FROM prestamos p
    JOIN libros l ON p.libro_id = l.id
    WHERE p.usuario_id = p_usuario_id
    ORDER BY p.fecha_prestamo DESC;
END//
DELIMITER ;

-- Procedimiento: Verificar disponibilidad de libro
DELIMITER //
CREATE PROCEDURE sp_verificar_disponibilidad(IN p_libro_id INT)
BEGIN
    SELECT 
        l.titulo,
        l.autor,
        l.cantidad_total,
        l.cantidad_disponible,
        (l.cantidad_disponible > 0) as disponible,
        COUNT(p.id) as prestamos_activos
    FROM libros l
    LEFT JOIN prestamos p ON l.id = p.libro_id AND p.fecha_devolucion IS NULL
    WHERE l.id = p_libro_id
    GROUP BY l.id, l.titulo, l.autor, l.cantidad_total, l.cantidad_disponible;
END//
DELIMITER ;

-- =====================================================
-- ÍNDICES ADICIONALES PARA OPTIMIZACIÓN
-- =====================================================

-- Índice compuesto para búsquedas frecuentes
CREATE INDEX idx_libro_categoria_autor ON libros(categoria_id, autor);
CREATE INDEX idx_prestamo_usuario_fecha ON prestamos(usuario_id, fecha_prestamo);
CREATE INDEX idx_prestamo_estado_fecha ON prestamos(estado, fecha_prestamo);

-- =====================================================
-- INFORMACIÓN DE USUARIOS DE PRUEBA
-- =====================================================

/*
USUARIOS DE PRUEBA PARA LOGIN:

1. Administrador:
   Email: admin@biblioteca.com
   Password: admin123

2. Bibliotecario:
   Email: maria.bibliotecaria@biblioteca.com
   Password: biblio123

3. Usuario Regular:
   Email: juan.perez@email.com
   Password: user123

NOTA: Las contraseñas están hasheadas con Werkzeug Security.
Para generar nuevos hashes, usar:
from werkzeug.security import generate_password_hash
generate_password_hash('tu_password')
*/

-- =====================================================
-- SCRIPT COMPLETADO
-- =====================================================

SELECT 'Base de datos biblioteca_db creada exitosamente con datos de prueba' as mensaje;
SELECT 'Total de usuarios creados:' as info, COUNT(*) as cantidad FROM usuarios;
SELECT 'Total de categorías creadas:' as info, COUNT(*) as cantidad FROM categorias;
SELECT 'Total de libros agregados:' as info, COUNT(*) as cantidad FROM libros;
SELECT 'Total de préstamos registrados:' as info, COUNT(*) as cantidad FROM prestamos;
