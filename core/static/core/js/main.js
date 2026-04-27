/* ===== FISKAL.AZ — MAIN JS ===== */

// ===== THEME =====
function toggleTheme() {
  const html = document.documentElement;
  const isDark = html.getAttribute('data-theme') === 'dark';
  const newTheme = isDark ? 'light' : 'dark';
  html.setAttribute('data-theme', newTheme);
  const btn = document.getElementById('themeBtn');
  if (btn) btn.textContent = isDark ? '🌙' : '☀️';
  localStorage.setItem('fiskal-theme', newTheme);
}

(function initTheme() {
  const saved = localStorage.getItem('fiskal-theme');
  if (saved) {
    document.documentElement.setAttribute('data-theme', saved);
    const btn = document.getElementById('themeBtn');
    if (btn) btn.textContent = saved === 'light' ? '🌙' : '☀️';
  }
})();

// ===== TAB SWITCH (home page) =====
function switchTab(el) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  el.classList.add('active');
  const tabName = el.textContent.trim();
  const cards = document.querySelectorAll('.card[data-status]');
  cards.forEach(card => {
    if (tabName.includes('Edilən')) {
      card.style.display = '';
    } else {
      const status = card.dataset.status;
      card.style.display = (status === 'confirmed' || status === 'returned') ? '' : 'none';
    }
  });
}

// ===== SEARCH (home page nav) =====
function initSearch() {
  const input = document.querySelector('.nav-search');
  const btn = document.querySelector('.nav-btn');
  if (!input) return;

  const resultsBox = document.createElement('div');
  resultsBox.className = 'search-results';
  resultsBox.id = 'searchResults';
  const page = document.querySelector('.page');
  if (page) page.prepend(resultsBox);

  function doSearch(query) {
    if (!query || query.length < 2) {
      resultsBox.classList.remove('show');
      resultsBox.innerHTML = '';
      return;
    }
    const cards = document.querySelectorAll('.card[data-shop]');
    const matches = [];
    cards.forEach(card => {
      const shop = card.dataset.shop || '';
      const loc = card.dataset.loc || '';
      if (shop.toLowerCase().includes(query.toLowerCase())) {
        matches.push({ shop, loc, status: card.dataset.status });
      }
    });

    if (matches.length === 0) {
      resultsBox.innerHTML = '<div style="padding:14px;text-align:center;font-size:13px;color:var(--text3)">Nəticə tapılmadı</div>';
    } else {
      resultsBox.innerHTML = matches.map(m => `
        <div class="search-result-item" onclick="highlightCard('${m.shop}')">
          <span class="search-result-ico">🛒</span>
          <div>
            <div class="search-result-nm">${m.shop}</div>
            <div class="search-result-loc">${m.loc}</div>
          </div>
        </div>
      `).join('');
    }
    resultsBox.classList.add('show');
  }

  input.addEventListener('input', e => doSearch(e.target.value));
  input.addEventListener('keydown', e => { if (e.key === 'Enter') doSearch(input.value); });
  if (btn) btn.addEventListener('click', () => doSearch(input.value));

  document.addEventListener('click', e => {
    if (!resultsBox.contains(e.target) && e.target !== input && e.target !== btn) {
      resultsBox.classList.remove('show');
    }
  });
}

function highlightCard(shopName) {
  const cards = document.querySelectorAll('.card[data-shop]');
  cards.forEach(card => {
    if (card.dataset.shop === shopName) {
      card.scrollIntoView({ behavior: 'smooth', block: 'center' });
      card.style.borderColor = 'var(--green)';
      setTimeout(() => card.style.borderColor = '', 2000);
    }
  });
  document.getElementById('searchResults').classList.remove('show');
}

// ===== FILE UPLOAD =====
function initFileUpload() {
  const fileInput = document.getElementById('fileInput');
  const uploadZone = document.querySelector('.upload-zone');
  if (!fileInput || !uploadZone) return;

  uploadZone.addEventListener('click', () => fileInput.click());
  fileInput.addEventListener('change', () => {
    const file = fileInput.files[0];
    if (file) {
      let nameEl = uploadZone.querySelector('.upload-name');
      if (!nameEl) {
        nameEl = document.createElement('div');
        nameEl.className = 'upload-name';
        uploadZone.appendChild(nameEl);
      }
      nameEl.textContent = '✅ ' + file.name;
      uploadZone.style.borderColor = 'var(--green)';
    }
  });

  uploadZone.addEventListener('dragover', e => { e.preventDefault(); uploadZone.style.borderColor = 'var(--green)'; });
  uploadZone.addEventListener('dragleave', () => uploadZone.style.borderColor = '');
  uploadZone.addEventListener('drop', e => {
    e.preventDefault();
    const files = e.dataTransfer.files;
    if (files.length) {
      fileInput.files = files;
      fileInput.dispatchEvent(new Event('change'));
    }
  });
}

// ===== BANK CARD MODAL =====
function initBankCardModal() {
  const warnBtn = document.querySelector('.warn-btn');
  if (!warnBtn) return;

  const overlay = document.createElement('div');
  overlay.className = 'modal-overlay';
  overlay.innerHTML = `
    <div class="modal">
      <div class="modal-header">
        <div class="modal-title">💳 Bank Kartı Əlavə Et</div>
        <button class="modal-close" onclick="closeModal()">✕</button>
      </div>
      <div class="form-group">
        <label class="form-label">Kart Nömrəsi</label>
        <input class="form-input" id="cardNumber" placeholder="0000 0000 0000 0000" maxlength="19" oninput="formatCard(this)">
      </div>
      <div class="form-row" style="margin-bottom:14px">
        <div class="form-group" style="margin-bottom:0">
          <label class="form-label">Son Tarix</label>
          <input class="form-input" id="cardExpiry" placeholder="MM/YY" maxlength="5" oninput="formatExpiry(this)">
        </div>
        <div class="form-group" style="margin-bottom:0">
          <label class="form-label">CVV</label>
          <input class="form-input" id="cardCvv" placeholder="123" maxlength="3" type="password">
        </div>
      </div>
      <button class="submit-btn" onclick="saveCard()">Kartı Saxla</button>
    </div>
  `;
  document.body.appendChild(overlay);

  warnBtn.addEventListener('click', () => overlay.classList.add('open'));
  overlay.addEventListener('click', e => { if (e.target === overlay) closeModal(); });
}

function closeModal() {
  document.querySelector('.modal-overlay')?.classList.remove('open');
}

function formatCard(input) {
  let v = input.value.replace(/\D/g, '').slice(0, 16);
  input.value = v.replace(/(.{4})/g, '$1 ').trim();
}

function formatExpiry(input) {
  let v = input.value.replace(/\D/g, '').slice(0, 4);
  if (v.length >= 2) v = v.slice(0, 2) + '/' + v.slice(2);
  input.value = v;
}

function saveCard() {
  const num = document.getElementById('cardNumber')?.value.replace(/\s/g, '');
  const exp = document.getElementById('cardExpiry')?.value;
  const cvv = document.getElementById('cardCvv')?.value;

  if (!num || num.length < 16 || !exp || exp.length < 5 || !cvv || cvv.length < 3) {
    alert('Zəhmət olmasa bütün kart məlumatlarını düzgün daxil edin.');
    return;
  }
  closeModal();
  const pill = document.querySelector('.no-card-pill');
  if (pill) { pill.innerHTML = '💳 Kart əlavə edildi'; pill.style.color = 'var(--green)'; }
  const banner = document.querySelector('.warn-banner');
  if (banner) banner.style.display = 'none';
}

// ===== NOTIFICATION SETTINGS MODAL =====
function openNotifModal() {
  const overlay = document.createElement('div');
  overlay.className = 'modal-overlay open';
  overlay.id = 'notifModal';
  overlay.innerHTML = `
    <div class="modal">
      <div class="modal-header">
        <div class="modal-title">🔔 Bildiriş Parametrləri</div>
        <button class="modal-close" onclick="document.getElementById('notifModal').remove()">✕</button>
      </div>
      <div style="display:flex;flex-direction:column;gap:14px">
        ${[
          ['Şikayət yeniliyi', true],
          ['ƏDV qaytarımı', true],
          ['AI analiz nəticəsi', true],
          ['Xəbər və yeniliklər', false]
        ].map(([label, checked]) => `
          <label style="display:flex;align-items:center;justify-content:space-between;cursor:pointer">
            <span style="font-size:14px">${label}</span>
            <input type="checkbox" ${checked ? 'checked' : ''} style="width:18px;height:18px;accent-color:var(--green)">
          </label>
        `).join('')}
        <button class="submit-btn" onclick="document.getElementById('notifModal').remove();showToast('Parametrlər saxlanıldı ✅')">Saxla</button>
      </div>
    </div>
  `;
  document.body.appendChild(overlay);
  overlay.addEventListener('click', e => { if (e.target === overlay) overlay.remove(); });
}

// ===== LANGUAGE MODAL =====
function openLangModal() {
  const overlay = document.createElement('div');
  overlay.className = 'modal-overlay open';
  overlay.id = 'langModal';
  overlay.innerHTML = `
    <div class="modal">
      <div class="modal-header">
        <div class="modal-title">🌐 Dil Seçimi</div>
        <button class="modal-close" onclick="document.getElementById('langModal').remove()">✕</button>
      </div>
      <div style="display:flex;flex-direction:column;gap:10px">
        ${[['🇦🇿 Azərbaycan dili', true], ['🇷🇺 Русский', false], ['🇬🇧 English', false]].map(([lang, active]) => `
          <div onclick="selectLang(this)" style="display:flex;align-items:center;justify-content:space-between;padding:12px 14px;background:var(--bg3);border:1px solid ${active ? 'var(--green)' : 'var(--border)'};border-radius:var(--radius-sm);cursor:pointer">
            <span style="font-size:14px">${lang}</span>
            ${active ? '<span style="color:var(--green)">✓</span>' : ''}
          </div>
        `).join('')}
      </div>
    </div>
  `;
  document.body.appendChild(overlay);
  overlay.addEventListener('click', e => { if (e.target === overlay) overlay.remove(); });
}

function selectLang(el) {
  document.querySelectorAll('#langModal [onclick="selectLang(this)"]').forEach(d => {
    d.style.borderColor = 'var(--border)';
    d.querySelector('span:last-child')?.remove();
  });
  el.style.borderColor = 'var(--green)';
  const check = document.createElement('span');
  check.style.color = 'var(--green)';
  check.textContent = '✓';
  el.appendChild(check);
  setTimeout(() => { document.getElementById('langModal')?.remove(); showToast('Dil dəyişdirildi ✅'); }, 500);
}

// ===== SUPPORT MODAL =====
function openSupportModal() {
  const overlay = document.createElement('div');
  overlay.className = 'modal-overlay open';
  overlay.id = 'supportModal';
  overlay.innerHTML = `
    <div class="modal">
      <div class="modal-header">
        <div class="modal-title">📞 Dəstək</div>
        <button class="modal-close" onclick="document.getElementById('supportModal').remove()">✕</button>
      </div>
      <div style="display:flex;flex-direction:column;gap:12px">
        <a href="tel:+994125551234" style="display:flex;align-items:center;gap:12px;padding:14px;background:var(--bg3);border:1px solid var(--border);border-radius:var(--radius-sm);text-decoration:none;color:var(--text)">
          <span style="font-size:20px">📞</span>
          <div><div style="font-size:14px;font-weight:600">Zəng et</div><div style="font-size:12px;color:var(--text3)">+994 12 555 12 34</div></div>
        </a>
        <a href="mailto:support@fiskal.az" style="display:flex;align-items:center;gap:12px;padding:14px;background:var(--bg3);border:1px solid var(--border);border-radius:var(--radius-sm);text-decoration:none;color:var(--text)">
          <span style="font-size:20px">✉️</span>
          <div><div style="font-size:14px;font-weight:600">E-mail</div><div style="font-size:12px;color:var(--text3)">support@fiskal.az</div></div>
        </a>
        <div style="text-align:center;font-size:12px;color:var(--text3);padding-top:8px">İş saatları: B.e — Cümə, 09:00 — 18:00</div>
      </div>
    </div>
  `;
  document.body.appendChild(overlay);
  overlay.addEventListener('click', e => { if (e.target === overlay) overlay.remove(); });
}

// ===== PRIVACY MODAL =====
function openPrivacyModal() {
  const overlay = document.createElement('div');
  overlay.className = 'modal-overlay open';
  overlay.id = 'privacyModal';
  overlay.innerHTML = `
    <div class="modal">
      <div class="modal-header">
        <div class="modal-title">🔒 Məxfilik</div>
        <button class="modal-close" onclick="document.getElementById('privacyModal').remove()">✕</button>
      </div>
      <div style="font-size:13px;color:var(--text2);line-height:1.6">
        <p style="margin-bottom:10px">Şəxsi məlumatlarınız Fiskal.az tərəfindən qorunur və üçüncü tərəflərlə paylaşılmır.</p>
        <p style="margin-bottom:10px">Məlumatlarınız yalnız ƏDV qaytarımı prosesi üçün istifadə olunur.</p>
        <button class="submit-btn" onclick="document.getElementById('privacyModal').remove()" style="margin-top:8px">Bağla</button>
      </div>
    </div>
  `;
  document.body.appendChild(overlay);
  overlay.addEventListener('click', e => { if (e.target === overlay) overlay.remove(); });
}

// ===== TOAST =====
function showToast(msg) {
  const t = document.createElement('div');
  t.style.cssText = 'position:fixed;bottom:80px;left:50%;transform:translateX(-50%);background:var(--bg2);border:1px solid var(--border);border-radius:8px;padding:10px 18px;font-size:13px;font-weight:600;z-index:999;box-shadow:0 4px 20px rgba(0,0,0,0.3);white-space:nowrap;color:var(--text)';
  t.textContent = msg;
  document.body.appendChild(t);
  setTimeout(() => t.remove(), 2500);
}

// ===== ANALYTICS CHART =====
function renderChart() {
  const bars = document.querySelectorAll('.chart-bar');
  if (!bars.length) return;
  const maxVal = Math.max(...Array.from(bars).map(b => parseInt(b.dataset.val || 0)));
  bars.forEach(bar => {
    const val = parseInt(bar.dataset.val || 0);
    const pct = maxVal > 0 ? (val / maxVal * 100) : 0;
    bar.style.height = pct + '%';
  });
}

// ===== INIT ON DOM READY =====
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initSearch();
  initFileUpload();
  initBankCardModal();
  renderChart();
});
