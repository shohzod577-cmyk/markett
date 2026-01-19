// Product Like Functionality
function toggleProductLike(productId, button) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    fetch(`/products/like/${productId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        credentials: 'same-origin'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update button state
            const icon = button.querySelector('i');
            if (data.liked) {
                icon.classList.remove('bi-heart');
                icon.classList.add('bi-heart-fill');
                button.classList.add('liked');
            } else {
                icon.classList.remove('bi-heart-fill');
                icon.classList.add('bi-heart');
                button.classList.remove('liked');
            }
            
            // Update likes count
            const countElement = button.querySelector('.likes-count');
            if (countElement) {
                countElement.textContent = data.likes_count;
            }
            
            // Show notification
            showNotification(data.message, 'success');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Please login to like products', 'error');
    });
}

// Initialize like buttons
document.addEventListener('DOMContentLoaded', function() {
    const likeButtons = document.querySelectorAll('.like-btn');
    
    likeButtons.forEach(button => {
        const productId = button.dataset.productId;
        
        // Get initial like status
        fetch(`/products/like-status/${productId}/`)
            .then(response => response.json())
            .then(data => {
                if (data.liked) {
                    const icon = button.querySelector('i');
                    icon.classList.remove('bi-heart');
                    icon.classList.add('bi-heart-fill');
                    button.classList.add('liked');
                }
            })
            .catch(error => console.error('Error loading like status:', error));
        
        // Add click event
        button.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            toggleProductLike(productId, this);
        });
    });
});

function showNotification(message, type) {
    // Simple notification system
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'success' ? 'success' : 'danger'} position-fixed top-0 end-0 m-3`;
    notification.style.zIndex = '9999';
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}
