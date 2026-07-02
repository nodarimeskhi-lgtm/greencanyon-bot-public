---
name: green-sales-portal
description: "Green Canyon Sales Portal Manager for Green. Manages the full pipeline: Excel inventory (Settlement_Optimized_Diversity_Plan.xlsx) â†’ Google Sheets sync â†’ Netlify deployment. Use when: (1) updating plot/apartment status (free/reserved/sold), (2) deploying portal changes to Netlify, (3) syncing inventory data between Excel and Google Sheets, (4) rebuilding index.html from template, (5) monitoring portal health, (6) translating UI (ka/en/ru). Trigger phrases: 'portal-áƒ˜', 'sales dashboard', 'áƒ˜áƒœáƒ•áƒ”áƒœáƒ¢áƒáƒ áƒ˜', 'netlify', 'google sheets áƒ¡áƒ˜áƒœáƒ¥', 'áƒœáƒáƒ™áƒ•áƒ”áƒ—áƒ˜áƒ¡ áƒ¡áƒ¢áƒáƒ¢áƒ£áƒ¡áƒ˜', 'deploy', 'rebuild'."
---

# Green Canyon Sales Portal â€” Agent Guide

## System Architecture

```
Settlement_Optimized_Diversity_Plan.xlsx  (source of truth for prices/plots)
        â†“ extract_settlement.py / export_to_sheets.py
portal_template.html + build_index.py
        â†“ python build_index.py
index.html  (90KB, 271 plots embedded)
        â†“ netlify CLI deploy
green-canyon-sales-portal.netlify.app
        â†‘ live sync (every 5 min)
Google Sheets CSV  (status / notes / prices â€” editable by agents)
```

## File Locations

All files: `C:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\`

| File | Purpose |
|---|---|
| `portal_template.html` | HTML template with I18N and all UI logic |
| `build_index.py` | Injects PLOTS JSON â†’ `index.html` |
| `index.html` | Final file for Netlify deploy |
| `deploy/index.html` | Deploy staging copy |
| `Settlement_Optimized_Diversity_Plan.xlsx` | Master inventory (prices, areas, styles) |
| `export_to_sheets.py` | Exports xlsx â†’ `GreenCanyon_ForGoogleSheets.xlsx` + `green_canyon_inventory.csv` |
| `GreenCanyon_ForGoogleSheets.xlsx` | Uploaded to Google Sheets (has status mgmt columns) |
| `verify_fixes.py` | Quick verification of index.html contents |

## Zone Names (Official)
- `LA` â€” áƒ™áƒáƒœáƒ˜áƒáƒœáƒ˜áƒ¡ áƒžáƒ˜áƒ áƒ˜
- `LB` â€” áƒ•áƒ”áƒšáƒ˜áƒ¡ áƒ™áƒ•áƒáƒ áƒ¢áƒáƒšáƒ˜
- `LC` â€” áƒ•áƒ”áƒšáƒ˜áƒ¡ áƒ£áƒ‘áƒáƒœáƒ˜
- `LD` â€” áƒ®áƒ”áƒáƒ‘áƒ˜áƒ¡ áƒ–áƒáƒšáƒ˜
- `AH` â€” Apart Hotel (75Ã— 35mÂ² Studio + 25Ã— 50mÂ² Junior Suite)

## Netlify

- **Main Portal**: `green-canyon-sales-portal` â†’ https://green-canyon-sales-portal.netlify.app
- **effervescent-fox-593acf** â†’ Antigravity "Data Dashboard" (agent analytics) â€” **keep, do not delete**
- **graceful-mooncake-d747f2** â†’ Old portal v1 (backup) â€” **keep as fallback**
- **CLI authenticated** as `greencanyonecovillage@gmail.com`

### Deploy command (run after rebuild):
```bash
Copy-Item "...\index.html" "...\deploy\index.html" -Force
npx netlify-cli deploy --prod --dir "...\deploy" --site "green-canyon-sales-portal" --no-build --message "description"
```

## Google Sheets

- **Account**: greencanyonecovillage@gmail.com
- **File**: "Green Canyon â€” Sales Inventory" (GreenCanyon_ForGoogleSheets.xlsx)
- **Published CSV URL** (Sheet 1 â€” áƒáƒ®áƒáƒšáƒ˜ áƒ™áƒšáƒ“áƒ˜áƒ¡ áƒžáƒ˜áƒ áƒ˜):
  ```
  https://docs.google.com/spreadsheets/d/e/2PACX-1vSxarJedqRj46r3G0SpC2hooZ-Mm5t_VhNzDo451AEXe7W6K2HOJgETUAAJZrlOBw/pub?gid=1846532347&single=true&output=csv
  ```
- **Status values**: `free` / `reserved` / `sold`
- **Editable columns**: `status`, `notes`, `buyer_name`, `sale_date`, `agent`, `daily_rent`, `land_price`
- **Do NOT edit**: `id` column

## Full Sync Workflow (Excel â†’ Sheets â†’ Netlify)

Use `/sync-portal` command or follow `.agent/workflows/sync-portal.md`.

Quick version:
```bash
python export_to_sheets.py          # Step 1: export xlsx
# Step 2: upload GreenCanyon_ForGoogleSheets.xlsx to Google Drive â†’ Sheets â†’ Publish CSV
python build_index.py               # Step 3: rebuild portal
Copy-Item index.html deploy\index.html -Force
npx netlify-cli deploy --prod --dir deploy --site green-canyon-sales-portal --no-build
```

### 1. Rebuild + Deploy (after template changes)
```bash
python build_index.py
# verify: python verify_fixes.py
Copy-Item index.html deploy\index.html -Force
npx netlify-cli deploy --prod --dir deploy --site green-canyon-sales-portal --no-build
```

### 2. Update inventory from Excel
```bash
python export_to_sheets.py
# Then upload GreenCanyon_ForGoogleSheets.xlsx to Google Drive â†’ Open with Sheets â†’ Publish to web â†’ CSV
```

### 3. Change zone names / UI text
Edit `portal_template.html`:
- **Zone dropdown** (line ~310): `<option value="LA">LA â€” ...</option>`
- **Legend** (line ~265): `<div class="leg-item">..LA â€” ...</div>`
- **I18N object** (line ~767): translations for ka/en/ru
Then rebuild.

### 4. Add/modify a plot in inventory
Edit plot data in `build_index.py` INVENTORY section OR regenerate from Excel via `export_to_sheets.py`.

### 5. Monitor portal health
Check: https://green-canyon-sales-portal.netlify.app
- Top-right badge: `áƒ›áƒ–áƒáƒ“áƒáƒ` (local data) or `Sheets âœ“` (Google Sheets connected)
- Stats bar: Total / Available / Reserved / Sold counts

## I18N System

Three languages: `ka` (Georgian), `en` (English), `ru` (Russian).
All translations in `const I18N = { ka: {...}, en: {...}, ru: {...} }` in `portal_template.html` (line ~767).
`setLang(l)` updates ALL UI elements by direct querySelector â€” no data-i18n required.

## Security Notes
- Portal is **public** â€” no password protection
- If sensitive data added â†’ enable Netlify Visitor Authentication
- Google Sheets URL is public once published (by design, for agent access)

## References
- See `references/plot_data_schema.md` for full PLOTS JSON structure
- See `references/google_sheets_setup.md` for Sheets API / CSV publishing guide
