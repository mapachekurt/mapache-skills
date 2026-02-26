# Resource: Authentication & Google Login Patterns

To achieve maximum resiliency for Google logins and other high-security environments, do not rely on standard UI-based automation for every run. Instead, use **Session Persistence**.

## The "Golden Session" Workflow

### 1. Manual Initialization
When a site requires complex 2FA or Google Auth:
```bash
# Open a visible browser window
agent-browser --headed open https://accounts.google.com
# MANUALLY complete login, 2FA, and 1Password entry
agent-browser state save auth.json
```

### 2. Automated Reuse
Your agents should start every task by loading the "Golden Session":
```bash
agent-browser state load auth.json
agent-browser open https://target-site.com
# The agent is now pre-authenticated
```

## 1Password CLI Integration

The 1Password CLI (`op`) acts as the "Secure Memory" for the agent.

### 1. How it Communicates
Unlike the browser extension which clicks things, the CLI is purely text-based. 
- **The Agent** runs: `op item get "Google" --fields password`
- **The CLI** returns the raw text.
- **The Agent** then runs: `agent-browser fill @e1 "the_password"`

> [!IMPORTANT]
> **Windows/Antigravity Environment**: On Windows, the `op` CLI typically communicates with the 1Password Desktop app to handle decryption. If the app isn't running, the CLI will prompt for your Master Password. For "Headless" automation (no user present), we recommend using a **1Password Service Account** token.

## Intelligence: How the Agent "Finds" Login
The `agent-browser` itself isn't "smart"—it's a tool. The **Agent** (the LLM) provides the intelligence:

1.  **Visibility**: The agent runs `agent-browser snapshot -i`.
2.  **Recognition**: It sees `[ref=e1] textbox "Email"`. It realizes this is a login screen.
3.  **Retrieval**: It searches its skills/knowledge for 1Password logic.
4.  **Action**: It retrieves the secret using `op` and fills it using `agent-browser`.

This loop makes it resilient because the agent "decides" what to do based on what it *sees* in the snapshot, rather than following a brittle, hard-coded script.

## Handling Multiple Vaults

Based on your configuration, you have two primary vaults: `Mapache-Secrets` and `Personal`.

### 1. Global vs. Explicit Search
By default, the `op` CLI searches **all available vaults**. 
- If you have only one "Google" item, it will find it regardless of the vault.
- If you have "Google" in both, the CLI will ask for more detail or return multiple results.

### 2. The `--vault` Flag
To ensure the agent always picks the correct credential for business tasks:
```bash
# Explicitly target the Mapache vault
op item get "Google" --vault "Mapache-Secrets" --fields password
```

### 3. Agent Mapping Intelligence
When you give an agent a task like "Deploy the Mapache store," the agent (the brain) will:
1.  **Extract Context**: Identify "Mapache" as the primary keyword.
2.  **Target Vault**: Automatically append `--vault "Mapache-Secrets"` to its 1Password commands.
3.  **Cross-Reference**: If the login fails, it may fallback to searching the "Personal" vault as a secondary step.

## Troubleshooting Vault Access
If an agent can't find an item:
- Run `op vault list` to confirm the vault is active.
- Ensure the item name matches exactly what the agent is searching for.
- Note: The agent can only see vaults that are currently "unlocked" in your 1Password Desktop app.
