# Policy tags

## What it is

**Policy tags** (Dataplex) provide **column-level security** and **dynamic masking** in BigQuery. You tag columns by sensitivity; IAM policies grant or deny access by tag. Useful for PII and confidential fields.

## Demo doc

Apply policy tags to columns in the demo dataset (e.g. treat a column as “confidential”) and show how IAM controls who can see plain values vs masked or no access. Use a copy of the demo table or a small test table to avoid affecting shared demos.

## Demo material

1. **Create a policy tag taxonomy (Dataplex)**  
   In **Dataplex** or **Governance** → **Policy tags**, create a taxonomy (e.g. `demo_taxonomy`) and a policy tag (e.g. `Confidential`). Note the tag’s resource name for the next step.

2. **Create a table with a tagged column**  
   In the query editor, create a small table in `bq_studio_demo_staging` (or a test dataset) with a column that uses the policy tag:
   ```sql
   CREATE TABLE `YOUR_PROJECT.bq_studio_demo_staging.demo_tagged` (
     id STRING,
     symbol STRING,
     value FLOAT64 OPTIONS (description = "Tagged column")
   );
   -- Then in Console: edit the table schema and add the policy tag to the 'value' column.
   ```
   Or use the Console UI to add the policy tag to an existing column of `bq_studio_demo.transactions` (e.g. a column you treat as sensitive).

3. **Set IAM for the policy tag**  
   Grant **Data Catalog Policy Tag Viewer** (or the role that allows reading the tag) to a test user or group. Deny the same principal **BigQuery Data Viewer** on the tagged column for another principal to show column-level deny. Or use a **masking** policy so unauthorized users see a mask (e.g. NULL or hash).

4. **Query as different identities**  
   Run `SELECT * FROM demo_tagged` (or the tagged table) as a user with access: they see the column. Run as a user without the policy-tag role: they get no rows or masked values depending on configuration. Document the outcome for your demo.

5. **Demo data only**  
   Prefer doing this in `bq_studio_demo_staging` or a clone so the main `bq_studio_demo` tables remain unchanged for other demos.

## Demo data used

- Dataset: `bq_studio_demo_staging` (or test dataset).  
- Table: e.g. `demo_tagged` or a copy of `transactions` with one column tagged.  
- Policy tag taxonomy and tag created in Dataplex.

## References

- [Column-level security](https://cloud.google.com/bigquery/docs/column-level-security)  
- [Best practices for policy tags](https://cloud.google.com/bigquery/docs/best-practices-policy-tags)
