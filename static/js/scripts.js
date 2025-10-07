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

// Gallery Modal functionality
function openModal(imageSrc) {
    const modal = document.getElementById('imageModal');
    const modalImg = document.getElementById('modalImage');
    
    if (modal && modalImg) {
        modal.style.display = 'block';
        modalImg.src = imageSrc;
    }
}

// Close modal when clicking the X or outside the image
document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('imageModal');
    const closeBtn = document.querySelector('.close');
    
    if (closeBtn) {
        closeBtn.addEventListener('click', function() {
            modal.style.display = 'none';
        });
    }
    
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                modal.style.display = 'none';
            }
        });
    }
    
    // Close modal with Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal) {
            modal.style.display = 'none';
        }
    });
});

// Testimonials enhanced functionality
document.addEventListener('DOMContentLoaded', function() {
    // Add hover effects and interaction to testimonials
    const testimonials = document.querySelectorAll('.testimonial-item');
    
    testimonials.forEach(testimonial => {
        testimonial.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        testimonial.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Enhanced rating display for testimonials
    const ratingElements = document.querySelectorAll('.testimonial-rating');
    
    ratingElements.forEach(rating => {
        const stars = rating.querySelectorAll('.star');
        
        stars.forEach((star, index) => {
            star.addEventListener('mouseenter', function() {
                for (let i = 0; i <= index; i++) {
                    stars[i].style.transform = 'scale(1.2)';
                    stars[i].style.transition = 'transform 0.2s ease';
                }
            });
            
            star.addEventListener('mouseleave', function() {
                stars.forEach(s => {
                    s.style.transform = 'scale(1)';
                });
            });
        });
    });
});

// Enhanced image loading
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img');
    
    images.forEach(img => {
        img.addEventListener('load', function() {
            this.style.opacity = '1';
        });
        
        img.addEventListener('error', function() {
            this.src = 'https://images.unsplash.com/photo-1571896349842-33c89424de2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80';
            this.alt = 'Imagen no disponible';
        });
    });
});
