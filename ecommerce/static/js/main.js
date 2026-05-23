/**
 * Main JavaScript for eCommerce website
 * Handles animations, interactions, and dynamic features
 */

document.addEventListener('DOMContentLoaded', function() {
    initializeMenuToggle();
    initializeWishlist();
    initializeRatingStars();
    initializeScrollAnimations();
    formatCurrency();
    autoHideMessages();
});

/**
 * Auto-hide alert messages
 */
function autoHideMessages() {
    const messages = document.querySelectorAll('.alert');
    if (messages.length > 0) {
        setTimeout(() => {
            messages.forEach(msg => {
                msg.style.animation = 'fadeOut 0.5s ease-out forwards';
                setTimeout(() => msg.remove(), 500);
            });
        }, 5000);
    }
}

/**
 * Mobile Menu Toggle
 */
function initializeMenuToggle() {
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    
    if (menuToggle && navLinks) {
        menuToggle.addEventListener('click', function() {
            navLinks.classList.toggle('active');
            
            // Animate hamburger icon
            const icon = menuToggle.querySelector('i');
            if (navLinks.classList.contains('active')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.add('fa-bars');
                icon.classList.remove('fa-times');
            }
        });
        
        // Close menu when clicking on a link
        const links = navLinks.querySelectorAll('a');
        links.forEach(link => {
            link.addEventListener('click', function() {
                navLinks.classList.remove('active');
                const icon = menuToggle.querySelector('i');
                icon.classList.add('fa-bars');
                icon.classList.remove('fa-times');
            });
        });
    }
}

/**
 * Wishlist functionality with AJAX
 */
function initializeWishlist() {
    const wishlistButtons = document.querySelectorAll('.wishlist-btn');
    
    wishlistButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const productId = this.dataset.productId;
            const csrfToken = getCsrfToken();
            
            if (!productId) return;
            
            // Show loading state
            const icon = this.querySelector('i');
            const originalClass = icon.className;
            icon.className = 'fas fa-spinner fa-spin';
            
            fetch(`/wishlist/add/${productId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Toggle button active state
                    this.classList.toggle('active');
                    
                    // Restore icon
                    icon.className = originalClass;
                    
                    // Show toast notification
                    showToast(data.message, 'success');
                    
                    // Add heart animation
                    animateHeartBeat(this);
                } else {
                    showToast(data.message || 'Error updating wishlist', 'error');
                    icon.className = originalClass;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                icon.className = originalClass;
                showToast('Error updating wishlist', 'error');
            });
        });
    });
}

/**
 * Get CSRF token from page
 */
function getCsrfToken() {
    // Try to get from input element first
    let token = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    if (token) return token;
    
    token = document.querySelector('input[name=csrfmiddlewaretoken]')?.value;
    if (token) return token;
    
    // Try to get from cookies
    const name = 'csrftoken';
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue || '';
}

/**
 * Interactive rating stars in reviews
 */
function initializeRatingStars() {
    const ratingOptions = document.querySelectorAll('.rating-option');
    
    ratingOptions.forEach(option => {
        const label = option.querySelector('label');
        const input = option.querySelector('input[type="radio"]');
        
        label.addEventListener('click', function() {
            // Add scale animation
            label.style.animation = 'none';
            setTimeout(() => {
                label.style.animation = 'pulse 0.3s ease-out';
            }, 10);
        });
        
        label.addEventListener('mouseover', function() {
            // Hover effect
            label.style.transform = 'scale(1.15)';
        });
        
        label.addEventListener('mouseout', function() {
            if (!input.checked) {
                label.style.transform = 'scale(1)';
            }
        });
    });
}

/**
 * Scroll animations for elements
 */
function initializeScrollAnimations() {
    if (!('IntersectionObserver' in window)) return;
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    // Observe product cards and review items
    document.querySelectorAll('.product-card, .review-item').forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
        observer.observe(element);
    });
}

/**
 * Format currency to Indian Rupees (₹)
 */
function formatCurrency() {
    const priceElements = document.querySelectorAll('[data-price], .product-price, .product-detail-price');
    
    priceElements.forEach(element => {
        const text = element.textContent.trim();
        
        // Check if already formatted
        if (text.includes('₹')) return;
        
        // Extract number
        let price = parseFloat(text.replace(/[^\d.]/g, ''));
        
        if (!isNaN(price)) {
            // Format price with commas in Indian style
            const formattedPrice = '₹' + Math.round(price).toLocaleString('en-IN');
            element.textContent = formattedPrice;
        }
    });
}

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    const iconClass = type === 'success' ? 'check-circle' : 
                     type === 'error' ? 'exclamation-circle' :
                     type === 'warning' ? 'exclamation-triangle' : 'info-circle';
    
    toast.className = `alert alert-${type}`;
    toast.innerHTML = `
        <i class="fas fa-${iconClass}"></i>
        <span>${message}</span>
    `;
    
    const messagesContainer = document.querySelector('.messages');
    
    if (messagesContainer) {
        messagesContainer.insertBefore(toast, messagesContainer.firstChild);
    } else {
        const mainContent = document.querySelector('main .container');
        if (mainContent) {
            mainContent.insertBefore(toast, mainContent.firstChild);
        }
    }
    
    // Remove after 4 seconds
    setTimeout(() => {
        toast.style.animation = 'fadeOut 0.5s ease-out forwards';
        setTimeout(() => toast.remove(), 500);
    }, 4000);
}

/**
 * Heart beat animation for wishlist button
 */
function animateHeartBeat(element) {
    element.style.animation = 'none';
    setTimeout(() => {
        element.style.animation = 'heartBeat 0.6s ease-in-out';
    }, 10);
}

/**
 * Format numbers with commas (Indian format)
 */
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

/**
 * Quantity input handler
 */
document.addEventListener('change', function(e) {
    if (e.target.classList.contains('quantity-input')) {
        const maxStock = parseInt(e.target.max);
        const value = parseInt(e.target.value);
        
        if (value > maxStock) {
            e.target.value = maxStock;
            showToast(`Maximum quantity available: ${maxStock}`, 'warning');
        } else if (value < 1) {
            e.target.value = 1;
        }
    }
});

/**
 * Add animation keyframes dynamically
 */
const style = document.createElement('style');
style.textContent = `
    @keyframes heartBeat {
        0%, 100% { transform: scale(1); }
        25% { transform: scale(1.3); }
        50% { transform: scale(1.1); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes fadeOut {
        from { opacity: 1; transform: translateY(0); }
        to { opacity: 0; transform: translateY(-10px); }
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-10px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
`;
document.head.appendChild(style);

/**
 * Smooth scroll to anchor links
 */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        if (href !== '#') {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        }
    });
});

/**
 * Rating distribution chart animation
 */
function animateRatingBars() {
    const bars = document.querySelectorAll('.rating-row-fill');
    bars.forEach((bar, index) => {
        const width = bar.style.width;
        bar.style.width = '0';
        
        setTimeout(() => {
            bar.style.transition = 'width 1s ease-out';
            bar.style.width = width;
        }, index * 100);
    });
}

// Call rating animation when page loads
window.addEventListener('load', animateRatingBars);

/**
 * Product image zoom on detail page
 */
const detailImage = document.querySelector('.product-detail-image img');
if (detailImage) {
    detailImage.addEventListener('mousemove', function(e) {
        const rect = this.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        const xPercent = (x / rect.width) * 100;
        const yPercent = (y / rect.height) * 100;
        
        this.style.transformOrigin = `${xPercent}% ${yPercent}%`;
        this.style.transform = 'scale(1.2)';
    });
    
    detailImage.addEventListener('mouseleave', function() {
        this.style.transform = 'scale(1)';
    });
}

console.log('✓ eCommerce app initialized successfully');

/**
 * Toggle review form visibility
 */
function toggleReviewForm() {
    const formContainer = document.getElementById('review-form-container');
    if (formContainer) {
        formContainer.style.display = formContainer.style.display === 'none' ? 'block' : 'none';
        
        // Scroll to form if showing
        if (formContainer.style.display === 'block') {
            formContainer.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }
}

/**
 * Toggle wishlist for product
 */
function toggleWishlist(productId) {
    const button = document.querySelector(`[data-product-id="${productId}"]`);
    if (!button) {
        console.error('Button not found for product:', productId);
        return;
    }
    
    const csrfToken = getCsrfToken();
    if (!csrfToken) {
        showToast('Security token not found. Please refresh the page.', 'error');
        console.error('CSRF token not found');
        return;
    }
    
    const icon = button.querySelector('i');
    const originalClass = icon?.className || 'fa-regular fa-heart';
    
    // Show loading state
    icon.className = 'fas fa-spinner fa-spin';
    
    fetch(`/wishlist/add/${productId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json'
        },
        credentials: 'same-origin'
    })
    .then(response => {
        // Check if response is OK
        if (!response.ok) {
            if (response.status === 403) {
                throw new Error('CSRF token invalid or expired. Please refresh the page.');
            } else if (response.status === 401) {
                throw new Error('Please log in to add items to wishlist.');
            } else if (response.status === 404) {
                throw new Error('Product not found.');
            }
            throw new Error(`Server error: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Wishlist response:', data);
        
        if (data.success) {
            // Update icon
            if (data.added) {
                icon.className = 'fa-solid fa-heart';
                button.classList.add('active');
            } else {
                icon.className = 'fa-regular fa-heart';
                button.classList.remove('active');
            }
            
            // Show notification
            showToast(data.message, 'success');
            
            // Heart animation
            animateHeartBeat(button);
        } else {
            icon.className = originalClass;
            showToast(data.message || 'Error updating wishlist', 'error');
            console.error('Wishlist error:', data);
        }
    })
    .catch(error => {
        console.error('Wishlist error:', error);
        icon.className = originalClass;
        showToast(error.message || 'Error updating wishlist', 'error');
    });
}

/**
 * Initialize mobile menu for new header
 */
function initializeMobileMenu() {
    const hamburger = document.getElementById('hamburger');
    const mobileMenu = document.getElementById('mobile-menu');
    const mobileOverlay = document.getElementById('mobile-menu-overlay');
    const mobileClose = document.getElementById('mobile-menu-close');
    
    if (hamburger && mobileMenu && mobileOverlay) {
        hamburger.addEventListener('click', function() {
            mobileMenu.classList.add('active');
            mobileOverlay.classList.add('active');
            document.body.style.overflow = 'hidden';
        });
        
        mobileClose.addEventListener('click', closeMobileMenu);
        mobileOverlay.addEventListener('click', closeMobileMenu);
        
        // Close on link click
        mobileMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', closeMobileMenu);
        });
    }
}

function closeMobileMenu() {
    const mobileMenu = document.getElementById('mobile-menu');
    const mobileOverlay = document.getElementById('mobile-menu-overlay');
    
    mobileMenu.classList.remove('active');
    mobileOverlay.classList.remove('active');
    document.body.style.overflow = '';
}

/**
 * Update cart count
 */
function updateCartCount() {
    // This would typically fetch cart count from server
    // For now, just update from local storage or count existing items
    const cartCount = document.getElementById('cart-count');
    if (cartCount) {
        // Placeholder - in real app, fetch from API
        const count = localStorage.getItem('cartCount') || '0';
        cartCount.textContent = count;
    }
}

// Initialize new features
document.addEventListener('DOMContentLoaded', function() {
    initializeMobileMenu();
    updateCartCount();
});
