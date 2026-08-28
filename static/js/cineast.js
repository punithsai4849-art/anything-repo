/**
 * Cineast Core JavaScript
 * Handles modals, interactive ratings, dropdowns, toasts, and UI interactions
 */

document.addEventListener('DOMContentLoaded', () => {
  // User Dropdown toggle
  const userBtn = document.getElementById('userMenuBtn');
  const userDropdown = document.getElementById('userDropdown');
  
  if (userBtn && userDropdown) {
    userBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      userDropdown.classList.toggle('show');
    });
    
    document.addEventListener('click', () => {
      userDropdown.classList.remove('show');
    });
  }

  // Modal open / close triggers
  document.querySelectorAll('[data-modal-open]').forEach(btn => {
    btn.addEventListener('click', () => {
      const targetId = btn.getAttribute('data-modal-open');
      const modal = document.getElementById(targetId);
      if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
      }
    });
  });

  document.querySelectorAll('[data-modal-close]').forEach(btn => {
    btn.addEventListener('click', () => {
      const modal = btn.closest('.cineast-modal');
      if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
      }
    });
  });

  // Close modal when clicking on overlay outside modal-dialog
  document.querySelectorAll('.cineast-modal').forEach(modal => {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
      }
    });
  });

  // Star rating interactive selector helper
  initStarPickers();
});

// Toast notification helper
window.showToast = function(message, type = 'success') {
  let container = document.getElementById('toastContainer');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }
  
  const toast = document.createElement('div');
  toast.className = `toast-msg toast-${type}`;
  const span = document.createElement('span');
  span.textContent = message;
  toast.appendChild(span);
  container.appendChild(toast);

  
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(8px)';
    toast.style.transition = 'all 0.25s ease';
    setTimeout(() => toast.remove(), 250);
  }, 3500);
};

// CSRF Cookie extraction helper
window.getCookie = function(name) {
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
};

// Interactive Star picker initialization
function initStarPickers() {
  document.querySelectorAll('.rating-star-picker').forEach(picker => {
    const input = picker.querySelector('input[type="hidden"]');
    const stars = picker.querySelectorAll('.star-item');
    const displayLabel = picker.querySelector('.rating-val-label');
    
    stars.forEach(star => {
      star.addEventListener('mouseenter', () => {
        const val = parseFloat(star.dataset.value);
        highlightStars(stars, val);
        if (displayLabel) displayLabel.textContent = val.toFixed(1) + ' / 5.0';
      });
      
      star.addEventListener('click', () => {
        const val = parseFloat(star.dataset.value);
        if (input) input.value = val;
        picker.dataset.selected = val;
        highlightStars(stars, val);
        if (displayLabel) displayLabel.textContent = val.toFixed(1) + ' / 5.0';
      });
    });
    
    picker.addEventListener('mouseleave', () => {
      const current = parseFloat(picker.dataset.selected || (input ? input.value : 0) || 0);
      highlightStars(stars, current);
      if (displayLabel) {
        displayLabel.textContent = current > 0 ? (current.toFixed(1) + ' / 5.0') : 'Select rating';
      }
    });
    
    // Initial highlight
    const initVal = parseFloat(picker.dataset.selected || (input ? input.value : 0) || 0);
    highlightStars(stars, initVal);
  });
}

function highlightStars(stars, rating) {
  stars.forEach(star => {
    const val = parseFloat(star.dataset.value);
    if (val <= rating) {
      star.style.color = 'var(--cineast-primary)';
    } else {
      star.style.color = '#DCDCDC';
    }
  });
}
