# Overview (Preview)

## What it is

The **Overview** page (Preview) is a hub for tutorials, get-started guides, release notes, and role-based content (data admin, engineering, science, analysis). You can filter by task or role to see relevant cards and links.

## Demo doc

Use the Overview to orient new users to BigQuery and point them to the demo. Customize which cards you show and add a short “Demo” section in your internal runbook that links to Overview plus the demo dataset and `bq_studio_demos/` assets.

## Demo material

1. **Open Overview**  
   In BigQuery → **Overview** (Preview). Or open `https://console.cloud.google.com/bigquery/overview`.

2. **Filter by role**  
   Use the filter bar to switch between **Data administration**, **Data engineering**, **Data science**, and **Data analysis**. Note which cards and tutorials appear for each. For the demo, “Data analysis” and “Data engineering” are most relevant.

3. **Try a get-started guide**  
   Click a **Get started** or **Try it** card that runs a query or loads data. If it uses a public dataset, run it once. Then tell users: “For our internal demo, use project X and dataset `bq_studio_demo` and the SQL in `bq_studio_demos/sql/`.”

4. **Link demo to Overview**  
   In your internal doc or wiki, add a section: “BigQuery demo: start at Overview → [link], then open Explorer → `bq_studio_demo` and run the queries in `bq_studio_demos/sql/`.” Optionally add a custom card or bookmark if your org supports it.

5. **Release notes**  
   From Overview, open **Release notes** and skim the latest BigQuery/Studio updates. Note any that affect the demo (e.g. new Gemini features, changes to saved queries). Document in your demo changelog if needed.

## Demo data used

- No direct use of demo tables on the Overview page itself.  
- Overview is the entry point; the demo dataset and `bq_studio_demos/` are used after navigating to Studio and Explorer.

## References

- [Explore BigQuery in the console](https://cloud.google.com/bigquery/docs/bigquery-web-ui)  
- BigQuery release notes (linked from Overview)
