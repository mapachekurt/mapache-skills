---
description: Safely clean up merged and redundant git branches.
---

1. Run `git branch --merged` to identify branches that have already been incorporated into the current one.
2. List the merged branches to the user.
3. **Safety Guard**: Ask the user for explicit confirmation to delete these specific branches.
4. If confirmed, run `git branch -d [branch-name]` for each branch.
5. Provide a summary of deleted branches and any that failed to delete.
