---
name: gcp-secrets
description: Specialized skill for gcp secrets.
license: MIT
---

# GCP Secrets Manager

This skill provides a standardized way to manage project secrets (API keys, credentials, tokens) using Google Secret Manager (GSM). It ensures that sensitive information is never stored in code or shared in plain text.

## Features
- **Secure Storage**: Store API keys and credentials in GSM.
- **Easy Retrieval**: Fetch secrets by name for use in scripts and agents.
- **Rube Integration**: Leverages Rube's `googlesuper` toolkit for remote management.
- **Fallback**: Automatically falls back to local `gcloud` if Rube is unavailable.

## Usage

### Listing Secrets
```bash
python skills/gcp-secrets/scripts/manage_secrets.py list
```

### Storing a Secret
```bash
python skills/gcp-secrets/scripts/manage_secrets.py set --name "MY_API_KEY" --value "sk-..."
```

### Retrieving a Secret
```bash
python skills/gcp-secrets/scripts/manage_secrets.py get --name "MY_API_KEY"
```

## Security Policy
- **Never Log Secrets**: Operations that retrieve secrets must never output them to logs or standard output unless explicitly requested for a non-logging context.
- **Short-lived Access**: Use service accounts with limited `roles/secretmanager.secretAccessor` permissions.
- **No Plaintext**: Avoid storing secrets in `.env` files if possible; prefer GSM for production.
