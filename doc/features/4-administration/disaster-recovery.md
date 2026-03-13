# Disaster recovery

## What it is

**Managed disaster recovery (DR)** for BigQuery provides backup and restore for critical datasets. You configure DR for a dataset so it can be recovered in a disaster scenario.

## Demo doc

Use the demo dataset as a non-critical example to walk through where DR settings live and what “enable DR” would mean. For production, you’d enable DR on real business datasets.

## Demo material

1. **Open Administration / DR**  
   In BigQuery → **Administration** (or the relevant menu). Find **Disaster recovery** or **Managed DR** (or the dataset-level backup/DR option in your region).

2. **Locate dataset settings**  
   Open the demo dataset `bq_studio_demo` (or `bq_studio_demo_staging`). Check **Dataset details** or **Settings** for any **Backup** or **Disaster recovery** option. Document what’s available (e.g. enable DR, RPO/RTO settings, cross-region replica).

3. **Enable DR for demo (optional)**  
   If the UI allows and you want to demo: enable managed DR for `bq_studio_demo`. Note the region and any secondary region. Confirm the dataset shows as DR-enabled. Explain RPO and recovery process from the docs.

4. **Restore (optional, advanced)**  
   If your org has a restore procedure (e.g. point-in-time or from replica), document it. Do not perform an actual restore on the shared demo unless agreed; instead, describe the steps and point to the official restore guide.

5. **Document**  
   For your team: “Demo dataset DR is [enabled/disabled]. Production datasets should enable DR with RPO X and region Y.” List the official DR and restore docs.

## Demo data used

- Dataset: `bq_studio_demo` (and optionally `bq_studio_demo_staging`).  
- No schema or data changes required; DR is a dataset-level configuration.

## References

- [Managed disaster recovery](https://cloud.google.com/bigquery/docs/managed-disaster-recovery)
