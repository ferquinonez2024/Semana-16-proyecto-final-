# 🎥 Guía de Presentación - Sistema de Gestión de Biblioteca

## 📋 Checklist para la Presentación

### ✅ Antes de Presentar

- [ ] **Verificar que el sistema está funcionando**
  ```bash
  python run.py
  ```
- [ ] **Probar todas las funcionalidades principales**
- [ ] **Tener datos de prueba listos**
- [ ] **Preparar navegador con pestañas abiertas**

### 🎯 Estructura de la Presentación (5-7 minutos)

## 1. **Introducción** (30 segundos)
> "Buenos días, voy a presentar el **Sistema de Gestión de Biblioteca** desarrollado en Flask con MySQL"

**Mostrar:**
- Página principal (`http://localhost:5000`)
- Explicar brevemente las tecnologías utilizadas

## 2. **Demostración de Login** (1 minuto)

**Credenciales a mostrar:**
```
Administrador:
- Email: admin@biblioteca.com
- Password: admin123
```

**Narración:**
> "El sistema cuenta con autenticación segura con contraseñas hasheadas. Voy a iniciar sesión como administrador."

## 3. **Dashboard y Navegación** (1 minuto)

**Mostrar:**
- Dashboard con estadísticas
- Navegación por el menú lateral
- Explicar los números de cada módulo

**Narración:**
> "Una vez autenticado, accedemos al dashboard que muestra estadísticas en tiempo real del sistema."

## 4. **CRUD Completo - Demostración** (3-4 minutos)

### A. **Gestión de Categorías** (45 segundos)
1. Ir a Categorías
2. **Crear**: Nueva categoría "Literatura Contemporánea"
3. **Mostrar**: Lista de categorías existentes
4. **Editar**: Modificar la descripción
5. **Eliminar**: (opcional, mencionar la funcionalidad)

### B. **Gestión de Libros** (1.5 minutos)
1. Ir a Libros
2. **Crear**: Nuevo libro con la categoría recién creada
   - Título: "El Tiempo Entre Costuras"
   - Autor: "María Dueñas"
   - Categoría: Literatura Contemporánea
   - Cantidad: 3
3. **Mostrar**: El libro en la lista con su categoría
4. **Editar**: Cambiar cantidad disponible

### C. **Gestión de Usuarios** (45 segundos)
1. Ir a Usuarios
2. **Mostrar**: Lista de usuarios existentes
3. **Crear**: Nuevo usuario lector
4. **Explicar**: Diferentes roles (admin, bibliotecario, usuario)

### D. **Gestión de Préstamos** (45 segundos)
1. Ir a Préstamos
2. **Crear**: Nuevo préstamo con el libro y usuario creados
3. **Mostrar**: Cómo se actualiza automáticamente la disponibilidad
4. **Devolver**: Marcar como devuelto
5. **Mostrar**: Estadísticas actualizadas

## 5. **Características Técnicas** (30 segundos)

**Mencionar rápidamente:**
- Base de datos MySQL con 4 tablas relacionadas
- Seguridad con Werkzeug
- Interfaz responsiva con Bootstrap
- Control de inventario automático

## 6. **Conclusión** (30 segundos)

> "El sistema implementa todas las funcionalidades requeridas: CRUD completo para múltiples entidades relacionadas, autenticación segura, y una interfaz intuitiva. Está listo para uso en producción."

---

## 🎬 Script de Demostración Detallado

### Login y Dashboard
```
1. Abrir http://localhost:5000
2. Clic en "Iniciar Sesión"
3. Ingresar: admin@biblioteca.com / admin123
4. Mostrar dashboard con estadísticas
5. Explicar navegación lateral
```

### CRUD de Categorías
```
1. Clic en "Categorías"
2. Clic en "Nueva Categoría"
3. Nombre: "Literatura Contemporánea"
4. Descripción: "Novelas y cuentos de autores contemporáneos"
5. Clic en "Crear Categoría"
6. Mostrar en la lista
7. Clic en "Editar" de alguna categoría
8. Modificar descripción
9. Guardar cambios
```

### CRUD de Libros
```
1. Clic en "Libros"
2. Clic en "Agregar Libro"
3. Llenar formulario:
   - Título: "El Tiempo Entre Costuras"
   - Autor: "María Dueñas"
   - ISBN: "978-84-8460-940-7"
   - Categoría: "Literatura Contemporánea"
   - Año: 2009
   - Editorial: "Planeta"
   - Cantidad: 3
4. Clic en "Agregar Libro"
5. Mostrar en la tabla
6. Explicar estados (disponible, pocos, agotado)
```

### CRUD de Usuarios
```
1. Clic en "Usuarios"
2. Mostrar diferentes tipos de usuarios
3. Clic en "Nuevo Usuario"
4. Llenar formulario:
   - Nombre: "Ana García"
   - Email: "ana.garcia@email.com"
   - Password: "password123"
   - Teléfono: "555-9999"
   - Rol: "Usuario"
5. Crear usuario
6. Mostrar en la lista
```

### CRUD de Préstamos
```
1. Clic en "Préstamos"
2. Clic en "Nuevo Préstamo"
3. Seleccionar:
   - Usuario: "Ana García"
   - Libro: "El Tiempo Entre Costuras"
4. Registrar préstamo
5. Mostrar que cantidad disponible se redujo
6. Volver a préstamos
7. Clic en "Devolver" para algún préstamo
8. Confirmar devolución
9. Mostrar actualización de inventario
```

---

## 💡 Tips para la Presentación

### Durante la Demostración:
- **Ir lento y explicar cada acción**
- **Mostrar las relaciones entre tablas**
- **Explicar la lógica de negocio** (inventario automático)
- **Destacar la seguridad** y validaciones
- **Mencionar la responsividad** del diseño

### Si algo falla:
- **Mantener la calma**
- **Explicar qué debería pasar**
- **Tener screenshots de respaldo**
- **Continuar con otras funcionalidades**

### Puntos clave a enfatizar:
1. **CRUD completo** en todas las entidades
2. **Relaciones entre tablas** (categorías↔libros, usuarios↔préstamos, etc.)
3. **Autenticación robusta**
4. **Control automático de inventario**
5. **Interfaz intuitiva y profesional**
6. **Código limpio y bien estructurado**

---

## 🎥 Para Video (Alternativa)

### Estructura del Video (3-5 minutos):

1. **Intro** (15 seg): "Sistema de Gestión de Biblioteca en Flask"
2. **Login rápido** (20 seg): Mostrar autenticación
3. **Dashboard** (20 seg): Explicar estadísticas
4. **CRUD rápido** (2-3 min): 
   - Crear categoría (30 seg)
   - Crear libro (45 seg)
   - Crear usuario (30 seg)
   - Hacer préstamo (45 seg)
   - Devolver libro (30 seg)
5. **Conclusión** (15 seg): Características técnicas principales

### Tips para grabación:
- **Pantalla limpia** sin distracciones
- **Cursor visible** y movimientos deliberados  
- **Narración clara** explicando cada acción
- **Zoom si es necesario** para mostrar detalles
- **Comprobar audio** antes de grabar

---

## ✅ Checklist Final

**Antes de presentar verificar:**
- [ ] MySQL ejecutándose
- [ ] Base de datos creada con datos de prueba
- [ ] Aplicación Flask funcionando
- [ ] Login funcionando con credenciales de prueba
- [ ] Todas las funciones CRUD operativas
- [ ] Navegador preparado con pestañas
- [ ] Script de presentación revisado

**¡Éxito asegurado! 🚀**
