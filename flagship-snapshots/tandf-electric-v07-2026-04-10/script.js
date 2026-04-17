/* T&F Electric - Plan B Build | Minimal vanilla JS */

document.addEventListener('DOMContentLoaded', function() {

  /* ===== Promo bar dismiss ===== */
  var dismissBtn = document.querySelector('.promo-bar .dismiss');
  if (dismissBtn) {
    dismissBtn.addEventListener('click', function() {
      document.querySelector('.promo-bar').classList.add('hidden');
    });
  }

  /* ===== Mobile hamburger ===== */
  var hamburger = document.querySelector('.hamburger');
  var mobileMenu = document.querySelector('.mobile-menu');
  if (hamburger && mobileMenu) {
    hamburger.addEventListener('click', function() {
      mobileMenu.classList.toggle('open');
      hamburger.classList.toggle('active');
    });
    // Close on link click
    mobileMenu.querySelectorAll('a').forEach(function(link) {
      link.addEventListener('click', function() {
        mobileMenu.classList.remove('open');
        hamburger.classList.remove('active');
      });
    });
  }

  /* ===== FAQ accordion ===== */
  document.querySelectorAll('.faq-question').forEach(function(btn) {
    btn.addEventListener('click', function() {
      var item = this.closest('.faq-item');
      var wasOpen = item.classList.contains('open');
      // Close all
      document.querySelectorAll('.faq-item').forEach(function(i) {
        i.classList.remove('open');
      });
      // Toggle current
      if (!wasOpen) {
        item.classList.add('open');
      }
    });
  });

  /* ===== Number counter animation (IntersectionObserver) ===== */
  var counters = document.querySelectorAll('[data-count]');
  if (counters.length > 0 && 'IntersectionObserver' in window) {
    var animated = new Set();
    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting && !animated.has(entry.target)) {
          animated.add(entry.target);
          animateCount(entry.target);
        }
      });
    }, { threshold: 0.3 });

    counters.forEach(function(el) { observer.observe(el); });
  }

  function animateCount(el) {
    var target = parseInt(el.getAttribute('data-count'), 10);
    var suffix = el.getAttribute('data-suffix') || '';
    var prefix = el.getAttribute('data-prefix') || '';
    var duration = 1500;
    var start = 0;
    var startTime = null;

    function step(timestamp) {
      if (!startTime) startTime = timestamp;
      var progress = Math.min((timestamp - startTime) / duration, 1);
      // Ease out cubic
      var eased = 1 - Math.pow(1 - progress, 3);
      var current = Math.floor(eased * target);
      el.textContent = prefix + current + suffix;
      if (progress < 1) {
        requestAnimationFrame(step);
      } else {
        el.textContent = prefix + target + suffix;
      }
    }
    requestAnimationFrame(step);
  }

  /* ===== Hero slideshow ===== */
  var slideshowEl = document.getElementById('hero-slideshow');
  if (slideshowEl) {
    var slides = slideshowEl.querySelectorAll('.slide');
    var dots = slideshowEl.querySelectorAll('.dot');
    var currentSlide = 0;
    var interval = null;
    var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function goToSlide(index) {
      slides[currentSlide].classList.remove('active');
      dots[currentSlide].classList.remove('active');
      currentSlide = index;
      slides[currentSlide].classList.add('active');
      dots[currentSlide].classList.add('active');
    }

    function nextSlide() {
      goToSlide((currentSlide + 1) % slides.length);
    }

    function startAutoplay() {
      if (reducedMotion) return;
      interval = setInterval(nextSlide, 4000);
    }

    function stopAutoplay() {
      if (interval) clearInterval(interval);
    }

    // Dot click navigation
    dots.forEach(function(dot) {
      dot.addEventListener('click', function() {
        stopAutoplay();
        goToSlide(parseInt(this.getAttribute('data-slide'), 10));
        startAutoplay();
      });
    });

    // Pause on hover (desktop)
    slideshowEl.addEventListener('mouseenter', stopAutoplay);
    slideshowEl.addEventListener('mouseleave', startAutoplay);

    // Start
    if (!reducedMotion) {
      startAutoplay();
    }
  }

  /* ===== Smooth scroll for anchor links ===== */
  document.querySelectorAll('a[href^="#"]').forEach(function(link) {
    link.addEventListener('click', function(e) {
      var target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

});

(function() {
  const slides = document.querySelectorAll('.hero-photo-slide');
  if (slides.length < 2) return;
  let current = 0;
  setInterval(() => {
    slides[current].classList.remove('active');
    current = (current + 1) % slides.length;
    slides[current].classList.add('active');
  }, 6000);
})();

(function() {
  const form = document.getElementById('contact-form');
  if (!form) return;
  form.addEventListener('submit', async function(e) {
    e.preventDefault();
    const submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
    const originalText = submitBtn ? submitBtn.textContent : '';
    if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = 'Sending...'; }
    try {
      const formData = new FormData(form);
      const response = await fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: { 'Accept': 'application/json' }
      });
      if (response.ok) {
        form.style.display = 'none';
        document.getElementById('contact-success').style.display = 'block';
      } else {
        throw new Error('Form submission failed');
      }
    } catch (err) {
      if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = originalText; }
      alert('Sorry, there was a problem sending your message. Please call (352) 465-4600 directly.');
    }
  });
})();
