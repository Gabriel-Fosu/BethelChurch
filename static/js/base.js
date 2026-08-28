// ── NAVBAR TOGGLE ───────────────────────────────────────────
function toggleNavbar() {
    document.getElementById('navLinks').classList.toggle('active');
}


// ── LOADER + REVEAL ─────────────────────────────────────────
const loader = document.getElementById('loader');

window.addEventListener('load', function() {

    setTimeout(function() {
        if (loader) {
            loader.classList.add('hidden');
            document.body.classList.add('loaded');
        }

        setTimeout(function() {
            if (loader) {
                loader.style.display = 'none';
            }

            revealOnScroll();

        }, 600);

    }, 800);

});


// ── REVEAL ON SCROLL ────────────────────────────────────────
function revealOnScroll() {
    const elements = document.querySelectorAll('.reveal');

    elements.forEach(function(el) {
        const elementTop   = el.getBoundingClientRect().top;
        const windowHeight = window.innerHeight;

        if (elementTop < windowHeight - 80) {
            el.classList.add('visible');
        }
    });
}

window.addEventListener('scroll', revealOnScroll);


// ── ANNOUNCEMENT DISMISS ─────────────────────────────────────
function dismissAnnouncement() {
    const bar = document.getElementById('announcementBar');
    if (bar) {
        bar.style.display = 'none';
        sessionStorage.setItem('announcementDismissed', 'true');
    }
}

if (sessionStorage.getItem('announcementDismissed')) {
    const bar = document.getElementById('announcementBar');
    if (bar) bar.style.display = 'none';
}