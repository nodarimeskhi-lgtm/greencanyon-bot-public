---
description: Sync Excel inventory to Google Sheets and redeploy Sales Portal to Netlify
---

// turbo-all

## Excel → Google Sheets → Netlify Auto-Sync Workflow

When the user says they've updated `Settlement_Optimized_Diversity_Plan.xlsx` and wants to sync/deploy, follow these steps:

### Step 1: Export from Excel
Run the export script to generate updated Google Sheets file and Portal CSV:

```powershell
python "C:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\export_to_sheets.py"
```

### Step 2: Upload updated file to Google Sheets
Use the browser subagent to:
1. Navigate to https://drive.google.com (logged in as greencanyonecovillage@gmail.com)
2. Find and delete the old "Green Canyon — Sales Inventory" file (or upload new version)
3. Upload `C:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\GreenCanyon_ForGoogleSheets.xlsx`
4. Right-click → Open with Google Sheets
5. File → Share → Publish to web → "ახალი კლდის პირი" sheet → CSV → Publish
6. Copy and save the new CSV URL

### Step 3: Update CSV URL in Portal (if URL changed)
If the published CSV URL changed, update `CFG.sheetsUrl` in `portal_template.html` around line 693:
```javascript
const CFG = {
  sheetsUrl: 'NEW_CSV_URL_HERE',
  ...
}
```

### Step 4: Rebuild index.html
```powershell
python "C:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\build_index.py"
```

### Step 5: Deploy to Netlify
```powershell
Copy-Item "C:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\index.html" "C:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\deploy\index.html" -Force
npx netlify-cli deploy --prod --dir "C:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\deploy" --site "green-canyon-sales-portal" --no-build --message "Inventory update from Excel"
```

### Step 6: Verify
Open https://green-canyon-sales-portal.netlify.app and confirm:
- Plot counts match Excel data
- Sync badge shows "Sheets ✓" after connecting
- Map markers load correctly

## Notes
- Google account: greencanyonecovillage@gmail.com (Netlify CLI already authenticated)
- Current CSV URL: https://docs.google.com/spreadsheets/d/e/2PACX-1vSxarJedqRj46r3G0SpC2hooZ-Mm5t_VhNzDo451AEXe7W6K2HOJgETUAAJZrlOBw/pub?gid=1846532347&single=true&output=csv
- Main portal: https://green-canyon-sales-portal.netlify.app
