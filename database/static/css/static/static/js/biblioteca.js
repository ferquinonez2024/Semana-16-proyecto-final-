// JavaScript personalizado para el Sistema de Biblioteca

// Funciones de utilidad
const BibliotecaApp = {
    // Inicialización
    init: function() {
        this.setupEventListeners();
        this.setupTooltips();
        this.setupFormValidation();
        this.setupSearchFunctionality();
    },

    // Configurar event listeners
    setupEventListeners: function() {
        // Confirmaciones de eliminación
        document.querySelectorAll('[data-confirm]').forEach(element => {
            element.addEventListener('click', function(e) {
                const message = this.getAttribute('data-confirm');
                if (!confirm(message)) {
                    e.preventDefault();
                }
            });
        });

        // Auto-dismiss para alerts
        document.querySelectorAll('.alert-dismissible').forEach(alert => {
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        });

        // Smooth scroll para links internos
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    },

    // Configurar tooltips
    setupTooltips: function() {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    },

    // Validación de formularios
    setupFormValidation: function() {
        // Validación en tiempo real
        document.querySelectorAll('.form-control').forEach(input => {
            input.addEventListener('blur', function() {
                this.classList.remove('is-invalid', 'is-valid');
                
                if (this.hasAttribute('required') && !this.value.trim()) {
                    this.classList.add('is-invalid');
                } else if (this.value.trim()) {
                    this.classList.add('is-valid');
                }
            });
        });

        // Validación de email
        document.querySelectorAll('input[type="email"]').forEach(input => {
            input.addEventListener('blur', function() {
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                this.classList.remove('is-invalid', 'is-valid');
                
                if (this.value && !emailRegex.test(this.value)) {
                    this.classList.add('is-invalid');
                    this.setCustomValidity('Por favor ingresa un email válido');
                } else if (this.value) {
                    this.classList.add('is-valid');
                    this.setCustomValidity('');
                }
            });
        });

        // Prevenir envío de formularios inválidos
        document.querySelectorAll('form').forEach(form => {
            form.addEventListener('submit', function(e) {
                if (!form.checkValidity()) {
                    e.preventDefault();
                    e.stopPropagation();
                }
                form.classList.add('was-validated');
            });
        });
    },

    // Funcionalidad de búsqueda
    setupSearchFunctionality: function() {
        // Búsqueda en tiempo real para tablas
        document.querySelectorAll('.search-input').forEach(input => {
            input.addEventListener('input', function() {
                const filter = this.value.toLowerCase();
                const tableId = this.getAttribute('data-table');
                const table = document.getElementById(tableId);
                
                if (table) {
                    const rows = table.getElementsByTagName('tbody')[0].getElementsByTagName('tr');
                    
                    Array.from(rows).forEach(row => {
                        const text = row.textContent.toLowerCase();
                        row.style.display = text.includes(filter) ? '' : 'none';
                    });
                }
            });
        });
    },

    // Funciones de utilidad
    utils: {
        // Formatear fecha
        formatDate: function(date) {
            return new Intl.DateTimeFormat('es-ES').format(new Date(date));
        },

        // Mostrar mensaje de éxito
        showSuccess: function(message) {
            this.showAlert(message, 'success');
        },

        // Mostrar mensaje de error
        showError: function(message) {
            this.showAlert(message, 'danger');
        },

        // Mostrar alerta
        showAlert: function(message, type = 'info') {
            const alertHtml = `
                <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                    ${message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            `;
            
            const container = document.querySelector('.alert-container') || document.body;
            container.insertAdjacentHTML('afterbegin', alertHtml);
        },

        // Confirmar acción
        confirmAction: function(message, callback) {
            if (confirm(message)) {
                if (typeof callback === 'function') {
                    callback();
                }
                return true;
            }
            return false;
        },

        // Debounce para búsquedas
        debounce: function(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        }
    },

    // Funciones específicas para módulos
    usuarios: {
        validateForm: function(form) {
            const nombre = form.querySelector('#nombre').value.trim();
            const email = form.querySelector('#email').value.trim();
            const password = form.querySelector('#password');
            
            if (nombre.length < 3) {
                BibliotecaApp.utils.showError('El nombre debe tener al menos 3 caracteres');
                return false;
            }
            
            if (!email.includes('@')) {
                BibliotecaApp.utils.showError('Por favor ingresa un email válido');
                return false;
            }
            
            if (password && password.value.length < 6) {
                BibliotecaApp.utils.showError('La contraseña debe tener al menos 6 caracteres');
                return false;
            }
            
            return true;
        }
    },

    libros: {
        validateForm: function(form) {
            const titulo = form.querySelector('#titulo').value.trim();
            const autor = form.querySelector('#autor').value.trim();
            const categoria = form.querySelector('#categoria_id').value;
            
            if (titulo.length < 3) {
                BibliotecaApp.utils.showError('El título debe tener al menos 3 caracteres');
                return false;
            }
            
            if (autor.length < 2) {
                BibliotecaApp.utils.showError('El autor debe tener al menos 2 caracteres');
                return false;
            }
            
            if (!categoria) {
                BibliotecaApp.utils.showError('Debes seleccionar una categoría');
                return false;
            }
            
            return true;
        },

        updateAvailability: function(libroId, nuevaCantidad) {
            // Aquí se podría implementar una actualización AJAX
            console.log(`Actualizando libro ${libroId} con cantidad ${nuevaCantidad}`);
        }
    },

    prestamos: {
        calculateDueDate: function(fechaPrestamo, dias = 15) {
            const fecha = new Date(fechaPrestamo);
            fecha.setDate(fecha.getDate() + dias);
            return fecha;
        },

        isOverdue: function(fechaVencimiento) {
            return new Date() > new Date(fechaVencimiento);
        }
    }
};

// Auto-completar campos comunes
const AutoComplete = {
    setupAutoresComunes: function() {
        const autoresComunes = [
            'Gabriel García Márquez',
            'Jorge Luis Borges',
            'Isabel Allende',
            'Mario Vargas Llosa',
            'Octavio Paz',
            'Pablo Neruda',
            'Julio Cortázar'
        ];
        
        const autorInput = document.getElementById('autor');
        if (autorInput) {
            this.setupDatalist(autorInput, autoresComunes, 'autores-list');
        }
    },

    setupEditorialesComunes: function() {
        const editorialesComunes = [
            'Editorial Sudamericana',
            'Alfaguara',
            'Planeta',
            'Random House',
            'Anagrama',
            'Tusquets',
            'Seix Barral'
        ];
        
        const editorialInput = document.getElementById('editorial');
        if (editorialInput) {
            this.setupDatalist(editorialInput, editorialesComunes, 'editoriales-list');
        }
    },

    setupDatalist: function(input, options, listId) {
        let datalist = document.getElementById(listId);
        if (!datalist) {
            datalist = document.createElement('datalist');
            datalist.id = listId;
            document.body.appendChild(datalist);
        }
        
        datalist.innerHTML = '';
        options.forEach(option => {
            const optionElement = document.createElement('option');
            optionElement.value = option;
            datalist.appendChild(optionElement);
        });
        
        input.setAttribute('list', listId);
    }
};

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    BibliotecaApp.init();
    AutoComplete.setupAutoresComunes();
    AutoComplete.setupEditorialesComunes();
});

// Hacer las funciones disponibles globalmente
window.BibliotecaApp = BibliotecaApp;
window.AutoComplete = AutoComplete;
