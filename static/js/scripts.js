// Smooth scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
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

// Set minimum date to today for booking forms
document.addEventListener('DOMContentLoaded', function() {
    const today = new Date().toISOString().split('T')[0];
    
    const checkinInputs = document.querySelectorAll('#checkin');
    const checkoutInputs = document.querySelectorAll('#checkout');
    
    checkinInputs.forEach(input => {
        input.setAttribute('min', today);
        
        input.addEventListener('change', function() {
            const checkinDate = new Date(this.value);
            checkinDate.setDate(checkinDate.getDate() + 1);
            const minCheckout = checkinDate.toISOString().split('T')[0];
            
            // Update corresponding checkout input
            const checkoutInput = this.closest('form').querySelector('#checkout');
            checkoutInput.setAttribute('min', minCheckout);
            
            // If checkout is before new min date, update it
            if (checkoutInput.value < minCheckout) {
                checkoutInput.value = minCheckout;
            }
        });
    });
    
    checkoutInputs.forEach(input => {
        input.setAttribute('min', today);
    });
});

// Play button functionality (demo)
document.querySelectorAll('.play-button').forEach(button => {
    button.addEventListener('click', function() {
        alert('¡Bienvenido al tráiler! En una implementación real, aquí se reproduciría un video sobre la experiencia en el hotel.');
    });
});

// Add animation on scroll
const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.1
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate');
        }
    });
}, observerOptions);

document.querySelectorAll('.hotel-card, .testimonial-card, .gallery-item').forEach(el => {
    observer.observe(el);
});
