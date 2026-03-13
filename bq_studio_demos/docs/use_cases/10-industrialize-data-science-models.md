# Use case 10: Industrialize data science models

## Goal

**Convert** data science models into **industrialized processes**: scheduled retraining, batch prediction jobs, and (optionally) serving or export for downstream systems.

## Context

Models built in use case 9 need to run in production: periodic retraining on fresh data and regular prediction runs (batch or real-time). This use case ties together scheduling (7), monitoring (8), and optional CI/CD.

## Demo resources

- **Model and training table:** From use case 9, e.g. `bq_studio_demo.model_returns` and `bq_studio_demo.prices_ml_input`.
- **Dataform:** Use an **operation** that runs `CREATE OR REPLACE MODEL ... AS SELECT ...` (retrain) or that runs `INSERT INTO ... SELECT * FROM ML.PREDICT(...)` (batch prediction). Schedule the workflow (use case 7).
- **Scheduled query:** For simple retraining or prediction that fits in one DDL/DML statement, use a scheduled query. For `CALL` or multi-step flows, use Dataform.
- **Monitoring:** Use case 8 — monitor the scheduled model jobs and set alerts on failure.

## Steps

### 1. Schedule model retraining

- **Option A — Dataform operation:** Add a `.sqlx` operation that runs:
  ```sql
  CREATE OR REPLACE MODEL `YOUR_PROJECT.bq_studio_demo.model_returns`
  OPTIONS (model_type='LINEAR_REG', input_label_cols=['daily_return']) AS
  SELECT daily_return, prev_close, close
  FROM `YOUR_PROJECT.bq_studio_demo.prices_ml_input`
  WHERE daily_return IS NOT NULL;
  ```
  Schedule the Dataform workflow (e.g. weekly) so the model is retrained on the latest `prices_ml_input` (which itself can be refreshed by earlier ETL steps).

- **Option B — Scheduled query:** If the full `CREATE MODEL` fits in one scheduled query, create a transfer config that runs it (e.g. weekly). Set the destination dataset if needed; the “output” is the model object.

### 2. Schedule batch prediction

- Add a Dataform operation (or scheduled query) that writes predictions to a table:
  ```sql
  INSERT INTO `YOUR_PROJECT.bq_studio_demo.predictions_daily`
  SELECT * FROM ML.PREDICT(MODEL `YOUR_PROJECT.bq_studio_demo.model_returns`,
    (SELECT * FROM `YOUR_PROJECT.bq_studio_demo.prices_ml_input` WHERE date = CURRENT_DATE() - 1));
  ```
  Run this daily after the staging/refined tables (and `prices_ml_input`) are updated. Order operations in Dataform so prediction runs after data refresh and (if desired) after retrain.

### 3. Ensure data freshness

- Ensure `prices_ml_input` (or your training/prediction input table) is populated by the same ETL pipeline you built in use cases 4–7. That way, when the ETL runs on a schedule, the model sees up-to-date data for retraining and prediction.

### 4. Monitor and alert

- Use the Jobs explorer and Cloud Monitoring (use case 8) to confirm retrain and prediction jobs succeed. Set alerts on failure. Document the schedule and the expected tables/models in a runbook.

### 5. Optional: Export or serve

- For downstream systems: export the model (e.g. to GCS or Vertex AI) or expose predictions via a view/API. BigQuery supports model export and Vertex AI integration; document the chosen path for your team.

## What you get

- A scheduled retraining and (optionally) batch prediction pipeline.
- Models and predictions updated automatically from the same ETL and monitoring stack as the rest of the financial pipeline.

## Next

- Revisit use cases 6–8 to ensure the model pipeline is versioned, shared, scheduled, and monitored like the rest of your ETLs.
