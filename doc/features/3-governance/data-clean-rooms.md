# Data clean rooms

## What it is

**Data clean rooms** let multiple parties run analytics on combined data without moving or exposing raw data. Access and analysis rules are set by data owners. Used for marketing, healthcare, finance, and other privacy-sensitive collaboration.

## Demo doc

Data clean rooms require multiple parties and policy setup. With the BQ-Features demo you can **document** the concept and **prepare** demo tables (e.g. `pnl_daily`, `transactions`) as examples of the kind of data that might be contributed to a clean room. A full clean-room demo usually needs two projects or two organizations.

## Demo material

1. **Open Governance**  
   In BigQuery → **Governance**. Find **Data clean rooms** (or the equivalent entry in your console).

2. **Review clean room roles**  
   Understand: **data clean room owner** (manages permissions and membership), **data contributor** (publishes data), **subscriber** (runs queries on combined data). The demo dataset could play the role of “contributor” data (e.g. PnL or transactions).

3. **Create a clean room (if available)**  
   Create a data clean room. Name it e.g. `demo-cleanroom`. As owner, configure analysis rules (what queries or aggregations are allowed). Add yourself or a test principal as a subscriber.

4. **Contribute demo data (conceptual)**  
   As a contributor, “publish” or link the demo dataset (or a view) to the clean room. In a real scenario this would be sensitive data; here use `bq_studio_demo.pnl_daily` or a view as stand-in. Confirm the clean room shows the contributed dataset.

5. **Run an allowed analysis**  
   As a subscriber, run a query or analysis that the clean room allows (e.g. aggregated PnL by strategy, no row-level access). Confirm results are returned without exposing raw rows if that’s how the rules are set.

6. **Document for your team**  
   In a short doc, note: which demo tables were used, who played owner/contributor/subscriber, and what analysis was allowed. Use this to explain clean rooms in training or architecture reviews.

## Demo data used

- Dataset: `bq_studio_demo`.  
- Tables (as contributor data): e.g. `pnl_daily` or a view over `transactions`.  
- No change to the demo schema; clean room governs access and query rules.

## References

- [Data clean rooms](https://cloud.google.com/bigquery/docs/data-clean-rooms)  
- [Share sensitive data with data clean rooms](https://cloud.google.com/bigquery/docs/data-clean-rooms)
