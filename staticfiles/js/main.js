// Manejo del menú móvil
document.addEventListener('DOMContentLoaded', function() {
    const navbarToggler = document.querySelector('.navbar-toggler');
    const body = document.body;
    const mobileMenuOverlay = document.querySelector('.mobile-menu-overlay');
    
    if (navbarToggler) {
        navbarToggler.addEventListener('click', function() {
            const isExpanded = this.getAttribute('aria-expanded') === 'true';
            
            if (isExpanded) {
                body.classList.remove('menu-open');
            } else {
                body.classList.add('menu-open');
            }
        });
    }
    
    // Cerrar menú al hacer clic en el overlay
    if (mobileMenuOverlay) {
        mobileMenuOverlay.addEventListener('click', function() {
            if (navbarToggler && body.classList.contains('menu-open')) {
                navbarToggler.click();
            }
        });
    }
    
    // Cerrar menú al hacer clic en un enlace
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (window.innerWidth < 992 && body.classList.contains('menu-open')) {
                if (navbarToggler) {
                    navbarToggler.click();
                }
            }
        });
    });

    // Mejorar comportamiento de dropdowns en móviles
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            if (window.innerWidth < 992) {
                e.preventDefault();
                e.stopPropagation();
                const dropdownMenu = this.nextElementSibling;
                if (dropdownMenu) {
                    dropdownMenu.classList.toggle('show');
                }
            }
        });
    });
});