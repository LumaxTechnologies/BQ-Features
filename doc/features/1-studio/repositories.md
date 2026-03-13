# Repositories

## What it is

**Repositories** in BigQuery Studio are Git-backed containers for version-controlled code. They store saved queries, notebooks, and other code assets (Dataform-backed). You can connect a repo to GitHub/GitLab/Bitbucket and use **workspaces** to edit files.

## Demo doc

Create a repository to hold the demo SQL and notebooks so they are versioned and shareable. Use the same project and region as your demo dataset (`bq_studio_demo`).

## Demo material

1. **Create a repository**  
   In BigQuery Studio → **Explorer** → **Repositories** → **Add Repository**.  
   - Repository ID: e.g. `bq-demo-assets`.  
   - Region: same as your demo (e.g. US or EU).  
   Click **Create**.

2. **Add a workspace**  
   Open the new repo → create a workspace (e.g. `main` or `demo-workspace`). You’ll edit files in this workspace.

3. **Add demo SQL as files**  
   Copy or upload the demo SQL from `bq_studio_demos/sql/` (e.g. `01_portfolio_value.sql`) into the workspace so they live in the repo. Example content to paste into a new file in the workspace:
   ```sql
   -- Portfolio market value (demo)
   SELECT p.as_of_date, p.symbol, p.quantity, d.close AS price,
          p.quantity * d.close AS market_value
   FROM `YOUR_PROJECT.bq_studio_demo.portfolio_holdings` p
   JOIN `YOUR_PROJECT.bq_studio_demo.daily_prices` d
     ON p.symbol = d.symbol AND p.as_of_date = d.date
   ORDER BY p.as_of_date, p.symbol;
   ```
   Replace `YOUR_PROJECT` with your project ID.

4. **Link to GitHub (optional)**  
   In the repo **Configuration** tab → **Connect with Git** → add your GitHub repo URL and credentials (see `doc/create-bq-repo-and-link-github.md`). Then commit and push from the workspace.

5. **Share the repo**  
   Use **Open actions** → **Share** to grant teammates **Code Viewer** or **Code Editor** so they can see or edit the demo queries.

## Demo data used

- Queries reference `bq_studio_demo.portfolio_holdings` and `bq_studio_demo.daily_prices`.  
- Same project as the repo.

## References

- [Create and manage repositories](https://cloud.google.com/bigquery/docs/repositories)  
- [Create a BQ repo and link to GitHub](../create-bq-repo-and-link-github.md)
