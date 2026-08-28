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

// ==========================================================================
// Interactive Onboarding Guided Tour System
// ==========================================================================

const TOUR_STEPS = [
  {
    step: 1,
    badge: "Universal Index",
    title: "Welcome to anything...",
    icon: "🌐",
    description: "The universal evaluation platform designed for everything. Discover, rate, and review physical products, books, films, gadgets, places, apps, theories, and emotions.",
    features: ["20 Universal Categories", "Bento Grid Discovery", "Dynamic Metadata", "Full-Text Instant Search"]
  },
  {
    step: 2,
    badge: "Ratings & Perspectives",
    title: "Rate & Review Anything",
    icon: "★",
    description: "Express your opinions with half-star precision from 0.5★ to 5.0★. Write in-depth perspectives and compare community ratings across diverse categories.",
    features: ["10-Increment Star Scale", "Aggregate Score Metrics", "Authentic Community Logs", "One-Click Quick Ratings"]
  },
  {
    step: 3,
    badge: "Open Indexing",
    title: "Add Any Entity in Seconds",
    icon: "➕",
    description: "Missing a tool, concept, movie, or landmark? Anyone can index new items with category-tailored dynamic properties, tags, and image uploads.",
    features: ["Category-Specific Schema", "Direct Media Uploads", "Semantic Hash Tagging", "Entity Relationships"]
  },
  {
    step: 4,
    badge: "Knowledge Base",
    title: "Community Edits & History",
    icon: "📝",
    description: "Contribute to descriptions and properties Wikipedia-style. Every modification is attributed to the user with a transparent revision audit trail.",
    features: ["Transparent Audit Log", "Before & After Diffs", "Community Attribution", "Content Moderation Tools"]
  },
  {
    step: 5,
    badge: "Social Cards",
    title: "Export & Share Anywhere",
    icon: "🎨",
    description: "Convert any rating and review into a beautiful, high-resolution 1200x630 visual card generated client-side for Twitter, Instagram, or messaging.",
    features: ["1200x630 Social Format", "Neubrutalist Visual Styling", "One-Click PNG Export", "Direct Sharing Link"]
  }
];

let currentTourIndex = 0;

window.startOnboardingTour = function(forceStart = false) {
  if (!forceStart && localStorage.getItem('anything_tour_completed') === 'true') {
    return;
  }

  currentTourIndex = 0;
  let backdrop = document.getElementById('onboardingTourBackdrop');
  if (!backdrop) {
    createTourDOM();
    backdrop = document.getElementById('onboardingTourBackdrop');
  }
  renderTourStep(0);
  backdrop.classList.add('active');
  document.body.style.overflow = 'hidden';
};

window.closeOnboardingTour = function() {
  const backdrop = document.getElementById('onboardingTourBackdrop');
  if (backdrop) {
    backdrop.classList.remove('active');
    document.body.style.overflow = '';
  }
  localStorage.setItem('anything_tour_completed', 'true');
};

function renderTourStep(index) {
  const step = TOUR_STEPS[index];
  if (!step) return;

  currentTourIndex = index;
  document.getElementById('tourStepBadge').textContent = step.badge;
  document.getElementById('tourStepCount').textContent = `Step ${index + 1} of ${TOUR_STEPS.length}`;
  document.getElementById('tourIconBox').textContent = step.icon;
  document.getElementById('tourTitle').textContent = step.title;
  document.getElementById('tourDesc').textContent = step.description;

  // Features
  const featContainer = document.getElementById('tourFeatures');
  featContainer.innerHTML = step.features.map(f => `
    <div class="tour-feature-item">
      <span style="color: var(--cineast-primary); font-weight: 900;">✓</span>
      <span>${f}</span>
    </div>
  `).join('');

  // Dots
  const dotsContainer = document.getElementById('tourProgressDots');
  dotsContainer.innerHTML = TOUR_STEPS.map((_, i) => `
    <div class="tour-dot ${i === index ? 'active' : ''}"></div>
  `).join('');

  // Buttons
  const prevBtn = document.getElementById('tourPrevBtn');
  const nextBtn = document.getElementById('tourNextBtn');

  if (index === 0) {
    prevBtn.style.display = 'none';
  } else {
    prevBtn.style.display = 'inline-block';
  }

  if (index === TOUR_STEPS.length - 1) {
    nextBtn.textContent = 'Get Started';
    nextBtn.className = 'btn btn-primary btn-md';
  } else {
    nextBtn.textContent = 'Next →';
    nextBtn.className = 'btn btn-primary btn-md';
  }
}

function createTourDOM() {
  const div = document.createElement('div');
  div.id = 'onboardingTourBackdrop';
  div.className = 'tour-backdrop';
  div.innerHTML = `
    <div class="tour-card">
      <div class="tour-header">
        <span class="tour-badge" id="tourStepBadge">Universal Index</span>
        <span class="tour-step-count" id="tourStepCount">Step 1 of 5</span>
      </div>
      
      <div class="tour-icon-box" id="tourIconBox" style="background: var(--bg-subtle);">🌐</div>
      <h2 class="tour-title" id="tourTitle">Welcome to anything...</h2>
      <p class="tour-desc" id="tourDesc"></p>
      
      <div class="tour-feature-list" id="tourFeatures"></div>
      
      <div class="tour-footer">
        <div class="tour-progress-dots" id="tourProgressDots"></div>
        <div class="tour-actions">
          <button type="button" class="btn btn-secondary btn-sm" id="tourSkipBtn" onclick="closeOnboardingTour()">Skip</button>
          <button type="button" class="btn btn-secondary btn-sm" id="tourPrevBtn" onclick="prevTourStep()" style="display: none;">← Back</button>
          <button type="button" class="btn btn-primary btn-md" id="tourNextBtn" onclick="nextTourStep()">Next →</button>
        </div>
      </div>
    </div>
  `;
  document.body.appendChild(div);
}

window.nextTourStep = function() {
  if (currentTourIndex < TOUR_STEPS.length - 1) {
    renderTourStep(currentTourIndex + 1);
  } else {
    closeOnboardingTour();
    window.showToast('You are ready to explore and review anything!', 'success');
  }
};

window.prevTourStep = function() {
  if (currentTourIndex > 0) {
    renderTourStep(currentTourIndex - 1);
  }
};

// Check if new registration tour was requested by session
document.addEventListener('DOMContentLoaded', () => {
  if (document.body.dataset.showTour === 'true') {
    setTimeout(() => {
      window.startOnboardingTour(true);
    }, 600);
  }
});
