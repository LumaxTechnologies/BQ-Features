# Create a BigQuery repository and link it to GitHub

This guide explains how to create a repository in BigQuery Studio and connect it to a GitHub Git repository so you can sync code (queries, notebooks, Dataform assets) between BigQuery and GitHub.

## Prerequisites

- A Google Cloud project with **billing enabled**.
- **BigQuery** and **Dataform** APIs enabled: [Enable the APIs](https://console.cloud.google.com/flows/enableapi?apiid=bigquery.googleapis.com,dataform.googleapis.com).
- IAM role that allows creating repositories and workspaces, for example:
  - **Code Creator** (`roles/dataform.codeCreator`) — create and manage private repositories.
  - **Code Owner** (`roles/dataform.codeOwner`) — create and manage shared repositories.
- A **GitHub** repository (existing or new) that you want to link. The repo must be reachable from the public internet (not behind a firewall that blocks Google Cloud).

---

## 1. Create a repository in BigQuery

1. Open the [BigQuery page](https://console.cloud.google.com/bigquery) in the Google Cloud console.
2. In the left pane, click **Explorer** (expand it if needed).
3. In the Explorer pane, expand your **project**, then click **Repositories**. The Repositories tab opens in the details pane.
4. Click **Add Repository**.
5. In **Create repository**:
   - **Repository ID**: Enter a unique ID (letters, numbers, hyphens, underscores only). Example: `my-bq-studio-repo` or `bq-github-sync`.
   - **Region**: Choose the BigQuery region where the repository and its contents will be stored (e.g. `us-central1`). It does not have to match your BigQuery dataset locations. See [BigQuery Studio locations](https://cloud.google.com/bigquery/docs/locations#bqstudio-loc).
6. Click **Create**.

Your new repository appears under **Explorer → Repositories**. You can open it and create workspaces to add and edit files. To keep those files in sync with GitHub, connect the BigQuery repo to your GitHub repo (next section).

---

## 2. Link the BigQuery repository to GitHub

You can connect via **SSH** or **HTTPS**. GitHub supports both.

- **SSH**: Uses an SSH key; you store the **private** key in Google Cloud Secret Manager and add the **public** key to GitHub.
- **HTTPS**: Uses a GitHub **personal access token (PAT)** stored in Secret Manager.

Recommendation: use **HTTPS** if you want a simpler setup with a token; use **SSH** if you prefer key-based auth.

---

### Option A: Connect with HTTPS (GitHub personal access token)

#### Step 1: Create a GitHub personal access token

1. In GitHub: **Settings → Developer settings → Personal access tokens** ([direct link](https://github.com/settings/tokens)).
2. Create either:
   - **Fine-grained token**: Choose “Fine-grained tokens” → “Generate new token”. Select only the repository you want to link; grant **Contents** read and write. Set an expiration if required.
   - **Classic token**: “Tokens (classic)” → “Generate new token (classic)”. Grant the **repo** scope.
3. Copy the token and store it somewhere safe; you will paste it into Secret Manager. If your org uses SAML SSO, [authorize the token for SSO](https://docs.github.com/en/enterprise-cloud@latest/authentication/authenticating-with-saml-single-sign-on/authorizing-a-personal-access-token-for-use-with-saml-single-sign-on) for that organization.

#### Step 2: Store the token in Secret Manager

1. In Google Cloud Console, go to [Secret Manager](https://console.cloud.google.com/security/secret-manager).
2. Click **Create secret**.
3. **Name**: e.g. `github-bq-repo-token`.
4. **Secret value**: Paste the GitHub personal access token.
5. Create the secret.

#### Step 3: Grant the Dataform service agent access to the secret

BigQuery repositories use the **Dataform service agent** to access Git. It must be able to read the secret.

1. Open the secret you created in Secret Manager.
2. Go to **Permissions** and **Grant access** (or add a principal).
3. **Principal**:  
   `service-PROJECT_NUMBER@gcp-sa-dataform.iam.gserviceaccount.com`  
   Replace `PROJECT_NUMBER` with your project number (find it in **Home → Dashboard** or **IAM & Admin → Settings**).
4. **Role**: **Secret Manager Secret Accessor** (`roles/secretmanager.secretAccessor`).
5. Save.

#### Step 4: Connect the BigQuery repository to GitHub

1. In [BigQuery](https://console.cloud.google.com/bigquery), go to **Explorer → Repositories** and select the repository you created.
2. Open the **Configuration** tab.
3. Click **Connect with Git**.
4. In **Connect to remote repository**:
   - Select **HTTPS**.
   - **Remote Git repository URL**: Your GitHub repo URL ending in `.git`, e.g.  
     `https://github.com/your-org/your-repo.git`  
     Do **not** include username or password in the URL.
   - **Default remote branch name**: Usually `main` or `master` (your GitHub default branch).
   - **Secret**: Choose the Secret Manager secret that contains the GitHub token.
5. Click **Connect**.

After connecting, you can pull from and push to GitHub from the BigQuery repository’s workspaces (e.g. via the Configuration / Git UI or workspace actions).

---

### Option B: Connect with SSH (GitHub SSH key)

#### Step 1: Generate an SSH key pair

On your machine:

```bash
ssh-keygen -t ed25519 -C "your-email@example.com" -f ~/.ssh/bq_github_key -N ""
```

This creates:

- **Public key**: `~/.ssh/bq_github_key.pub` — you will add this to GitHub.
- **Private key**: `~/.ssh/bq_github_key` — you will put this in Secret Manager.

#### Step 2: Add the public key to GitHub

1. Copy the contents of `~/.ssh/bq_github_key.pub`.
2. In GitHub: **Settings → SSH and GPG keys** ([link](https://github.com/settings/keys)) → **New SSH key**.
3. Give it a title (e.g. “BigQuery Studio”) and paste the public key. Save.

For a **deploy key** (repo-specific): open the GitHub repo → **Settings → Deploy keys** → **Add deploy key**, then paste the public key and allow write access if you need to push.

#### Step 3: Store the private key in Secret Manager

1. In Google Cloud, go to [Secret Manager](https://console.cloud.google.com/security/secret-manager) → **Create secret**.
2. **Name**: e.g. `github-ssh-private-key`.
3. **Secret value**: Paste the **entire** contents of `~/.ssh/bq_github_key` (including `-----BEGIN ... KEY-----` and `-----END ... KEY-----`).
4. Create the secret.

#### Step 4: Grant the Dataform service agent access to the secret

Same as in Option A, Step 3:

- **Principal**: `service-PROJECT_NUMBER@gcp-sa-dataform.iam.gserviceaccount.com`
- **Role**: **Secret Manager Secret Accessor**

#### Step 5: Get GitHub’s SSH host key

Run:

```bash
ssh-keyscan -t ed25519 github.com
```

Copy one of the lines that looks like:

```
github.com ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOMqqnkVzrm0SdG6UOoqKLsabgH5C9okWi0dh2l9GKJl
```

Use only the part **after** `github.com` (algorithm + base64), e.g.:

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOMqqnkVzrm0SdG6UOoqKLsabgH5C9okWi0dh2l9GKJl
```

You can confirm current keys on [GitHub’s SSH key fingerprints](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints).

#### Step 6: Connect the BigQuery repository to GitHub via SSH

1. In [BigQuery](https://console.cloud.google.com/bigquery), go to **Explorer → Repositories** and select your repository.
2. Open the **Configuration** tab.
3. Click **Connect with Git**.
4. In **Connect to remote repository**:
   - Select **SSH**.
   - **Remote Git repository URL**: SSH URL ending in `.git`, e.g.  
     `git@github.com:your-org/your-repo.git`
   - **Default remote branch name**: e.g. `main` or `master`.
   - **Secret**: The secret that contains the **private** SSH key.
   - **SSH public host key value**: Paste the GitHub host key (algorithm + base64 from Step 5).
5. Click **Connect**.

After this, BigQuery will use the SSH key to pull and push to GitHub; commits are made with your Google Cloud user email.

---

## 3. After connecting

- **Pull**: Get latest from GitHub into your BigQuery repository (e.g. from the repo’s Configuration or workspace Git actions).
- **Push**: Send changes made in BigQuery workspaces to GitHub.
- **Edit connection**: In the repository’s **Configuration** tab, use **Edit Git connection** to change URL, branch, or secret.

One BigQuery repository should map to one remote repo. Use a clear Repository ID (e.g. same name as the GitHub repo) to keep the mapping obvious.

---

## References

- [Create and manage repositories (BigQuery)](https://cloud.google.com/bigquery/docs/repositories)
- [Introduction to repositories (BigQuery)](https://cloud.google.com/bigquery/docs/repository-intro)
- [GitHub: Personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [GitHub: Adding an SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)
