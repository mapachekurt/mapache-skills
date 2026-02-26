---
description: Standard workflow for transforming a prompt or Stitch project into high-quality React components.
---

# Stitch-to-Code Workflow

This workflow standardizes the path from a raw UI idea to a production-ready React component library using the Stitch suite.

## Step 1: Prompt Enhancement (Loose Workflow)
If starting from a rough idea, use the `enhance-prompt` skill to define the visual language and structure.

1.  **Request**: `@enhance-prompt [your idea here]`
2.  **Output**: A structured specification with Visual Vibe, DESIGN SYSTEM, and Page Structure.
3.  **Action**: Save this output to `next-prompt.md`.

## Step 2: Design System Synthesis (Connected Workflow)
If starting from an existing Stitch project, use the `design-md` skill to extract tokens.

1.  **Request**: `@design-md [Stitch Project URL]`
2.  **Output**: A `DESIGN.md` file in the project root.
3.  **Action**: Review `DESIGN.md` to ensure all brand colors and geometry are captured.

## Step 3: Component Generation
Use the `react-components` skill to generate modular, type-safe code.

1.  **Request**: `@react-components generate components for [next-prompt.md or DESIGN.md]`
2.  **Pipeline**:
    *   AI decomposes the UI into `Sidebar`, `MainHero`, `GridList`, etc.
    *   Creates `src/data/mockData.ts` to keep components clean.
    *   Generates components using Tailwind and TypeScript.
3.  **Action**: Verify components in the `lab/` or `src/components/` directory.

## Step 4: Iteration & Polish
1.  **Review**: Check the generated components against the original design intent.
2.  **Refine**: If styles are missing, update `DESIGN.md` and re-run `@react-components`.
3.  **Sync**: Run `python scripts/sync_skills.py` if new custom skills were added during the process.

---
// turbo-all
## Usage Tip
Run `git add DESIGN.md next-prompt.md` to keep your design source of truth in version control alongside your code.
