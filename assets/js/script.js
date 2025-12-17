// Global variables
let currentSlide = 0;
let slideInterval;

// Mobile menu toggle
function toggleMenu() {
    const navMenu = document.querySelector('.nav-menu');
    const burgerMenu = document.querySelector('.burger-menu');
    const overlay = document.querySelector('.mobile-menu-overlay');
    
    navMenu.classList.toggle('active');
    burgerMenu.classList.toggle('active');
    overlay.classList.toggle('active');
}

// Carousel functionality
function changeSlide(direction) {
    const slides = document.querySelectorAll('.carousel-slide');
    const indicators = document.querySelectorAll('.indicator');
    
    // Remove active class from current slide
    slides[currentSlide].classList.remove('active');
    indicators[currentSlide].classList.remove('active');
    
    // Calculate new slide index
    currentSlide += direction;
    
    if (currentSlide >= totalSlides) {
        currentSlide = 0;
    } else if (currentSlide < 0) {
        currentSlide = totalSlides - 1;
    }
    
    // Add active class to new slide
    slides[currentSlide].classList.add('active');
    indicators[currentSlide].classList.add('active');
}

function goToSlide(slideIndex) {
    const slides = document.querySelectorAll('.carousel-slide');
    const indicators = document.querySelectorAll('.indicator');
    
    // Remove active class from current slide
    slides[currentSlide].classList.remove('active');
    indicators[currentSlide].classList.remove('active');
    
    // Set new slide
    currentSlide = slideIndex;
    
    // Add active class to new slide
    slides[currentSlide].classList.add('active');
    indicators[currentSlide].classList.add('active');
}

// Auto-advance carousel
function startCarousel() {
    slideInterval = setInterval(() => {
        changeSlide(1);
    }, 5000);
}

function stopCarousel() {
    clearInterval(slideInterval);
}

// Smooth scrolling for navigation links
function initSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="/#"], a[href^="/en/#"]');

    links.forEach(link => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href'); // مثل "/#home" أو "/en/#contact"
            const isEnglish = href.startsWith('/en/');
            const hash = href.split('#')[1]; // "home" أو "contact"

            // تحقق هل نحن على الصفحة الرئيسية أو الإنجليزية
            const onArabicHome = window.location.pathname === '/' || window.location.pathname === '/index.php';
            const onEnglishHome = window.location.pathname === '/en/' || window.location.pathname === '/en/index.php';

            const onHomePage = isEnglish ? onEnglishHome : onArabicHome;

            if (!onHomePage) {
                // لو مش في الصفحة الرئيسية المناسبة، روح لها ومعاك الهاش
                window.location.href = href;
                return;
            }

            e.preventDefault(); // امنع القفز التلقائي

            const targetElement = document.getElementById(hash);
            if (targetElement) {
                const headerHeight = document.querySelector('.header')?.offsetHeight || 0;
                const targetPosition = targetElement.offsetTop - headerHeight;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });

                history.replaceState(null, document.title, window.location.pathname);

                // اقفل المينيو لو كانت مفتوحة
                const navMenu = document.querySelector('.nav-menu');
                const burgerMenu = document.querySelector('.burger-menu');
                const overlay = document.querySelector('.mobile-menu-overlay');

                if (navMenu?.classList.contains('active')) {
                    navMenu.classList.remove('active');
                    burgerMenu?.classList.remove('active');
                    overlay?.classList.remove('active');
                }
            }
        });
    });

    // ✅ تنفيذ السكروول التلقائي إذا فيه هاش
    const hash = window.location.hash;
    if (hash) {
        const targetId = hash.substring(1); // يشيل #
        const targetElement = document.getElementById(targetId);
        if (targetElement) {
            const headerHeight = document.querySelector('.header')?.offsetHeight || 0;
            const targetPosition = targetElement.offsetTop - headerHeight;

            setTimeout(() => {
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });

                history.replaceState(null, document.title, window.location.pathname);
            }, 200); // تأخير بسيط لضمان تحميل العنصر
        }
    }
}

// Header scroll effect
function initHeaderScrollEffect() {
    const header = document.querySelector('.header');
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 100) {
            header.style.background = 'rgba(255, 255, 255, 0.95)';
            header.style.backdropFilter = 'blur(10px)';
        } else {
            header.style.background = 'var(--white)';
            header.style.backdropFilter = 'none';
        }
    });
}

// Close mobile menu when clicking outside
function initOutsideClickHandler() {
    document.addEventListener('click', (e) => {
        const navMenu = document.querySelector('.nav-menu');
        const burgerMenu = document.querySelector('.burger-menu');
        const overlay = document.querySelector('.mobile-menu-overlay');
        
        if (navMenu.classList.contains('active') && 
            !navMenu.contains(e.target) && 
            !burgerMenu.contains(e.target)) {
            navMenu.classList.remove('active');
            burgerMenu.classList.remove('active');
            overlay.classList.remove('active');
        }
    });
}

// Keyboard navigation for carousel
function initKeyboardNavigation() {
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft') {
            changeSlide(-1);
        } else if (e.key === 'ArrowRight') {
            changeSlide(1);
        }
    });
}

// Initialize all functionality when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    startCarousel();
    initSmoothScrolling();
    initContactForm();
    initHeaderScrollEffect();
    initOutsideClickHandler();
    initKeyboardNavigation();
    
    // Pause carousel when user hovers over it
    const carousel = document.querySelector('.carousel');
    carousel.addEventListener('mouseenter', stopCarousel);
    carousel.addEventListener('mouseleave', startCarousel);
    
    // Add loading animation
    document.body.classList.add('loaded');
});

// Handle window resize
window.addEventListener('resize', () => {
    // Close mobile menu on resize to desktop
    if (window.innerWidth > 768) {
        const navMenu = document.querySelector('.nav-menu');
        const burgerMenu = document.querySelector('.burger-menu');
        const overlay = document.querySelector('.mobile-menu-overlay');
        
        navMenu.classList.remove('active');
        burgerMenu.classList.remove('active');
        overlay.classList.remove('active');
    }
});

// Performance optimization: Lazy load images
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                observer.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// Call lazy loading if supported
if ('IntersectionObserver' in window) {
    initLazyLoading();
}