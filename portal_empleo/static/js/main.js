// tu_app/static/js/main.js

// Este evento asegura que el código se ejecute solo después de que todo el HTML ha sido cargado.
document.addEventListener('DOMContentLoaded', function() {

    // Se busca el elemento de la barra de navegación.
    const navbar = document.getElementById('navbar');

    // Solo ejecutamos el código si la navbar existe en la página actual para evitar errores.
    if (navbar) {
        
        // --- Lógica para el efecto de scroll en la Navbar ---
        
        // Función para añadir o quitar la clase 'scrolled' según la posición del scroll.
        function updateNavbarOnScroll() {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        }
        
        // Se ejecuta la función una vez al cargar la página para establecer el estado inicial.
        updateNavbarOnScroll();
        
        // Se añade un listener para que la función se ejecute cada vez que el usuario hace scroll.
        window.addEventListener('scroll', updateNavbarOnScroll);

        
        // --- Lógica para el efecto hover en los enlaces de la Navbar ---

        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('mouseenter', function() {
                // Al entrar el ratón, el enlace se mueve ligeramente hacia arriba.
                this.style.transform = 'translateY(-2px)';
            });
            
            link.addEventListener('mouseleave', function() {
                // Al salir el ratón, el enlace vuelve a su posición original.
                this.style.transform = 'translateY(0)';
            });
        });
    }
});