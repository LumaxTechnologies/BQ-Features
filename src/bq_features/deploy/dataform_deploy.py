"""Deploy Dataform demo workspace and write .sqlx files into it."""

from __future__ import annotations

from pathlib import Path

import click

# Map BigQuery region to Dataform API location
_REGION_TO_LOCATION = {
    "US": "us-central1",
    "EU": "europe-west2",
}

WORKSPACE_ID = "demo-workspace"
REPO_ID_DEFAULT = "bq-studio-demo"


def _dataform_location(region: str) -> str:
    return _REGION_TO_LOCATION.get(region.upper(), region)


def deploy_dataform_workspace(
    project_id: str,
    region: str,
    output_dir: Path,
) -> bool:
    """Create demo-workspace in Dataform (if not exists) and deploy .sqlx files from output_dir/dataform.

    Uses the first existing repository in the project/location, or creates one named REPO_ID_DEFAULT.
    Returns True if deploy succeeded, False if skipped (no Dataform API or no repo possible).
    """
    try:
        from google.cloud.dataform_v1beta1 import DataformClient
        from google.cloud.dataform_v1beta1.types import (
            CreateRepositoryRequest,
            CreateWorkspaceRequest,
            Repository,
            WriteFileRequest,
            Workspace,
        )
    except ImportError:
        click.echo("  Dataform deploy skipped: google-cloud-dataform not installed.")
        return False

    location = _dataform_location(region)
    parent = f"projects/{project_id}/locations/{location}"
    dataform_dir = Path(output_dir).resolve() / "dataform"
    operations_dir = dataform_dir / "definitions" / "operations"
    if not operations_dir.is_dir():
        click.echo("  Dataform deploy skipped: no dataform/definitions/operations/.")
        return False

    sqlx_files = sorted(operations_dir.glob("*.sqlx"))
    if not sqlx_files:
        click.echo("  Dataform deploy skipped: no .sqlx files in dataform/definitions/operations/.")
        return False

    client = DataformClient()
    repo_name = None

    # List repositories; use first one or create
    try:
        repos = list(client.list_repositories(parent=parent))
    except Exception as e:
        click.echo(f"  Dataform deploy skipped: list_repositories failed: {e}")
        return False

    if repos:
        repo_name = repos[0].name
        click.echo(f"  Using Dataform repository: {repo_name}")
    else:
        try:
            repo = client.create_repository(
                request=CreateRepositoryRequest(
                    parent=parent,
                    repository_id=REPO_ID_DEFAULT,
                    repository=Repository(),
                )
            )
            repo_name = repo.name
            click.echo(f"  Created Dataform repository: {repo_name}")
        except Exception as e:
            click.echo(f"  Dataform deploy skipped: no repo and create failed: {e}")
            return False

    # List workspaces; create demo-workspace if not exists
    workspace_name = None
    try:
        workspaces = list(client.list_workspaces(parent=repo_name))
        for w in workspaces:
            if w.name.endswith(f"/workspaces/{WORKSPACE_ID}"):
                workspace_name = w.name
                break
    except Exception as e:
        click.echo(f"  Dataform deploy skipped: list_workspaces failed: {e}")
        return False

    if not workspace_name:
        try:
            workspace = client.create_workspace(
                request=CreateWorkspaceRequest(
                    parent=repo_name,
                    workspace_id=WORKSPACE_ID,
                    workspace=Workspace(),
                )
            )
            workspace_name = workspace.name
            click.echo(f"  Created Dataform workspace: {workspace_name}")
        except Exception as e:
            click.echo(f"  Dataform deploy skipped: create_workspace failed: {e}")
            return False
    else:
        click.echo(f"  Using existing Dataform workspace: {WORKSPACE_ID}")

    # Write each .sqlx into the workspace
    for path in sqlx_files:
        rel = path.relative_to(operations_dir)
        # path in workspace: definitions/operations/filename.sqlx
        workspace_path = f"definitions/operations/{rel.name}"
        contents = path.read_bytes()
        try:
            client.write_file(
                request=WriteFileRequest(
                    workspace=workspace_name,
                    path=workspace_path,
                    contents=contents,
                )
            )
            click.echo(f"  Deployed to Dataform: {workspace_path}")
        except Exception as e:
            click.echo(f"  Failed to write {workspace_path}: {e}")
            return False

    return True
