# Data exchanges

## What it is

**Analytics Hub** / **BigQuery sharing** lets you create and manage **data exchanges** and **listings**. Subscribers get zero-copy, read-only access to shared datasets in their project. You govern who can see which listings.

## Demo doc

Use the demo dataset to practice **publishing** a listing (e.g. a subset or view of the demo data) and, in another project or as another user, **subscribing** to it. This demonstrates sharing without copying data.

## Demo material

1. **Open Governance**  
   In BigQuery → **Governance** (or Analytics Hub). Open **Data exchanges** or **Analytics Hub**.

2. **Create an exchange (if needed)**  
   Create a data exchange (e.g. `demo-exchange`) in your organization or project. Set name and description.

3. **Create a listing**  
   Create a listing that exposes the demo dataset (or a view on it). For example:
   - **Listing name**: “BQ Studio demo dataset.”
   - **Dataset**: your project’s `bq_studio_demo` (or a view like “PnL summary” that selects from `pnl_daily`).
   - **Region**: same as dataset.
   Configure access (e.g. which groups can request access). Publish the listing.

4. **Subscribe (second project or user)**  
   From another project (or as a user with subscriber role), open Analytics Hub, find the listing, and **Subscribe**. Confirm the linked dataset appears in the subscriber project and is read-only. Run a query against it (e.g. `SELECT * FROM linked_dataset.pnl_daily LIMIT 10`).

5. **Demo with a view**  
   Optionally share only a **view** over `bq_studio_demo` (e.g. aggregated PnL by strategy) so subscribers see only approved aggregates, not raw tables.

## Demo data used

- Dataset: `bq_studio_demo` (or a view on it).  
- Listing exposes this dataset (or view) for subscription.  
- Subscriber project gets a read-only linked dataset.

## References

- [Introduction to BigQuery sharing](https://cloud.google.com/bigquery/docs/analytics-hub-introduction)  
- [View and subscribe to listings](https://cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings)
