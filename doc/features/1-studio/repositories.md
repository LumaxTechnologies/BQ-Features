# Repositories

## What it is

**Repositories** in BigQuery Studio are Git-backed containers for version-controlled code. They store **saved queries**, **notebooks**, and other Studio code assets (Dataform-backed). You can connect a repo to GitHub/GitLab/Bitbucket and use **workspaces** to edit files.

**What lives in a Studio repo:** Saved queries (SQL), notebooks (Python + SQL), data preparations, and data canvases. These are **versioned** (history in the UI; full Git if the repo is linked to GitHub) and **shared** via IAM on the repo or on the asset (Code Viewer / Code Editor / Code Owner).

### Query editor and saved queries

- **Query editor:** Write and run SQL in the browser. **Untitled** = session-only; **Save** = creates a saved query in a repo. No tracking for untitled; saved queries have version history in the repo.
- **Saved queries:** Named SQL scripts in a repository; appear under **Explorer → Queries**. Share via IAM (Code Viewer / Code Editor / Code Owner). Use for reusable SQL; not for procedural logic (use stored procedures) or scheduled `CALL` (use Dataform).

### Repositories in Studio vs Dataform, and workspaces

BigQuery has two repository concepts; both use **workspaces** (your editable copy of a repo, branch-style):

| | **Repositories in BigQuery Studio** | **Repositories in Dataform** |
|--|-------------------------------------|------------------------------|
| **Where** | BigQuery console → Explorer → Repositories. | Dataform console (e.g. BigQuery → Dataform). |
| **Purpose** | Store **Studio code assets**: saved queries, notebooks, data preparations, data canvases. Version control and sharing for analysts/engineers in the Studio UI. | Store **Dataform pipeline** code: SQLX (tables, views, operations), JavaScript, `workflow_settings.yaml`. Used to **compile** and **run/schedule** workflows. |
| **Scheduling** | Assets in a Studio repo **cannot be scheduled for execution** from the BigQuery repo. To schedule pipeline runs, use a **Dataform** repository and its workflow/release configs. | **Designed for execution:** release configs, workflow configs; trigger runs from Dataform UI or Cloud Scheduler. |
| **Workspaces** | Edit files (queries, notebooks, etc.); commit and push to the repo and optionally to GitHub. | Develop, compile, trigger runs; commit and push. Multiple people can have different workspaces (e.g. feature branches). |

**Summary:** **Studio repositories** = version control and sharing for “everything you see in BigQuery Studio” (queries, notebooks, etc.); no pipeline scheduling from there. **Dataform repositories** = version control and execution for **SQLX pipelines**; you schedule and run from Dataform.

### Notebooks

Notebooks (Colab Enterprise: Python + SQL) are saved in a **repository**. Same versioning and sharing as saved queries (version history in Studio; full Git if repo is linked). Use for exploratory analysis and sharing analyses with the team.

### Tracking, versioning, and sharing (Studio assets)

| Asset | Versioning | Sharing |
|-------|------------|---------|
| **Saved query / notebook** | Version history in repo; full Git if repo linked to GitHub. | IAM on asset or **repository**: **Code Viewer** (view/run), **Code Editor** (edit/run), **Code Owner** (manage). Users need **BigQuery Job User** and **BigQuery Read Session User** to run queries. |

**Best practice:** Save anything reusable as a saved query (or in a Dataform repo); link the repo to GitHub for history and code review.

---

## Create a repository and link to GitHub

This section explains how to create a repository in BigQuery Studio and connect it to a GitHub Git repository so you can sync code (queries, notebooks) between BigQuery and GitHub.

### Prerequisites

- A Google Cloud project with **billing enabled**.
- **BigQuery** and **Dataform** APIs enabled: [Enable the APIs](https://console.cloud.google.com/flows/enableapi?apiid=bigquery.googleapis.com,dataform.googleapis.com).
- IAM role that allows creating repositories and workspaces, e.g. **Code Creator** (`roles/dataform.codeCreator`) or **Code Owner** (`roles/dataform.codeOwner`).
- A **GitHub** repository (existing or new) that you want to link; it must be reachable from the public internet.

### 1. Create a repository in BigQuery

1. Open the [BigQuery page](https://console.cloud.google.com/bigquery) in the Google Cloud console.
2. In the left pane, click **Explorer** (expand it if needed).
3. Expand your **project**, then click **Repositories**. The Repositories tab opens in the details pane.
4. Click **Add Repository**.
5. In **Create repository**:
   - **Repository ID**: A unique ID (letters, numbers, hyphens, underscores only). Example: `my-bq-studio-repo` or `bq-github-sync`.
   - **Region**: BigQuery region where the repository will be stored (e.g. `us-central1`). See [BigQuery Studio locations](https://cloud.google.com/bigquery/docs/locations#bqstudio-loc).
6. Click **Create**.

Your new repository appears under **Explorer → Repositories**. Open it and create workspaces to add and edit files. To sync with GitHub, connect the BigQuery repo to your GitHub repo (below).

### 2. Link the BigQuery repository to GitHub

You can connect via **SSH** or **HTTPS**. **HTTPS** uses a GitHub personal access token (PAT) in Secret Manager; **SSH** uses an SSH key (private key in Secret Manager, public key on GitHub).

#### Option A: Connect with HTTPS (GitHub personal access token)

1. **Create a GitHub personal access token**  
   In GitHub: **Settings → Developer settings → Personal access tokens** ([link](https://github.com/settings/tokens)). Create a **Fine-grained token** (select the repo; grant **Contents** read and write) or a **Classic token** (grant **repo** scope). Copy the token. If your org uses SAML SSO, [authorize the token for SSO](https://docs.github.com/en/enterprise-cloud@latest/authentication/authenticating-with-saml-single-sign-on/authorizing-a-personal-access-token-for-use-with-saml-single-sign-on).

2. **Store the token in Secret Manager**  
   In Google Cloud: [Secret Manager](https://console.cloud.google.com/security/secret-manager) → **Create secret**. Name (e.g. `github-bq-repo-token`), paste the token as **Secret value**, create.

3. **Grant the Dataform service agent access to the secret**  
   Open the secret → **Permissions** → **Grant access**. **Principal**: `service-PROJECT_NUMBER@gcp-sa-dataform.iam.gserviceaccount.com` (replace `PROJECT_NUMBER` with your project number; find it in **Home → Dashboard** or **IAM & Admin → Settings**). **Role**: **Secret Manager Secret Accessor** (`roles/secretmanager.secretAccessor`). Save.

4. **Connect the repo to GitHub**  
   In BigQuery → **Explorer → Repositories** → select your repository → **Configuration** tab → **Connect with Git**. Select **HTTPS**. **Remote Git repository URL**: your GitHub repo URL ending in `.git`, e.g. `https://github.com/your-org/your-repo.git` (do not include username or password). **Default remote branch name**: e.g. `main` or `master`. **Secret**: choose the Secret Manager secret that contains the token. Click **Connect**.

#### Option B: Connect with SSH (GitHub SSH key)

1. **Generate an SSH key pair**  
   On your machine: `ssh-keygen -t ed25519 -C "your-email@example.com" -f ~/.ssh/bq_github_key -N ""`. This creates a **public** key (`~/.ssh/bq_github_key.pub`) and a **private** key (`~/.ssh/bq_github_key`).

2. **Add the public key to GitHub**  
   Copy the contents of `~/.ssh/bq_github_key.pub`. In GitHub: **Settings → SSH and GPG keys** ([link](https://github.com/settings/keys)) → **New SSH key**; paste the key. For a **deploy key** (repo-specific): repo → **Settings → Deploy keys** → **Add deploy key**; allow write if you need to push.

3. **Store the private key in Secret Manager**  
   In Google Cloud: [Secret Manager](https://console.cloud.google.com/security/secret-manager) → **Create secret**. Name (e.g. `github-ssh-private-key`). **Secret value**: paste the **entire** contents of `~/.ssh/bq_github_key` (including `-----BEGIN ... KEY-----` and `-----END ... KEY-----`). Create.

4. **Grant the Dataform service agent access to the secret**  
   Same as Option A step 3: principal `service-PROJECT_NUMBER@gcp-sa-dataform.iam.gserviceaccount.com`, role **Secret Manager Secret Accessor**.

5. **Get GitHub’s SSH host key**  
   Run `ssh-keyscan -t ed25519 github.com` and copy one line; use only the part **after** `github.com` (algorithm + base64). See [GitHub’s SSH key fingerprints](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints) to confirm.

6. **Connect the repo via SSH**  
   In BigQuery → **Explorer → Repositories** → your repo → **Configuration** → **Connect with Git**. Select **SSH**. **Remote Git repository URL**: e.g. `git@github.com:your-org/your-repo.git`. **Default remote branch name**: e.g. `main`. **Secret**: the secret with the **private** SSH key. **SSH public host key value**: paste the GitHub host key (algorithm + base64). Click **Connect**.

### 3. After connecting

- **Pull**: Get latest from GitHub into your BigQuery repository (Configuration or workspace Git actions).
- **Push**: Send changes made in BigQuery workspaces to GitHub.
- **Edit connection**: In the repository’s **Configuration** tab, use **Edit Git connection** to change URL, branch, or secret.

One BigQuery repository maps to one remote repo. Use a clear Repository ID (e.g. same name as the GitHub repo) to keep the mapping obvious.

---

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
   In the repo **Configuration** tab → **Connect with Git** → add your GitHub repo URL and credentials (see **Create a repository and link to GitHub** above: HTTPS with a token or SSH with a key). Then commit and push from the workspace.

5. **Share the repo**  
   Use **Open actions** → **Share** to grant teammates **Code Viewer** or **Code Editor** so they can see or edit the demo queries.

## Demo data used

- Queries reference `bq_studio_demo.portfolio_holdings` and `bq_studio_demo.daily_prices`.  
- Same project as the repo.

## References

- [Create and manage repositories](https://cloud.google.com/bigquery/docs/repositories)
- [Introduction to repositories](https://cloud.google.com/bigquery/docs/repository-intro)
- [Introduction to saved queries](https://cloud.google.com/bigquery/docs/saved-queries-introduction)
- [Share saved queries](https://cloud.google.com/bigquery/docs/work-with-saved-queries#share_saved_query)
- [GitHub: Personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [GitHub: Adding an SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)
