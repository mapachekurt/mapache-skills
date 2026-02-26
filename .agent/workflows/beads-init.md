---
description: Initialize Beads execution memory in a new or existing repo
---

# Initialize Beads

Set up Beads (`bd`) as the execution memory layer for a repository.

## Steps

1. **Verify Beads CLI is available**
// turbo
   ```pwsh
   $env:PATH = "C:\Users\Kurt Anderson\AppData\Local\Programs\bd;$env:PATH"; bd version
   ```

2. **Initialize Beads in the repo**
// turbo
   ```bash
   bd init --quiet
   ```

3. **Install git hooks**
// turbo
   ```bash
   bd hooks install
   ```

4. **Add Beads instructions to AGENTS.md**
   - If `AGENTS.md` exists, append the Beads session protocol section
   - If not, create one with:
     - Session Start: `bd prime` → `bd ready`
     - During Work: `bd update <id> --claim`
     - Session End: `bd sync` → `git push`
     - Anti-patterns: never `bd edit`, never skip `bd prime`

5. **Configure .gitattributes for merge driver**
// turbo
   ```bash
   echo ".beads/issues.jsonl merge=beads" >> .gitattributes
   ```

6. **Commit the initialization**
   ```bash
   git add .beads/ .gitattributes AGENTS.md
   git commit -m "feat: initialize Beads execution memory"
   ```

7. **Verify**
// turbo
   ```bash
   bd prime
   ```

## Notes
- Run this once per repo. Beads state lives in `.beads/` and travels with the code.
- For the `mapache-solutions` org, also register the repo with `mapache-beads-hub` for cross-repo hydration.
