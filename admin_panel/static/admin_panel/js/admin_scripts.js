// Cuando el documento esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Añadir confirmación a botones de eliminar
    const deleteButtons = document.querySelectorAll('[data-confirm]');
    
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm(this.getAttribute('data-confirm'))) {
                e.preventDefault();
            }
        });
    });
    
    // Funcionalidad para mostrar/ocultar detalles
    const toggleButtons = document.querySelectorAll('[data-toggle="collapse"]');
    
    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const target = document.querySelector(this.getAttribute('data-target'));
            if (target) {
                target.classList.toggle('show');
            }
        });
    });
});