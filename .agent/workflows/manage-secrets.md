---
description: Interactive workflow to manage GCP Secret Manager secrets.
---

# Secrets Management Workflow

This workflow guides you through storing and listing secrets in Google Secret Manager.

## Step 1: List Existing Secrets

See what's already stored in your project.

// turbo
```bash
python skills/gcp-secrets/scripts/manage_secrets.py list
```

## Step 2: Store/Update a Secret

If you need to store a new API key or update an existing one, run the following command.

> [!TIP]
> If you omit the `--value` argument, the script will prompt you to enter the value securely (it will be hidden as you type).

```bash
python skills/gcp-secrets/scripts/manage_secrets.py set --name "SECRET_NAME"
```

## Step 3: Verify Retrieval (Optional)

You can verify that the secret was stored correctly.

> [!WARNING]
> This will print the secret value to your terminal.

```bash
python skills/gcp-secrets/scripts/manage_secrets.py get --name "SECRET_NAME"
```

## Next Steps
- Use these secrets in your agents by adding them to the `secrets:` section of `adk.yaml`.
- Reference them in Python using `google-cloud-secretmanager` or the provided script.
