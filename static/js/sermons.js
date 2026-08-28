// ── CURRENT STATE ───────────────────────────────────────────
let currentState = {
    q: '',
    speaker: '',
    series: '',
    page: 1,
};

// ── VIEW TOGGLE ─────────────────────────────────────────────
function switchView(view) {
    const grid    = document.getElementById('gridView');
    const list    = document.getElementById('listView');
    const gridBtn = document.getElementById('gridBtn');
    const listBtn = document.getElementById('listBtn');

    if (view === 'grid') {
        grid.style.display = '';
        list.style.display = 'none';
        gridBtn.classList.add('active');
        listBtn.classList.remove('active');
        localStorage.setItem('sermonView', 'grid');
    } else {
        grid.style.display = 'none';
        list.style.display = '';
        listBtn.classList.add('active');
        gridBtn.classList.remove('active');
        localStorage.setItem('sermonView', 'list');
    }
}

// Remember preferred view across page loads
window.addEventListener('load', function() {
    const saved = localStorage.getItem('sermonView');
    if (saved === 'list') switchView('list');
});

// ── INTERCEPT SEARCH FORM ───────────────────────────────────
const filterForm = document.getElementById('filterForm');
const clearBtn   = document.getElementById('clearBtn');

filterForm.addEventListener('submit', function(e) {
    e.preventDefault();
    currentState.q       = document.querySelector('input[name="q"]').value;
    currentState.speaker = document.querySelector('select[name="speaker"]').value;
    currentState.series  = document.querySelector('select[name="series"]').value;
    currentState.page    = 1;
    loadSermons();
});

clearBtn.addEventListener('click', function(e) {
    e.preventDefault();
    document.querySelector('input[name="q"]').value       = '';
    document.querySelector('select[name="speaker"]').value = '';
    document.querySelector('select[name="series"]').value  = '';
    currentState = { q: '', speaker: '', series: '', page: 1 };
    loadSermons();
});

// ── FETCH SERMONS ───────────────────────────────────────────
function loadSermons() {
    const url = `/sermons/results/?q=${currentState.q}&speaker=${currentState.speaker}&series=${currentState.series}&page=${currentState.page}`;

    document.getElementById('gridView').style.opacity = '0.4';
    document.getElementById('listView').style.opacity = '0.4';

    fetch(url)
        .then(function(res) { return res.json(); })
        .then(function(data) {
            renderGrid(data.sermons);
            renderList(data.sermons);
            renderPagination(data.page, data.total_pages);
            updateCount(data.total);

            document.getElementById('gridView').style.opacity = '1';
            document.getElementById('listView').style.opacity = '1';

            document.getElementById('sermonsWrapper').scrollIntoView({
                behavior: 'smooth', block: 'start'
            });
        });
}

// ── RENDER GRID ─────────────────────────────────────────────
function renderGrid(sermons) {
    const grid = document.getElementById('gridView');
    if (sermons.length === 0) {
        grid.innerHTML = `
            <div class="no-results">
                <p>No sermons found. Try adjusting your search.</p>
            </div>`;
        return;
    }
    grid.innerHTML = sermons.map(function(s) {
        return `
        <a href="/sermons/${s.slug}/" class="sermon-card">
            <div class="sermon-thumb">
                <div class="play-btn">
                    <div class="play-icon"></div>
                </div>
            </div>
            <div class="sermon-info">
                <div class="sermon-series">${s.series}</div>
                <div class="sermon-title">${s.title}</div>
                <div class="sermon-meta">${s.speaker} · ${s.date}</div>
                <div class="sermon-meta">${s.scripture}</div>
            </div>
        </a>`;
    }).join('');
}

// ── RENDER LIST ─────────────────────────────────────────────
function renderList(sermons) {
    const list = document.getElementById('listView');
    if (sermons.length === 0) {
        list.innerHTML = `
            <p style="padding:2rem; text-align:center; color:var(--text-light);">
                No sermons found.
            </p>`;
        return;
    }
    list.innerHTML = sermons.map(function(s) {
        return `
        <a href="/sermons/${s.slug}/" class="sermon-row">
            <div class="sermon-row-thumb">
                <div class="play-icon"></div>
            </div>
            <div class="sermon-row-info">
                <div class="sermon-row-title">${s.title}</div>
                <div class="sermon-row-meta">
                    <span>${s.speaker}</span>
                    <span>${s.date}</span>
                </div>
            </div>
            <span class="sermon-row-series">${s.series}</span>
            <span class="sermon-row-scripture">${s.scripture}</span>
        </a>`;
    }).join('');
}

// ── RENDER PAGINATION ───────────────────────────────────────
function renderPagination(page, totalPages) {
    const pagination = document.getElementById('pagination');
    if (totalPages <= 1) {
        pagination.innerHTML = '';
        return;
    }
    let html = '';
    if (page > 1) {
        html += `<a class="page-btn" onclick="goToPage(${page - 1})" href="#">‹</a>`;
    }
    for (let p = 1; p <= totalPages; p++) {
        html += `<a class="page-btn ${p === page ? 'active' : ''}"
            onclick="goToPage(${p})" href="#">${p}</a>`;
    }
    if (page < totalPages) {
        html += `<a class="page-btn" onclick="goToPage(${page + 1})" href="#">›</a>`;
    }
    pagination.innerHTML = html;
}

// ── GO TO PAGE ──────────────────────────────────────────────
function goToPage(p) {
    currentState.page = p;
    loadSermons();
}

// ── UPDATE COUNT ────────────────────────────────────────────
function updateCount(total) {
    document.getElementById('resultsCount').innerHTML =
        `Showing <strong>${total}</strong> sermon${total !== 1 ? 's' : ''}`;
}