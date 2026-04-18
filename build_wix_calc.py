import json
import os

app_dir = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing"
base_dir = r"c:\Users\Nodar\2026 antigraviti"

# Load data
with open(os.path.join(base_dir, 'plots_data_2026.json'), 'r', encoding='utf-8') as f:
    standard_data = json.load(f)

with open(os.path.join(base_dir, 'alt_plots_data_2026.json'), 'r', encoding='utf-8') as f:
    alt_data = json.load(f)

# Convert to dictionary keyed by ID for O(1) access
plots_dict = {}
for p in standard_data:
    plots_dict[p['id']] = {'standard': p, 'alternative': None}
for a in alt_data:
    if a['id'] in plots_dict:
        plots_dict[a['id']]['alternative'] = a

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
    <title>Green Canyon Calculator</title>
    <style>
        :root {
            --bg-color: #f4f3ef;
            --calc-bg: #ffffff;
            --primary: #5c5a4e;
            --primary-hover: #4a483e;
            --secondary: #6e7160;
            --accent-green: #8db290;
            --accent-sage: #a1b5a9;
            --accent-red: #a24035;
            --text-dark: #333333;
            --text-muted: #6e7160;
            --border: #e0e0e0;
            --border-focus: #8db290;
            --radius: 12px;
            --shadow: 0 10px 30px rgba(0, 0, 0, 0.06);
        }

        body {
            font-family: -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--calc-bg);
            color: var(--text-dark);
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            min-height: 100vh;
        }

        .calc-wrapper {
            max-width: 800px;
            width: 100%;
            background: var(--calc-bg);
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            overflow: hidden;
            border: 1px solid var(--border);
            position: relative;
        }

        .header {
            background: var(--primary);
            color: white;
            padding: 20px;
            text-align: center;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .header h1 {
            margin: 0;
            font-size: 20px;
            font-weight: 600;
            color: var(--accent-sage);
        }

        .langs {
            display: flex;
            gap: 5px;
        }

        .lang-btn {
            background: none;
            border: 1px solid rgba(255,255,255,0.3);
            color: white;
            padding: 5px 10px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            transition: 0.2s;
        }

        .lang-btn.active, .lang-btn:hover {
            background: var(--accent-green);
            border-color: var(--accent-green);
        }

        .main-content {
            padding: 30px;
            display: grid;
            grid-template-columns: 1fr;
            gap: 30px;
        }

        /* TABS */
        .tabs {
            display: flex;
            background: #f0f0f0;
            border-radius: 8px;
            padding: 4px;
            margin-bottom: 20px;
        }

        .tab {
            flex: 1;
            padding: 12px;
            text-align: center;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            font-size: 14px;
            transition: 0.3s;
            color: var(--text-muted);
        }

        .tab.active {
            background: var(--accent-green);
            color: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .tab.disabled {
            opacity: 0.4;
            cursor: not-allowed;
        }

        /* DATA GRID */
        .data-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }

        @media(max-width: 600px) {
            .data-grid { grid-template-columns: 1fr; }
        }

        .data-card {
            background: #f9f9f9;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid var(--border);
        }

        .data-card h3 {
            margin-top: 0;
            font-size: 16px;
            color: var(--primary);
            border-bottom: 2px solid var(--accent-sage);
            padding-bottom: 10px;
            margin-bottom: 15px;
        }

        .row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 12px;
            border-bottom: 1px dashed rgba(0,0,0,0.05);
            padding-bottom: 5px;
        }

        .row:last-child {
            border-bottom: none;
            margin-bottom: 0;
        }

        .label {
            font-size: 13px;
            color: var(--text-muted);
            font-weight: 500;
        }

        .value {
            font-size: 14px;
            font-weight: 700;
            color: var(--text-dark);
        }

        .highlight-value {
            color: var(--accent-green);
            font-size: 16px;
        }

        /* PLOT SELECTOR */
        .selector {
            margin-bottom: 25px;
        }
        
        .selector label {
            display: block;
            font-size: 14px;
            font-weight: 600;
            color: var(--primary);
            margin-bottom: 8px;
        }

        .selector select {
            width: 100%;
            padding: 12px;
            border-radius: 6px;
            border: 1px solid var(--border);
            font-size: 16px;
            color: var(--text-dark);
            outline: none;
        }
        
        .selector select:focus {
            border-color: var(--accent-green);
            box-shadow: 0 0 0 2px rgba(141, 178, 144, 0.2);
        }

        .promo-card {
            background: rgba(162, 64, 53, 0.05);
            border: 1px solid var(--accent-red);
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
        }

        .promo-card.hidden {
            display: none;
        }

        .promo-card h3 {
            color: var(--accent-red);
            margin-top: 0;
            font-size: 16px;
        }
        
        .promo-card .value {
            color: var(--accent-red);
        }
        
        .no-alt-msg {
            display: none;
            text-align: center;
            padding: 40px;
            color: var(--text-muted);
            font-size: 14px;
            background: #f9f9f9;
            border-radius: 8px;
            border: 1px dashed var(--border);
        }
    </style>
</head>
<body>

<div class="calc-wrapper">
    <div class="header">
        <h1 data-i18n="title">Detailed ROI Calculator</h1>
        <div class="langs">
            <button class="lang-btn active" onclick="setLang('ka')">KA</button>
            <button class="lang-btn" onclick="setLang('en')">EN</button>
            <button class="lang-btn" onclick="setLang('ru')">RU</button>
        </div>
    </div>

    <div class="main-content">
        
        <div class="selector">
            <label data-i18n="select_plot">Select Plot</label>
            <select id="plotSelect" onchange="render()"></select>
        </div>

        <div class="tabs">
            <div class="tab active" id="tabStandard" onclick="setTab('standard')" data-i18n="tab_standard">Standard Solution</div>
            <div class="tab" id="tabAlternative" onclick="setTab('alternative')" data-i18n="tab_alternative">Alternative / Promo</div>
        </div>
        
        <div id="no-alt-msg" class="no-alt-msg" data-i18n="no_alternative">
            No alternative offer is available for this plot.
        </div>

        <div class="data-grid" id="data-grid">
            <!-- Property Details -->
            <div class="data-card">
                <h3 data-i18n="sec_property">Property Details</h3>
                <div class="row">
                    <span class="label" data-i18n="house_style">House Style</span>
                    <span class="value" id="val_house_style">-</span>
                </div>
                <div class="row">
                    <span class="label" data-i18n="land_area">Plot Area (m²)</span>
                    <span class="value" id="val_land_area">-</span>
                </div>
                <div class="row">
                    <span class="label" data-i18n="house_area">House Area (m²)</span>
                    <span class="value" id="val_house_area">-</span>
                </div>
                <div class="row">
                    <span class="label" data-i18n="total_investment">Total Investment</span>
                    <span class="value highlight-value" id="val_total_investment">-</span>
                </div>
            </div>

            <!-- Payment Plan -->
            <div class="data-card">
                <h3 data-i18n="sec_payment">Payment Plan</h3>
                <div class="row">
                    <span class="label" data-i18n="reservation">Reservation / Down</span>
                    <span class="value" id="val_reservation">-</span>
                </div>
                <div class="row">
                    <span class="label" data-i18n="downpayment">1st Installment (10%)</span>
                    <span class="value" id="val_downpayment">-</span>
                </div>
                <div class="row" id="row_monthly">
                    <span class="label" data-i18n="monthly">Monthly (36 mos)</span>
                    <span class="value" id="val_monthly">-</span>
                </div>
                <div class="row" id="row_post">
                    <span class="label" data-i18n="post_handover">Post-Handover (20%)</span>
                    <span class="value" id="val_post">-</span>
                </div>
            </div>
            
            <!-- Rental & ROI -->
            <div class="data-card" style="grid-column: 1 / -1;">
                <h3 data-i18n="sec_returns">Expected Returns</h3>
                <div class="data-grid" style="gap:20px; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));">
                    <div class="row" id="row_rent">
                        <span class="label" data-i18n="daily_rent">Daily Rent Value</span>
                        <span class="value" id="val_daily_rent">-</span>
                    </div>
                    <div class="row">
                        <span class="label" data-i18n="roi">Projected ROI (%)</span>
                        <span class="value highlight-value" id="val_roi">-</span>
                    </div>
                    <div class="row">
                        <span class="label" data-i18n="payback">Payback Period (Years)</span>
                        <span class="value" id="val_payback">-</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Special Promo Section -->
        <div class="promo-card hidden" id="promo-card">
            <h3 data-i18n="sec_promo">Special Promotional Offer</h3>
            <div class="row" style="border:none;">
                <span class="label" data-i18n="promo_8">8% Guaranteed Return (2 Years)</span>
                <span class="value highlight-value" id="val_promo">-</span>
            </div>
        </div>

    </div>
</div>

<script>
    const DATA = __DATA_PAYLOAD__;
    
    const DICT = {
        ka: {
            title: "საინვესტიციო კალკულატორი",
            select_plot: "აირჩიეთ ნაკვეთი (Plot Code)",
            tab_standard: "სტანდარტული პროექტი",
            tab_alternative: "ალტერნატიული / სააქციო",
            sec_property: "ობიექტის მონაცემები",
            house_style: "სახლის სტილი",
            land_area: "მიწის ფართობი (მ²)",
            house_area: "სახლის ფართი (მ²)",
            total_investment: "საინვესტიციო ღირებულება",
            sec_payment: "გადახდის გრაფიკი",
            reservation: "ბეი - რეზერვი",
            downpayment: "პირველი შენატანი (10%)",
            monthly: "ყოველთვიური (36 თვე)",
            post_handover: "პოსტ-ჰენდოვერი (20%)",
            sec_returns: "მოსალოდნელი ამონაგები და ROI",
            daily_rent: "დღიური ქირის ფასი",
            roi: "Rental ROI (პესიმისტური)",
            payback: "უკუგების პერიოდი (წელი)",
            sec_promo: "სააქციო შეთავაზება",
            promo_8: "8% გარანტირებული უკუგება (2 წელი)",
            no_alternative: "ამ ნაკვეთისთვის ალტერნატიული პროექტი არ არის ხელმისაწვდომი."
        },
        en: {
            title: "Investment ROI Calculator",
            select_plot: "Select Plot Code",
            tab_standard: "Standard Solution",
            tab_alternative: "Alternative / Promo",
            sec_property: "Property Details",
            house_style: "House Style",
            land_area: "Plot Area (m²)",
            house_area: "House Area (m²)",
            total_investment: "Total Investment",
            sec_payment: "Payment Plan",
            reservation: "Reservation Fee",
            downpayment: "First Installment (10%)",
            monthly: "Monthly Installment (36 mos)",
            post_handover: "Post-Handover (20%)",
            sec_returns: "Expected Returns",
            daily_rent: "Daily Rent Value",
            roi: "Rental ROI (Pessimistic)",
            payback: "Payback Period (Years)",
            sec_promo: "Special Promotional Offer",
            promo_8: "8% Guaranteed Return (2 Years)",
            no_alternative: "Alternative project is not available for this plot."
        },
        ru: {
            title: "Инвестиционный Калькулятор",
            select_plot: "Выберите Участок",
            tab_standard: "Стандартный Проект",
            tab_alternative: "Альтернатива / Акция",
            sec_property: "Детали Объекта",
            house_style: "Тип Дома",
            land_area: "Площадь Участка (м²)",
            house_area: "Площадь Дома (м²)",
            total_investment: "Инвестиционная Стоимость",
            sec_payment: "План Оплаты",
            reservation: "Бронь / Резерв",
            downpayment: "Первый Взнос (10%)",
            monthly: "Ежемесячно (36 мес)",
            post_handover: "Пост-сдача (20%)",
            sec_returns: "Ожидаемая Доходность",
            daily_rent: "Суточная Аренда",
            roi: "Rental ROI (Пессимистичный)",
            payback: "Срок Окупаемости (Лет)",
            sec_promo: "Специальное Предложение",
            promo_8: "8% Гарантированный Доход (2 Года)",
            no_alternative: "Альтернативный проект недоступен для этого участка."
        }
    };

    let currentLang = 'ka';
    let currentPlotId = '';
    let currentTab = 'standard';
    
    function fmtC(val) {
        if (!val) return '$0';
        return '$' + Math.round(val).toLocaleString();
    }
    
    function init() {
        const urlParams = new URLSearchParams(window.location.search);
        let urlPlot = urlParams.get('plot');
        
        const sel = document.getElementById('plotSelect');
        const ids = Object.keys(DATA).sort();
        
        ids.forEach(id => {
            const opt = document.createElement('option');
            opt.value = id;
            opt.textContent = id;
            sel.appendChild(opt);
        });
        
        if (urlPlot && ids.includes(urlPlot)) {
            currentPlotId = urlPlot;
            sel.value = urlPlot;
        } else {
            currentPlotId = ids[0];
            sel.value = currentPlotId;
        }
        
        setLang('ka'); // Render handles population
    }
    
    function setLang(lang) {
        currentLang = lang;
        document.querySelectorAll('.lang-btn').forEach(b => {
           b.classList.toggle('active', b.innerText.toLowerCase() === lang);
        });
        
        document.querySelectorAll('[data-i18n]').forEach(el => {
           const key = el.getAttribute('data-i18n');
           if(DICT[lang][key]) el.textContent = DICT[lang][key];
        });
        
        render();
    }
    
    function setTab(tab) {
        const plotData = DATA[currentPlotId];
        if (tab === 'alternative' && !plotData.alternative) return; // Prevent selection
        currentTab = tab;
        document.getElementById('tabStandard').classList.toggle('active', tab === 'standard');
        document.getElementById('tabAlternative').classList.toggle('active', tab === 'alternative');
        render();
    }
    
    function render() {
        currentPlotId = document.getElementById('plotSelect').value;
        const plotData = DATA[currentPlotId];
        
        // Check Alt Availability
        const tabAlt = document.getElementById('tabAlternative');
        if (!plotData.alternative) {
            tabAlt.classList.add('disabled');
            if (currentTab === 'alternative') currentTab = 'standard'; // Fallback
            document.getElementById('tabStandard').classList.add('active');
            tabAlt.classList.remove('active');
        } else {
            tabAlt.classList.remove('disabled');
        }
        
        const d = plotData[currentTab];
        
        if (!d) { // fallback
           document.getElementById('no-alt-msg').style.display = 'block';
           document.getElementById('data-grid').style.display = 'none';
           document.getElementById('promo-card').style.display = 'none';
           return;
        } else {
           document.getElementById('no-alt-msg').style.display = 'none';
           document.getElementById('data-grid').style.display = 'grid';
        }
        
        // Population
        document.getElementById('val_house_style').textContent = d.house_style || '-';
        document.getElementById('val_land_area').textContent = d.land_area || '-';
        document.getElementById('val_house_area').textContent = d.house_area || '-';
        document.getElementById('val_total_investment').textContent = fmtC(d.total_investment);
        
        document.getElementById('val_reservation').textContent = fmtC(d.financial.reservation);
        document.getElementById('val_downpayment').textContent = fmtC(d.financial.downpayment_10);
        
        const mo = d.financial.monthly_36;
        const post = d.financial.post_handover_20;
        
        if (mo > 0) {
            document.getElementById('row_monthly').style.display = 'flex';
            document.getElementById('val_monthly').textContent = fmtC(mo);
        } else {
            document.getElementById('row_monthly').style.display = 'none';
        }
        
        if (post > 0) {
            document.getElementById('row_post').style.display = 'flex';
            document.getElementById('val_post').textContent = fmtC(post);
        } else {
            document.getElementById('row_post').style.display = 'none';
        }
        
        // Returns
        const dr = d.financial.daily_rent;
        if(dr > 0) {
             document.getElementById('row_rent').style.display = 'flex';
             document.getElementById('val_daily_rent').textContent = fmtC(dr);
        } else {
             document.getElementById('row_rent').style.display = 'none';
        }
        
        document.getElementById('val_roi').textContent = d.financial.roi_percent ? (d.financial.roi_percent).toFixed(1) + '%' : '-';
        document.getElementById('val_payback').textContent = d.financial.payback_years ? (d.financial.payback_years).toFixed(1) : '-';
        
        // Promo
        const p8 = d.financial.promo_8_percent;
        if (p8 > 0) {
            document.getElementById('promo-card').style.display = 'block';
            document.getElementById('val_promo').textContent = fmtC(p8);
        } else {
            document.getElementById('promo-card').style.display = 'none';
        }
    }
    
    window.onload = init;
</script>
</body>
</html>
"""

html_out = html_template.replace('__DATA_PAYLOAD__', json.dumps(plots_dict))

with open(os.path.join(app_dir, 'wix_calc.html'), 'w', encoding='utf-8') as f:
    f.write(html_out)

print("wix_calc.html generated!")
