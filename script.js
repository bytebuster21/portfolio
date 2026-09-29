// Portfolio JavaScript for Mehak Wadhwa

document.addEventListener('DOMContentLoaded', () => {
  // ── 1. Scroll Reveal Observer ────────────────────────────
  const revealElements = document.querySelectorAll('.reveal');
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        // Staggered reveal for sibling elements
        const siblings = Array.from(entry.target.parentElement.querySelectorAll('.reveal'));
        const index = siblings.indexOf(entry.target);
        const delay = Math.min(index * 90, 400);

        setTimeout(() => {
          entry.target.classList.add('visible');
        }, delay);

        revealObserver.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.1,
    rootMargin: '0px 0px -40px 0px'
  });

  revealElements.forEach(el => revealObserver.observe(el));

  // ── 2. Mobile Navigation Toggle ──────────────────────────
  const menuToggle = document.getElementById('menuToggle');
  const navLinks = document.getElementById('navLinks');

  if (menuToggle && navLinks) {
    menuToggle.addEventListener('click', () => {
      navLinks.classList.toggle('active');
      const icon = menuToggle.querySelector('i');
      if (icon) {
        if (navLinks.classList.contains('active')) {
          icon.classList.remove('fa-bars');
          icon.classList.add('fa-xmark');
        } else {
          icon.classList.remove('fa-xmark');
          icon.classList.add('fa-bars');
        }
      }
    });

    // Close menu when clicking link
    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('active');
        const icon = menuToggle.querySelector('i');
        if (icon) {
          icon.classList.remove('fa-xmark');
          icon.classList.add('fa-bars');
        }
      });
    });
  }

  // ── 3. Active Nav Link on Scroll ─────────────────────────
  const sections = document.querySelectorAll('section[id]');
  window.addEventListener('scroll', () => {
    const scrollY = window.pageYOffset;
    sections.forEach(current => {
      const sectionHeight = current.offsetHeight;
      const sectionTop = current.offsetTop - 120;
      const sectionId = current.getAttribute('id');
      const matchingLink = document.querySelector(`.nav-links a[href*="${sectionId}"]`);

      if (matchingLink) {
        if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
          matchingLink.classList.add('active-nav');
        } else {
          matchingLink.classList.remove('active-nav');
        }
      }
    });

    // ── 4. Scroll To Top Visibility ────────────────────────
    const scrollTopBtn = document.getElementById('scrollTopBtn');
    if (scrollTopBtn) {
      if (window.scrollY > 400) {
        scrollTopBtn.classList.add('visible');
      } else {
        scrollTopBtn.classList.remove('visible');
      }
    }
  });

  // Scroll to Top action
  const scrollTopBtn = document.getElementById('scrollTopBtn');
  if (scrollTopBtn) {
    scrollTopBtn.addEventListener('click', () => {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }

  // ── 5. Mobile Tap to Expand Details for Flip Cards ───────
  const flipCards = document.querySelectorAll('.flip-card');
  flipCards.forEach(card => {
    const tapBtn = card.querySelector('.mobile-tap-btn');
    const mobileDetails = card.querySelector('.mobile-details');

    if (tapBtn && mobileDetails) {
      tapBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        const isOpen = mobileDetails.classList.toggle('open');
        tapBtn.innerHTML = isOpen
          ? '<i class="fa-solid fa-chevron-up"></i> Hide Details'
          : '<i class="fa-solid fa-circle-info"></i> View Details';
      });
    }
  });

  // ── 6. Contact Form & Toast Notification ─────────────────
  const contactForm = document.getElementById('contactForm');
  const toastNotice = document.getElementById('toastNotice');

  window.showToast = function (message, duration = 4000) {
    if (!toastNotice) return;
    toastNotice.querySelector('.toast-text').textContent = message;
    toastNotice.classList.add('show');
    setTimeout(() => {
      toastNotice.classList.remove('show');
    }, duration);
  };

  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();

      const name = document.getElementById('formName').value.trim();
      const email = document.getElementById('formEmail').value.trim();
      const subject = document.getElementById('formSubject').value.trim() || 'New Portfolio Message from ' + name;
      const message = document.getElementById('formMessage').value.trim();

      if (!name || !email || !message) {
        showToast('Please fill out all required fields.');
        return;
      }

      // Generate mailto link
      const bodyContent = `Name: ${name}\nEmail: ${email}\n\nMessage:\n${message}`;
      const mailtoUrl = `mailto:wadhwam50@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(bodyContent)}`;

      // Open email client
      window.location.href = mailtoUrl;

      // Show user feedback
      showToast('Opening your email client to send the message! Thank you, ' + name + '!');
      contactForm.reset();
    });
  }

  // ── 7. Resume Button Click Handler ──────────────────────
  document.querySelectorAll('a[href*="resume"], .nav-resume-btn').forEach(btn => {
    btn.setAttribute('href', 'resume.pdf');
    btn.setAttribute('target', '_blank');
    btn.setAttribute('rel', 'noopener noreferrer');
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      window.open('resume.pdf', '_blank');
    });
  });
});
