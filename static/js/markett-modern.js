/**
 * Markett - Modern JavaScript
 * Optimized for Uzum Market style e-commerce
 */

// ============================================
// CSRF Token Setup
// ============================================
function getCookie(name) {
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
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// ============================================
// Notification System
// ============================================
class NotificationManager {
    static show(type, message, duration = 3000) {
        const notification = document.createElement('div');
        notification.className = `notification-modern notification-${type}`;
        notification.innerHTML = `
            <i class="bi bi-${type === 'success' ? 'check-circle-fill' : 'x-circle-fill'}"></i>
            <span>${message}</span>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => notification.classList.add('show'), 100);
        
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, duration);
    }
}

// Add notification styles
const notificationStyles = document.createElement('style');
notificationStyles.textContent = `
.notification-modern {
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 16px 24px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    gap: 12px;
    font-weight: 500;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    z-index: 10000;
    transform: translateX(400px);
    transition: transform 0.3s ease;
}

.notification-modern.show {
    transform: translateX(0);
}

.notification-modern.notification-success {
    background: #10b981;
    color: white;
}

.notification-modern.notification-error {
    background: #ef4444;
    color: white;
}

.notification-modern i {
    font-size: 1.5rem;
}
`;
document.head.appendChild(notificationStyles);

// ============================================
// Export functions for global use
// ============================================
window.showNotification = (type, message) => NotificationManager.show(type, message);

// Cart functions
window.addToCart = async function(productId, quantity = 1) {
    try {
        const response = await fetch(`/cart/add/${productId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ quantity })
        });
        
        const data = await response.json();
        
        if (data.success) {
            NotificationManager.show('success', data.message || 'Mahsulot savatga qo\'shildi!');
            // Update cart badge
            const badge = document.querySelector('.cart-badge');
            if (badge && data.cart_count) {
                badge.textContent = data.cart_count;
                badge.style.display = 'flex';
            }
            setTimeout(() => location.reload(), 1000);
        } else {
            NotificationManager.show('error', data.message || 'Xatolik yuz berdi');
        }
    } catch (error) {
        console.error('Error:', error);
        NotificationManager.show('error', 'Xatolik yuz berdi');
    }
};

window.removeFromCart = async function(itemId) {
    if (!confirm('Mahsulotni o\'chirmoqchimisiz?')) return;
    
    try {
        const response = await fetch(`/cart/remove/${itemId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            }
        });
        
        const data = await response.json();
        if (data.success) {
            location.reload();
        }
    } catch (error) {
        console.error('Error:', error);
    }
};

window.updateCartQuantity = async function(itemId, quantity) {
    try {
        const response = await fetch(`/cart/update/${itemId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ quantity })
        });
        
        const data = await response.json();
        if (data.success) {
            location.reload();
        }
    } catch (error) {
        console.error('Error:', error);
    }
};

// Wishlist functions
window.toggleFavorite = async function(productId) {
    try {
        const response = await fetch(`/wishlist/toggle/${productId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            }
        });
        
        const data = await response.json();
        if (data.success) {
            NotificationManager.show('success', data.message);
        }
    } catch (error) {
        console.error('Error:', error);
    }
};

// Image gallery
window.changeMainImage = function(imageUrl, thumbnail) {
    const mainImg = document.getElementById('mainImage');
    if (mainImg) mainImg.src = imageUrl;
    
    document.querySelectorAll('.thumbnail').forEach(t => t.classList.remove('active'));
    if (thumbnail) thumbnail.classList.add('active');
};

// Quantity controls
window.increaseQuantity = function() {
    const input = document.getElementById('quantityInput');
    if (input) {
        const max = parseInt(input.getAttribute('max'));
        const current = parseInt(input.value);
        if (current < max) input.value = current + 1;
    }
};

window.decreaseQuantity = function() {
    const input = document.getElementById('quantityInput');
    if (input) {
        const current = parseInt(input.value);
        if (current > 1) input.value = current - 1;
    }
};

// Initialize on load
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(el => new bootstrap.Tooltip(el));
    
    // Lazy load images
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                        imageObserver.unobserve(img);
                    }
                }
            });
        });
        
        document.querySelectorAll('img.lazy').forEach(img => imageObserver.observe(img));
    }
});
