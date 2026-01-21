// Main JavaScript for MovieRec

document.addEventListener('DOMContentLoaded', function() {
    
    // Star rating functionality
    initStarRating();
    
    // Auto-hide flash messages
    autoHideAlerts();
    
});

function initStarRating() {
    const starContainers = document.querySelectorAll('.star-rating');
    
    starContainers.forEach(container => {
        const stars = container.querySelectorAll('i');
        const input = container.querySelector('input[type="hidden"]');
        
        stars.forEach((star, index) => {
            star.addEventListener('click', function() {
                const rating = index + 1;
                if (input) {
                    input.value = rating;
                }
                
                // Update star display
                stars.forEach((s, i) => {
                    if (i < rating) {
                        s.classList.remove('far');
                        s.classList.add('fas', 'active');
                    } else {
                        s.classList.remove('fas', 'active');
                        s.classList.add('far');
                    }
                });
            });
            
            // Hover effect
            star.addEventListener('mouseenter', function() {
                const rating = index + 1;
                stars.forEach((s, i) => {
                    if (i < rating) {
                        s.classList.add('hover');
                    } else {
                        s.classList.remove('hover');
                    }
                });
            });
        });
        
        container.addEventListener('mouseleave', function() {
            stars.forEach(s => s.classList.remove('hover'));
        });
    });
}

function autoHideAlerts() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}

// AJAX rating submission
function submitRating(movieId, rating) {
    const formData = new FormData();
    formData.append('rating', rating);
    
    fetch(`/rate/${movieId}`, {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            showToast('Ocena zapisana!', 'success');
        } else {
            showToast('Błąd przy zapisywaniu oceny', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('Błąd połączenia', 'error');
    });
}

function showToast(message, type) {
    // Simple toast notification
    const toast = document.createElement('div');
    toast.className = `alert alert-${type === 'success' ? 'success' : 'danger'} position-fixed top-0 end-0 m-3`;
    toast.style.zIndex = '9999';
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 3000);
}
