/**
 * Market E-Commerce Platform - Main JavaScript
 */

// CSRF Token Setup for AJAX
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document. cookie !== '') {
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

// Setup AJAX with CSRF token
$. ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) && ! this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

// Add to Cart with AJAX
$(document).on('submit', '. add-to-cart-form', function(e) {
    e.preventDefault();

    const form = $(this);
    const url = form.attr('action');
    const data = form.serialize();

    $.ajax({
        url: url,
        type: 'POST',
        data: data,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        },
        success: function(response) {
            if (response.success) {
                // Update cart count
                $('. cart-count').text(response.cart_count);

                // Show success toast
                showToast('success', response.message);
            }
        },
        error: function() {
            showToast('error', 'Failed to add item to cart');
        }
    });
});

// Show Toast Notification
function showToast(type, message) {
    const toastHTML = `
        <div class="toast align-items-center text-white bg-${type === 'success' ? 'success' : 'danger'} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;

    // Create toast container if not exists
    if ($('#toastContainer').length === 0) {
        $('body').append('<div id="toastContainer" class="toast-container position-fixed top-0 end-0 p-3"></div>');
    }

    const $toast = $(toastHTML);
    $('#toastContainer').append($toast);

    const toast = new bootstrap.Toast($toast[0]);
    toast.show();

    // Remove after hidden
    $toast.on('hidden.bs. toast', function() {
        $(this).remove();
    });
}

// Auto-hide alerts after 5 seconds
$(document).ready(function() {
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);
});

// Lazy loading images
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries. forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry. target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });

    document.querySelectorAll('img.lazy').forEach(img => {
        imageObserver.observe(img);
    });
}

// Smooth scroll
$('a[href^="#"]').on('click', function(e) {
    const target = $(this.getAttribute('href'));
    if (target.length) {
        e.preventDefault();
        $('html, body').stop().animate({
            scrollTop: target.offset().top - 80
        }, 1000);
    }
});

// Product quantity controls
function updateQuantity(input, change) {
    const currentValue = parseInt(input.value) || 1;
    const min = parseInt(input.min) || 1;
    const max = parseInt(input.max) || 999;

    const newValue = currentValue + change;

    if (newValue >= min && newValue <= max) {
        input.value = newValue;
    }
}

// Search with debounce
let searchTimeout;
$('#searchInput').on('input', function() {
    clearTimeout(searchTimeout);
    const query = $(this).val();

    if (query. length >= 3) {
        searchTimeout = setTimeout(function() {
            // Implement search AJAX here
            console.log('Searching for:', query);
        }, 500);
    }
});

// Initialize Bootstrap tooltips
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
});

// Initialize Bootstrap popovers
var popoverTriggerList = [].slice.call(document. querySelectorAll('[data-bs-toggle="popover"]'))
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl)
});

console.log('Market platform initialized successfully!  🚀');