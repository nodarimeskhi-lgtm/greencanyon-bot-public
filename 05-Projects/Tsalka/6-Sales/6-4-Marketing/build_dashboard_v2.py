import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Read plots JS data
with open(r'C:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\plots_js.txt', 'r', encoding='utf-8') as f:
    plots_js = f.read()

# Read the partial HTML we already wrote
with open(r'C:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\sales_dashboard_v2.html', 'r', encoding='utf-8') as f:
    partial = f.read()

# Build the JS/logic part
js_logic = r"""
// ============================================
// STATE
// ============================================
let PLOTS = [];
let filtered = [];
let sortKey = 'id';
let sortAsc = true;
let currentPage = 1;
let selectedPlot = null;
const PAGE_SIZE = CONFIG.pageSize;

// ============================================
// GOOGLE SHEETS FETCH
// ============================================
async function fetchFromSheets(url) {
  setSyncStatus('loading', 'სინქრონიზაცია...');
  try {
    // Use CORS proxy for Google Sheets CSV
    const response = await fetch(url);
    if (!response.ok) throw new Error('HTTP ' + response.status);
    const csv = await response.text();
    
    return new Promise((resolve, reject) => {
      Papa.parse(csv, {
        header: true,
        skipEmptyLines: true,
        complete: (results) => {
          const rows = results.data.map(row => ({
            id: row.id || '',
            zone: row.zone || 'LA',
            area: parseFloat(row.area) || 500,
            sqm: parseFloat(row.sqm) || 115,
            style: row.style || 'Barnhouse',
            land_price: parseFloat(row.land_price) || 100,
            build_cost: parseFloat(row.build_cost) || 1750,
            daily_rent: parseFloat(row.daily_rent) || 200,
            roi_file: parseFloat(row.roi_file) || 10,
            ah_price: row.ah_price ? parseFloat(row.ah_price) : null,
            status: (row.status || 'free').toLowerCase().trim(),
            notes: row.notes || ''
          })).filter(r => r.id);
          resolve(rows);
        },
        error: reject
      });
    });
  } catch (e) {
    throw e;
  }
}

async function loadData() {
  showLoading(true, 'მონაცემები იტვირთება...');
  
  if (CONFIG.sheetsUrl) {
    try {
      document.getElementById('loading-sub').textContent = 'Google Sheets-დან სინქრონიზაცია...';
      const rows = await fetchFromSheets(CONFIG.sheetsUrl);
      if (rows.length > 0) {
        PLOTS = rows;
        setSyncStatus('ok', 'Sheets სინქ. ✓');
        document.getElementById('data-source-info').textContent = 'Google Sheets (live)';
        document.getElementById('sheets-open-link').style.display = 'inline';
        document.getElementById('sheets-open-link').href = CONFIG.sheetsUrl.replace('/pub?output=csv','').replace('output=csv','');
        document.getElementById('banner-title').textContent = '✅ Google Sheets — Live სინქრონიზაცია';
        document.getElementById('banner-desc').textContent = 'მონაცემები პირდაპირ Google Sheets-დან. ცვლილება Sheets-ში = ავტო-განახლება.';
        document.getElementById('last-sync').textContent = new Date().toLocaleTimeString('ka-GE');
        showLoading(false);
        initDashboard();
        return;
      }
    } catch (e) {
      console.warn('Sheets fetch failed:', e);
      setSyncStatus('err', 'Sheets შეცდომა');
    }
  }
  
  // Fallback to embedded data
  PLOTS = EMBEDDED_PLOTS;
  setSyncStatus('ok', 'ჩაშენებული მონ.');
  document.getElementById('data-source-info').textContent = 'ჩაშენებული (Settlement Excel)';
  document.getElementById('last-sync').textContent = 'ჩაშენებული მონაცემები';
  document.getElementById('banner-desc').textContent = 'ახლა გამოიყენება ჩაშენებული მონაცემები. Google Sheets-ის შეერთებისთვის დააჭირეთ ⚙️';
  showLoading(false);
  initDashboard();
}

// ============================================
// REFRESH
// ============================================
async function manualRefresh() {
  if (!CONFIG.sheetsUrl) { openModal(); return; }
  showLoading(true, 'განახლება...');
  try {
    const rows = await fetchFromSheets(CONFIG.sheetsUrl);
    if (rows.length > 0) {
      PLOTS = rows;
      document.getElementById('last-sync').textContent = new Date().toLocaleTimeString('ka-GE');
      setSyncStatus('ok', 'Sheets სინქ. ✓');
    }
  } catch(e) {
    setSyncStatus('err', 'შეცდომა');
  }
  showLoading(false);
  initDashboard();
}

// Auto-refresh
setInterval(() => {
  if (CONFIG.sheetsUrl) manualRefresh();
}, CONFIG.refreshInterval);

// ============================================
// SHEETS MODAL
// ============================================
function openModal() { document.getElementById('setup-modal').classList.add('open'); }
function closeModal() { document.getElementById('setup-modal').classList.remove('open'); }

function connectSheets() {
  const url = document.getElementById('sheets-url-input').value.trim();
  if (!url.includes('docs.google.com') && !url.includes('output=csv')) {
    alert('სწორი Google Sheets Publish URL ჩასვით! (output=csv ბოლოში უნდა იყოს)');
    return;
  }
  CONFIG.sheetsUrl = url;
  localStorage.setItem('gc_sheets_url', url);
  closeModal();
  loadData();
}

// ============================================
// UI HELPERS
// ============================================
function showLoading(show, msg) {
  document.getElementById('loading-overlay').style.display = show ? 'flex' : 'none';
  if (msg) document.querySelector('.loading-text').textContent = msg;
}

function setSyncStatus(state, label) {
  const dot = document.getElementById('sync-dot');
  dot.className = 'sync-dot ' + state;
  document.getElementById('sync-label').textContent = label;
}

// ============================================
// DASHBOARD LOGIC
// ============================================
function initDashboard() {
  updateSummary();
  applyFilters();
}

function calcPrice(p) {
  if (p.ah_price) return p.ah_price;
  return Math.round((p.area * p.land_price) + (p.sqm * p.build_cost));
}

function calcROI(p, occ=0.45, mgmt=0.40) {
  const capex = calcPrice(p);
  const gross = p.daily_rent * 365 * occ;
  const net = gross * (1 - mgmt) * 0.82;
  return capex > 0 ? (net / capex * 100) : 0;
}

function updateSummary() {
  const free     = PLOTS.filter(p => p.status === 'free').length;
  const reserved = PLOTS.filter(p => p.status === 'reserved').length;
  const sold     = PLOTS.filter(p => p.status === 'sold').length;
  const val = PLOTS.filter(p => p.status === 'free').reduce((s,p) => s + calcPrice(p), 0);
  document.getElementById('stat-total').textContent    = PLOTS.length;
  document.getElementById('stat-free').textContent     = free;
  document.getElementById('stat-reserved').textContent = reserved;
  document.getElementById('stat-sold').textContent     = sold;
  document.getElementById('stat-value').textContent    = '$' + Math.round(val/1000) + 'K';
}

function applyFilters() {
  const zone   = document.getElementById('filter-zone').value;
  const status = document.getElementById('filter-status').value;
  const type   = document.getElementById('filter-type').value;
  const q      = (document.getElementById('search-box').value || '').toLowerCase();

  filtered = PLOTS.filter(p => {
    if (zone   !== 'all' && p.zone   !== zone)   return false;
    if (status !== 'all' && p.status !== status) return false;
    if (type   !== 'all' && p.style  !== type)   return false;
    if (q && !p.id.toLowerCase().includes(q) && !p.style.toLowerCase().includes(q) && !(p.notes||'').toLowerCase().includes(q)) return false;
    return true;
  });
  currentPage = 1;
  sortAndRender();
}

function sortTable(key) {
  if (sortKey === key) sortAsc = !sortAsc;
  else { sortKey = key; sortAsc = true; }
  sortAndRender();
}

function sortAndRender() {
  filtered.sort((a, b) => {
    let va, vb;
    if (sortKey === 'price') { va = calcPrice(a); vb = calcPrice(b); }
    else if (sortKey === 'roi') { va = calcROI(a); vb = calcROI(b); }
    else { va = a[sortKey]; vb = b[sortKey]; }
    if (typeof va === 'string') return sortAsc ? va.localeCompare(vb) : vb.localeCompare(va);
    return sortAsc ? va - vb : vb - va;
  });
  renderTable();
}

function renderTable() {
  const tbody = document.getElementById('inv-tbody');
  tbody.innerHTML = '';

  const start = (currentPage - 1) * PAGE_SIZE;
  const page  = filtered.slice(start, start + PAGE_SIZE);

  if (!page.length) {
    tbody.innerHTML = '<tr><td colspan="9"><div class="empty-state">🏡<br>ვერ მოიძებნა</div></td></tr>';
    renderPagination();
    return;
  }

  page.forEach(p => {
    const price = calcPrice(p);
    const roi   = calcROI(p).toFixed(1);
    const tr    = document.createElement('tr');
    if (selectedPlot && selectedPlot.id === p.id) tr.classList.add('selected-row');

    const bCls  = p.status === 'free' ? 'badge-free' : p.status === 'reserved' ? 'badge-reserved' : 'badge-sold';
    const bTxt  = p.status === 'free' ? 'ხელმ.' : p.status === 'reserved' ? 'დაჯავ.' : 'გაყ.';
    const zCls  = 'zone-' + p.zone;

    tr.innerHTML = `
      <td><strong>${p.id}</strong></td>
      <td><span class="zone-pill ${zCls}">${p.zone}</span></td>
      <td>${p.sqm} m²</td>
      <td>${p.zone === 'AH' ? '—' : (p.area + ' m²')}</td>
      <td style="color:#555;font-size:12px">${p.style}</td>
      <td><strong>$${price.toLocaleString()}</strong></td>
      <td style="color:${parseFloat(roi)>10?'#1a7a3f':'#888'};font-weight:600">${roi}%</td>
      <td><span class="badge ${bCls}">${bTxt}</span></td>
      <td style="font-size:11px;color:var(--text-muted);max-width:120px;overflow:hidden;text-overflow:ellipsis">${p.notes || ''}</td>
    `;
    tr.addEventListener('click', () => selectPlot(p));
    tbody.appendChild(tr);
  });

  renderPagination();
}

function renderPagination() {
  const pag   = document.getElementById('pagination');
  const total = Math.ceil(filtered.length / PAGE_SIZE);
  pag.innerHTML = `<span class="page-info">${filtered.length} ჩანაწ.</span>`;
  for (let i = 1; i <= total; i++) {
    const btn = document.createElement('button');
    btn.className = 'page-btn' + (i === currentPage ? ' active' : '');
    btn.textContent = i;
    btn.onclick = () => { currentPage = i; renderTable(); };
    pag.appendChild(btn);
  }
}

function selectPlot(p) {
  selectedPlot = p;
  const price = calcPrice(p);
  renderTable();
  document.getElementById('sel-plot-id').textContent   = p.id;
  document.getElementById('sel-plot-type').textContent = p.style + (p.zone !== 'AH' ? ` | ${p.area} m² ნაკვ.` : ' | Apart Hotel') + (p.notes ? ' | ' + p.notes : '');
  document.getElementById('c-capex').value = price;
  document.getElementById('c-rent').value  = p.daily_rent;
  recalc();
}

function recalc() {
  const capex  = parseFloat(document.getElementById('c-capex').value) || 0;
  const rent   = parseFloat(document.getElementById('c-rent').value)  || 0;
  const occ    = parseFloat(document.getElementById('c-occ').value)   / 100;
  const mgmt   = parseFloat(document.getElementById('c-mgmt').value)  / 100;
  const cRate  = parseFloat(document.getElementById('comm-rate').value) / 100;

  document.getElementById('occ-lbl').textContent      = Math.round(occ * 100) + '%';
  document.getElementById('mgmt-lbl').textContent     = Math.round(mgmt * 100) + '%';
  document.getElementById('comm-rate-lbl').textContent = (cRate * 100) + '%';

  const gross   = rent * 365 * occ;
  const net     = gross * (1 - mgmt) * 0.82;
  const roi     = capex > 0 ? (net / capex * 100) : 0;
  const payback = net > 0 ? (capex / net) : 0;
  const comm    = capex * cRate;

  document.getElementById('r-gross').textContent   = '$' + Math.round(gross).toLocaleString();
  document.getElementById('r-income').textContent  = '$' + Math.round(net).toLocaleString();
  document.getElementById('r-roi').textContent     = roi.toFixed(1) + '%';
  document.getElementById('r-payback').textContent = payback.toFixed(1) + ' წ';
  document.getElementById('comm-value').textContent = '$' + Math.round(comm).toLocaleString();
  document.getElementById('comm-detail').textContent = `${(cRate*100)}% × $${capex.toLocaleString()}`;
}

function setLang(l) {
  document.querySelectorAll('.lang-pill button').forEach(b => {
    b.classList.toggle('active', b.textContent.trim().toLowerCase() === l || (l==='ka' && b.textContent.includes('ქართ')));
  });
}

// SLIDERS
document.getElementById('c-occ').addEventListener('input', recalc);
document.getElementById('c-mgmt').addEventListener('input', recalc);
document.getElementById('comm-rate').addEventListener('input', recalc);
document.getElementById('c-rent').addEventListener('input', recalc);

// INIT
window.addEventListener('DOMContentLoaded', loadData);
</script>
</body>
</html>
"""

# Combine: partial HTML + plots_js (renamed to EMBEDDED_PLOTS) + js_logic
plots_embedded = plots_js.replace('const PLOTS = [', 'const EMBEDDED_PLOTS = [', 1)

full_html = partial + '\n' + plots_embedded + '\n' + js_logic

# Save
out_path = r'C:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\sales_dashboard_v2.html'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(full_html)

print(f'Written: {len(full_html)} chars ({len(full_html)//1024}KB)')
print(f'Path: {out_path}')
