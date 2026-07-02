# Google Sheets Setup & Maintenance Guide

## Current Published CSV

**Sheet 1 (ახალი კლდის პირი)**:
```
https://docs.google.com/spreadsheets/d/e/2PACX-1vSxarJedqRj46r3G0SpC2hooZ-Mm5t_VhNzDo451AEXe7W6K2HOJgETUAAJZrlOBw/pub?gid=1846532347&single=true&output=csv
```

## Re-publishing After Changes to Structure

If the Google Sheets document is deleted or url changes:
1. Open Google Drive as `greencanyonecovillage@gmail.com`
2. Upload `GreenCanyon_ForGoogleSheets.xlsx`
3. Right-click → Open with → Google Sheets
4. File → Share → Publish to web
5. Select sheet → CSV → Publish
6. Copy URL
7. Update `CFG.sheetsUrl` default in `portal_template.html` (line ~693) and rebuild

## Python Upload (gspread)

Library installed: `gspread 6.2.1`, `google-auth-oauthlib 1.3.1`

To upload programmatically via browser subagent: navigate to drive.google.com (account already logged in), use file upload dialog.

## Status Update Workflow (for sales agents)

1. Open Google Sheets: https://docs.google.com/spreadsheets/
2. Find file "Green Canyon — Sales Inventory"
3. Navigate to sheet tab "ახალი კლდის პირი" or "ახალი ვაკის უბანი"
4. Scroll right to management columns (after the main data)
5. Find the plot ID row
6. Change `status` cell: `free` → `reserved` or `sold`
7. Optionally fill `notes`, `buyer_name`, `sale_date`, `agent`
8. Changes sync to portal within 5 minutes automatically

## CORS Proxy

The portal uses `allorigins.win` proxy for cross-origin CSV fetch:
```javascript
const proxy = 'https://api.allorigins.win/raw?url=' + encodeURIComponent(url);
```
If this proxy goes down, alternative proxies:
- `https://corsproxy.io/?` + url
- `https://api.codetabs.com/v1/proxy?quest=` + url

To update proxy: edit `fetchCSV()` function in `portal_template.html` (line ~904) and rebuild.
