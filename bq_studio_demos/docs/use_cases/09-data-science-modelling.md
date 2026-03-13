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

## No-code / AI alternatives (BI analysts and non-developers)

- **Gemini to generate BigQuery ML:** In the **query editor**, use **Gemini** and describe what you want in natural language, e.g. “Train a linear regression model to predict daily_return from prev_close and close using the table prices_ml_input, and name the model model_returns.” Gemini can generate the `CREATE MODEL` and subsequent `ML.EVALUATE` / `ML.PREDICT` statements; you run them with one click. No need to memorize BigQuery ML syntax.
- **Data canvas for exploration and model steps:** In a **Data canvas**, use a **SQL** node with a Gemini prompt to build the training dataset (e.g. “From daily_prices compute daily returns and lagged close”). Add another SQL node: “Train a linear regression model on this data to predict daily return.” You can then add a **Visualization** node to plot evaluation metrics or predictions. The flow is visual and prompt-based.
- **Notebooks with natural language:** In a **notebook**, use the built-in assist (e.g. Gemini) to generate cells that load data, create a training table, run `CREATE MODEL`, and call `ML.PREDICT`. Run cells step by step; save and share the notebook. For custom Python (e.g. scikit-learn), you can still ask the assist to draft the code and run it in the notebook.

Non-developers can train and evaluate models using BigQuery ML with minimal or no SQL, by relying on Gemini and the data canvas to generate and run the statements.

## Next

- **Use case 10:** Convert this model into an industrialized process (scheduled retrain, scheduled prediction, or API).
