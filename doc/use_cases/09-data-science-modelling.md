# Use case 9: Data science modelling on data

## Goal

Do **data science modelling** on the (refined) data: train models, evaluate them, and use them for prediction or classification, within the analytics workflow.

## Context

Analysts and data scientists need to build models (e.g. returns prediction, risk classification) on top of the same datasets used for reporting and ETL. BigQuery ML and notebooks in BigQuery Studio support this without leaving the platform.

## Demo resources

- **Dataset:** `bq_studio_demo` (e.g. `daily_prices`, `pnl_daily`, and any refined tables from use case 4).
- **Notebook:** `bq_studio_demos/notebooks/finance_analytics_demo.ipynb` — load data, compute returns, plot; extend with model training.
- **BigQuery ML:** Train models (linear regression, boosted tree, etc.) via SQL in the query editor or in a notebook. [analytics-ml.md](../features/1-studio/analytics-ml.md).
- **Feature docs:** [analytics-ml.md](../features/1-studio/analytics-ml.md), [notebooks.md](../features/1-studio/notebooks.md).

## Steps

### 1. Prepare a training dataset

- From `daily_prices`, build a table with features and a target (e.g. next-day return, or a binary label). Example:
  ```sql
  CREATE OR REPLACE TABLE `YOUR_PROJECT.bq_studio_demo.prices_ml_input` AS
  SELECT symbol, date, close,
         LAG(close) OVER (PARTITION BY symbol ORDER BY date) AS prev_close,
         (close - LAG(close) OVER (PARTITION BY symbol ORDER BY date))
           / NULLIF(LAG(close) OVER (PARTITION BY symbol ORDER BY date), 0) AS daily_return
  FROM `YOUR_PROJECT.bq_studio_demo.daily_prices`;
  ```
- Or use the notebook to build a pandas DataFrame and optionally write it back to a BQ table for ML.

### 2. Train a model with BigQuery ML

- In the query editor (or a notebook with `%%bigquery`), run a `CREATE MODEL` statement. Example (linear regression on next-day return):
  ```sql
  CREATE OR REPLACE MODEL `YOUR_PROJECT.bq_studio_demo.model_returns`
  OPTIONS (model_type='LINEAR_REG', input_label_cols=['daily_return']) AS
  SELECT daily_return, prev_close, close
  FROM `YOUR_PROJECT.bq_studio_demo.prices_ml_input`
  WHERE daily_return IS NOT NULL;
  ```
- Evaluate with `ML.EVALUATE` and predict with `ML.PREDICT`. See [BigQuery ML docs](https://cloud.google.com/bigquery/docs/bigqueryml-intro) and [analytics-ml.md](../features/1-studio/analytics-ml.md).

### 3. Use the notebook for exploration and custom code

- Open the finance demo notebook; add cells that load `prices_ml_input` (or the training table), train a model with BigQuery ML or with a library (e.g. scikit-learn) on a sample, and plot residuals or feature importance. Save the notebook in a repo for versioning (use case 6).

### 4. Document the model and metrics

- Note model name, training table, and evaluation metrics in the repo or in `doc/use_cases/`. This prepares for industrialization (use case 10): scheduled retraining and prediction.

## What you get

- A trained model (e.g. in `bq_studio_demo`) and evaluation results.
- A notebook or saved queries that reproduce the training and prediction steps.
- A clear path to scheduling retraining and batch prediction (use case 10).

## Next

- **Use case 10:** Convert this model into an industrialized process (scheduled retrain, scheduled prediction, or API).
