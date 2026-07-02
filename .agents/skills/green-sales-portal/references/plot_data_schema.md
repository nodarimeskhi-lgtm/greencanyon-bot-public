# PLOTS JSON Schema

Each object in the `PLOTS` array (in `index.html`) has this structure:

```json
{
  "id": "LA-1",           // Unique ID — matches Google Sheets id column
  "zone": "LA",           // LA / LB / LC / LD / AH
  "house": 145,           // House area m²
  "plot": 702.4,          // Plot area m²
  "style": "Modern Flat-Roof",  // Barnhouse / A-Frame / Barn_85 / Barn_115 / etc.
  "price": 338038,        // Total price $ (land + house CAPEX)
  "land_price": 120,      // Land $/m²
  "daily_rent": 400,      // Suggested daily rental rate $
  "roi": 9.6,             // ROI % (pessimistic scenario)
  "status": "free",       // free / reserved / sold (overridable from Sheets)
  "notes": "",            // Free text (overridable from Sheets)
  "latlng": [41.5123, 43.7456]  // Map coordinates [lat, lng]
}
```

## Apart Hotel Units

- `AH-SS-01` to `AH-SS-75`: Studio Suite 35m², daily_rent: $160
- `AH-JS-01` to `AH-JS-25`: Junior Suite 50m², daily_rent: $190

## Zone Plot Counts (from Settlement_Optimized_Diversity_Plan.xlsx)
- LA: 48 plots (ახალი კლდის პირი sheet, პირველი ზოლი)
- LC: 48 plots (ახალი კლდის პირი sheet, მეორე ზოლი)  
- LB: 48 plots (ახალი ვაკის უბანი sheet, მესამე ზოლი)
- LD: 48 plots (ახალი ვაკის უბანი sheet, მეოთხე ზოლი)
- AH: 100 units (75 Studio + 25 Junior Suite)
- **Total: 292 objects** (271 in current portal — verify against xlsx)

## Google Sheets CSV Column Mapping

When Sheets CSV is fetched, these columns are merged into PLOTS:

| CSV Column | PLOTS Field | Notes |
|---|---|---|
| `id` | `id` | Match key — must be exact |
| `status` | `status` | Overwrites embedded value |
| `notes` | `notes` | Overwrites embedded value |
| `daily_rent` | `daily_rent` | Only if non-empty float |
| `land_price` | `land_price` | Only if non-empty float |
