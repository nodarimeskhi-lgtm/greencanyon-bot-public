import json

with open('plots_wix_data.json', 'r', encoding='utf-8') as f:
    plots_data = f.read()

html = f"""<!DOCTYPE html>
<html lang="ka">
<head>
    <meta charset="UTF-8">
    <style>
        :root {{
            --bg-color: #fcfcfc;
            --calc-bg: #ffffff;
            --primary: #5c5a4e;
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
        }}

        body {{
            font-family: 'Venryn Sans Light', 'Venryn Sans', sans-serif;
            font-weight: 300;
            background-color: var(--bg-color);
            color: var(--text-dark);
            margin: 0;
            padding: 40px 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }}

        .calculator-wrapper {{ max-width: 900px; width: 100%; position: relative; }}
        .calculator-container {{
            background: var(--calc-bg);
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            width: 100%;
            display: grid;
            grid-template-columns: 1fr 1fr;
            overflow: hidden;
        }}
        @media (max-width: 768px) {{ .calculator-container {{ grid-template-columns: 1fr; }} }}

        .input-section {{ padding: 40px; border-right: 1px solid var(--border); }}
        .output-section {{ padding: 40px; background: var(--primary); color: white; display: flex; flex-direction: column; }}

        h2 {{ font-weight: 600; font-size: 24px; margin-top: 0; margin-bottom: 24px; color: var(--primary); }}
        .output-section h2 {{ color: var(--accent-sage); margin-bottom: 20px; }}

        .form-group {{ margin-bottom: 20px; }}
        .form-group label {{ display: block; font-size: 14px; font-weight: 600; margin-bottom: 8px; color: var(--text-muted); }}

        select, input[type="number"], input[type="text"] {{
            width: 100%; padding: 12px; border: 1px solid var(--border); border-radius: 6px;
            font-size: 16px; font-family: inherit; color: var(--text-dark); box-sizing: border-box; background: #fff;
        }}
        select:focus, input:focus {{ outline: none; border-color: var(--border-focus); }}

        .toggle-container {{
            display: flex; gap: 10px; margin-bottom: 30px; background: rgba(255,255,255,0.1); padding: 5px; border-radius: 8px;
        }}
        .toggle-btn {{
            flex: 1; padding: 10px; border: none; background: transparent; color: white; cursor: pointer; border-radius: 6px; font-weight: 600; transition: 0.3s;
        }}
        .toggle-btn.active {{ background: var(--accent-green); color: white; }}
        .toggle-btn.promo {{ background: transparent; color: #ffcccc; }}
        .toggle-btn.promo.active {{ background: var(--accent-red); color: white; }}

        .result-item {{ margin-bottom: 15px; padding-bottom: 15px; border-bottom: 1px solid rgba(255, 255, 255, 0.1); }}
        .result-item:last-child {{ border-bottom: none; }}
        .result-label {{ font-size: 14px; opacity: 0.9; margin-bottom: 4px; }}
        .result-value {{ font-size: 24px; font-weight: 600; color: white; }}
        .result-value.highlight {{ color: var(--accent-green); }}

        .payment-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 20px; }}
        .payment-box {{ background: rgba(0,0,0,0.2); padding: 15px; border-radius: 8px; }}
        .payment-box .lbl {{ font-size: 12px; opacity: 0.8; margin-bottom: 5px; display: block; }}
        .payment-box .val {{ font-size: 20px; font-weight: bold; color: var(--accent-sage); }}
        
        .disclaimer {{ font-size: 11px; color: var(--text-muted); margin-top: 20px; }}
    </style>
</head>
<body>

<div class="calculator-wrapper">
    <div class="calculator-container">
        <!-- Input Section -->
        <div class="input-section">
            <h2>პარამეტრები (Parameters)</h2>

            <div class="form-group">
                <label>აირჩიეთ ნაკვეთი (Select Plot)</label>
                <select id="plot-select" onchange="updateCalc()"></select>
            </div>

            <div class="form-group">
                <label>ნაკვეთის ფართობი (Plot Size m²)</label>
                <input type="text" id="plot-size" readonly style="background:#f5f5f5">
            </div>

            <div class="form-group">
                <label>მიწის ფასი 1 მ² (Land Price $)</label>
                <input type="text" id="land-price" readonly style="background:#f5f5f5">
            </div>

            <div class="form-group">
                <label>ვილის სტილი / ფართი (Villa Style)</label>
                <input type="text" id="villa-style" readonly style="background:#f5f5f5">
            </div>

            <div class="form-group">
                <label>მშენებლობის ფასი 1 მ² (Build Cost $)</label>
                <input type="text" id="build-cost" readonly style="background:#f5f5f5">
            </div>

            <div class="disclaimer">
                * მონაცემები ეყრდნობა Green Canyon-ის განახლებულ ფასებს. <br>
                ფასებში შესულია მიწის და სახლის მშენებლობის (სრული რემონტით) ღირებულება.
            </div>
        </div>

        <!-- Output Section -->
        <div class="output-section">
            <h2>საინვესტიციო შედეგი (Investment Result)</h2>

            <div class="toggle-container">
                <button class="toggle-btn active" id="btn-standard" onclick="setOfferType('standard')">Standard Offer</button>
                <button class="toggle-btn promo" id="btn-promo" onclick="setOfferType('promo')">Alternative Offer</button>
            </div>

            <div class="result-item">
                <div class="result-label">საინვესტიციო ღირებულება (CAPEX)</div>
                <div class="result-value" id="capex">$0</div>
            </div>

            <div class="payment-grid">
                <div class="payment-box">
                    <span class="lbl">ჯავშანი (Reservation)</span>
                    <span class="val" id="res-fee">$5,000</span>
                </div>
                <div class="payment-box">
                    <span class="lbl">პირველი შენატანი (10%)</span>
                    <span class="val" id="downpayment">$0</span>
                </div>
                <div class="payment-box">
                    <span class="lbl">პოსტ-ჰენდოვერი (20%)</span>
                    <span class="val" id="post-handover">$0</span>
                </div>
                <div class="payment-box">
                    <span class="lbl">ყოველთვიური (36 თვე)</span>
                    <span class="val" id="monthly" style="color:#fff">$0</span>
                </div>
            </div>

            <div class="result-item" style="border: none; margin-bottom: 0;">
                <div class="result-label">Guaranteed 8% (4% Net Share) Monthly</div>
                <div class="result-value highlight" id="guaranteed-return">$0 / თვეში</div>
            </div>
        </div>
    </div>
</div>

<script>
    const plotsConfig = {plots_data};
    let currentOfferType = 'standard';

    function isPromoAvailable(plot) {{
        return plot.promo_style && plot.promo_style !== "nan" && plot.promo_sqm > 0;
    }}

    function init() {{
        const select = document.getElementById('plot-select');
        plotsConfig.forEach(p => {{
            const opt = document.createElement('option');
            opt.value = p.id;
            opt.textContent = `ნაკვეთი ${{p.id}} (${{p.area}} მ²)`;
            select.appendChild(opt);
        }});
        updateCalc();
    }}

    function setOfferType(type) {{
        currentOfferType = type;
        document.getElementById('btn-standard').classList.remove('active');
        document.getElementById('btn-promo').classList.remove('active');
        
        if (type === 'standard') document.getElementById('btn-standard').classList.add('active');
        else document.getElementById('btn-promo').classList.add('active');

        calcROI();
    }}

    function updateCalc() {{
        const plotId = document.getElementById('plot-select').value;
        const plot = plotsConfig.find(p => p.id === plotId);
        if (!plot) return;

        document.getElementById('plot-size').value = plot.area + ' მ²';
        document.getElementById('land-price').value = '$' + plot.land_price;
        
        // Disable Promo toggle if no promo available
        const promoBtn = document.getElementById('btn-promo');
        if (!isPromoAvailable(plot)) {{
            promoBtn.style.display = 'none';
            if(currentOfferType === 'promo') setOfferType('standard');
        }} else {{
            promoBtn.style.display = 'block';
            promoBtn.textContent = "Promo Offers: " + plot.promo_style;
        }}

        calcROI();
    }}

    function calcROI() {{
        const plotId = document.getElementById('plot-select').value;
        const plot = plotsConfig.find(p => p.id === plotId);
        if(!plot) return;

        let style = plot.style;
        let sqm = plot.sqm;
        let buildCost = plot.build_cost;
        let hasMarkup = true; // Standard offer has 25% markup on installments

        if (currentOfferType === 'promo' && isPromoAvailable(plot)) {{
            style = plot.promo_style;
            sqm = plot.promo_sqm;
            buildCost = plot.promo_build_cost;
            hasMarkup = false; // Promo offer has 0% interest on installments
        }}

        document.getElementById('villa-style').value = `${{style}} (${{sqm}} მ²)`;
        document.getElementById('build-cost').value = '$' + buildCost;

        // Financials
        const landValue = plot.area * plot.land_price;
        const constructionValue = sqm * buildCost;
        const investmentValue = landValue + constructionValue;

        const reservation = 5000;
        let downpayment = (investmentValue * 0.10) - reservation;
        if(downpayment < 0) downpayment = 0;
        const postHandover = investmentValue * 0.20;

        // Monthly Calculation
        let financedAmount = investmentValue;
        if (hasMarkup) {{
            // 25% markup applied to the entire investment amount!
            financedAmount = investmentValue * 1.25;
        }}
        
        const remainingForInstallment = financedAmount - reservation - downpayment - postHandover;
        const monthly = remainingForInstallment / 36;

        const guaranteedNet = investmentValue * 0.04 / 12;

        // Update UI
        document.getElementById('capex').textContent = formatC(investmentValue);
        document.getElementById('res-fee').textContent = formatC(reservation);
        document.getElementById('downpayment').textContent = formatC(downpayment);
        document.getElementById('post-handover').textContent = formatC(postHandover);
        document.getElementById('monthly').textContent = formatC(monthly);
        document.getElementById('guaranteed-return').textContent = formatC(guaranteedNet) + ' / თვეში';
    }}

    function formatC(num) {{
        return '$' + num.toLocaleString('en-US', {{ maximumFractionDigits: 0 }});
    }}

    window.onload = init;
</script>
</body>
</html>
"""

with open(r'05-Projects\Tsalka\6-Sales\6-4-Marketing\roi_calculator_wix.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Generated new roi_calculator_wix.html successfully!")
