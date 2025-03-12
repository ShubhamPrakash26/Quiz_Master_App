// Set current year in footer
document.getElementById('current-year').textContent = new Date().getFullYear();

// Mobile Menu Toggle
const menuToggle = document.querySelector('.menu-toggle');
const navMenu = document.querySelector('.nav-menu');

menuToggle.addEventListener('click', () => {
  navMenu.classList.toggle('active');
  menuToggle.querySelector('i').classList.toggle('fa-bars');
  menuToggle.querySelector('i').classList.toggle('fa-times');
});

// Close menu when clicking on a nav link
document.querySelectorAll('.nav-menu a').forEach(link => {
  link.addEventListener('click', () => {
    navMenu.classList.remove('active');
    menuToggle.querySelector('i').classList.add('fa-bars');
    menuToggle.querySelector('i').classList.remove('fa-times');
  });
});

// Carousel functionality
const carousel = document.querySelector('.carousel');
const carouselItems = document.querySelectorAll('.carousel-item');
const prevBtn = document.querySelector('.prev');
const nextBtn = document.querySelector('.next');
const indicatorsContainer = document.querySelector('.carousel-indicators');

let currentIndex = 0;
const totalItems = carouselItems.length;

// Create indicators
for (let i = 0; i < totalItems; i++) {
  const indicator = document.createElement('div');
  indicator.classList.add('indicator');
  if (i === 0) indicator.classList.add('active');
  indicator.addEventListener('click', () => {
    goToSlide(i);
  });
  indicatorsContainer.appendChild(indicator);
}

const indicators = document.querySelectorAll('.indicator');

// Function to update carousel position
function updateCarousel() {
  carousel.style.transform = `translateX(-${currentIndex * 100}%)`;
  
  // Update indicators
  indicators.forEach((indicator, index) => {
    if (index === currentIndex) {
      indicator.classList.add('active');
    } else {
      indicator.classList.remove('active');
    }
  });
}

// Go to specific slide
function goToSlide(index) {
  currentIndex = index;
  updateCarousel();
}

// Next slide
function nextSlide() {
  currentIndex = (currentIndex + 1) % totalItems;
  updateCarousel();
}

// Previous slide
function prevSlide() {
  currentIndex = (currentIndex - 1 + totalItems) % totalItems;
  updateCarousel();
}

// Event listeners for carousel controls
nextBtn.addEventListener('click', nextSlide);
prevBtn.addEventListener('click', prevSlide);

// Auto-advance carousel
let carouselInterval = setInterval(nextSlide, 5000);

// Pause auto-advance on hover
carousel.addEventListener('mouseenter', () => {
  clearInterval(carouselInterval);
});

carousel.addEventListener('mouseleave', () => {
  carouselInterval = setInterval(nextSlide, 5000);
});

// FAQ Accordion
const faqItems = document.querySelectorAll('.faq-item');

faqItems.forEach(item => {
  const question = item.querySelector('.faq-question');
  
  question.addEventListener('click', () => {
    // Close all other items
    faqItems.forEach(otherItem => {
      if (otherItem !== item) {
        otherItem.classList.remove('active');
      }
    });
    
    // Toggle current item
    item.classList.toggle('active');
  });
});

// Feature cards and pricing cards hover animation
const featureCards = document.querySelectorAll('.feature-card');
const pricingCards = document.querySelectorAll('.pricing-card');
const testimonialCards = document.querySelectorAll('.testimonial-card');

// Apply hover effect for touch devices
function applyHoverEffect(elements) {
  elements.forEach(element => {
    element.addEventListener('touchstart', () => {
      // Remove hover class from all elements
      elements.forEach(el => el.classList.remove('hover'));
      // Add hover class to current element
      element.classList.add('hover');
    });
  });
}

applyHoverEffect(featureCards);
applyHoverEffect(pricingCards);
applyHoverEffect(testimonialCards);

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    e.preventDefault();
    
    const targetId = this.getAttribute('href');
    if (targetId === '#') return;
    
    const targetElement = document.querySelector(targetId);
    if (targetElement) {
      const navbarHeight = document.querySelector('.navbar').offsetHeight;
      const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset - navbarHeight;
      
      window.scrollTo({
        top: targetPosition,
        behavior: 'smooth'
      });
    }
  });
});

// Add scroll event listener to change navbar background
window.addEventListener('scroll', () => {
  const navbar = document.querySelector('.navbar');
  if (window.scrollY > 50) {
    navbar.style.backgroundColor = 'rgba(255, 255, 255, 0.98)';
    navbar.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
  } else {
    navbar.style.backgroundColor = 'rgba(255, 255, 255, 0.95)';
    navbar.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
  }
});