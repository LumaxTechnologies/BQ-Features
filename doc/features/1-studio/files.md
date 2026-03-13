# Files

## What it is

The **Files** tab (Preview) in BigQuery Studio lets you organize code assets (saved queries, notebooks) in **user and team folders**. It’s an alternative view to Explorer → Queries / Notebooks.

## Demo doc

After uploading or saving demo queries and the finance notebook, use Files to group them in folders (e.g. “Demo” or “Finance”) for quick access.

## Demo material

1. **Open Files**  
   In BigQuery Studio, open the **Files** tab in the left pane (Preview). You may see default or personal folders.

2. **Create a folder**  
   Create a folder (e.g. `Demo` or `BQ-Features`). Name it so it’s clear these are demo assets.

3. **Organize demo assets**  
   Move or add your saved demo queries (e.g. Portfolio value, Returns and volatility, PnL by strategy) and the finance notebook into this folder. Use the folder’s context menu or drag-and-drop if the UI supports it.

4. **Open from Files**  
   Open a query or notebook from the folder to run or edit it. Confirm it still runs against `bq_studio_demo` and shows expected results.

5. **Team folders (if available)**  
   If your org uses team folders, create or use a shared folder and place demo assets there so the team can find them in one place.

## Demo data used

- Saved queries and notebook that reference `bq_studio_demo` (portfolio_holdings, daily_prices, pnl_daily).  
- No additional demo tables required; this feature is about organization of existing assets.

## References

- [Organize code assets with folders](https://cloud.google.com/bigquery/docs/code-asset-folders)
