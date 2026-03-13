# Settings (Preview)

## What it is

**Settings** (Preview) let you customize BigQuery defaults and UI preferences: default project, location, query options (e.g. bytes billed limit), and other configuration. Settings can be user- or project-scoped.

## Demo doc

Set the demo project and default dataset/location so that new queries and notebooks default to the demo context. Document the recommended settings for anyone running the BQ-Features demo.

## Demo material

1. **Open Settings**  
   In BigQuery → **Settings** (Preview). Or open the settings entry from the navigation menu.

2. **Set default project**  
   Set **Default project** to the project that contains `bq_studio_demo`. New query tabs and notebooks will use this project unless overridden.

3. **Set default location/dataset (if available)**  
   If the UI offers a default dataset or default location, set:
   - **Default dataset**: `bq_studio_demo` (so unqualified table names resolve there).  
   - **Default location**: same region as your demo (e.g. US or EU).  
   Save.

4. **Query options**  
   In Settings or in the query editor **More** menu, check **Query options**. For demo, you may set **Maximum bytes billed** to cap cost (e.g. 1 GB) so accidental large scans are limited. Document the value for your team.

5. **Verify**  
   Open a new **SQL query**. Confirm the project (and dataset, if shown) default to the demo. Run `SELECT * FROM daily_prices LIMIT 5` and confirm it resolves to `bq_studio_demo.daily_prices`. Document: “For the demo, use Settings → default project X, default dataset bq_studio_demo.”

## Demo data used

- Default project: the project that contains `bq_studio_demo`.  
- Default dataset: `bq_studio_demo` (if supported).  
- No schema or data changes; settings only affect defaults.

## References

- [Default configuration and settings](https://cloud.google.com/bigquery/docs/default-configuration#configuration-settings)
