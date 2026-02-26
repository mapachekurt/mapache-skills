---
name: best-practices-reviewer
description: Actionable skill for performing code reviews following established project standards.
version: 1.2.0
license: MIT
---

# Best Practices Reviewer

**Purpose:** Executes project-level code reviews, audits, and health assessments.

> [!NOTE]
> **Passive Context**: Core standards for review priorities, feedback loops, and positive reinforcement have been moved to the project-level `AGENTS.md` and `GEMINI.md` files.

## How to use it
Trigger a review by specifying the target files or directories. This skill uses the benchmarks defined in `AGENTS.md` and `GEMINI.md` to evaluate compliance.

## Review Operations
1. **Critical Audit**: Identify high-priority issues (Security, Performance, Breaking Changes).
2. **Quality Audit**: Review for JSDoc, "Why" comments, and architectural inheritance.
3. **Feedback Generation**: Produce structured reports with clear summaries and actionable strengths/weaknesses.

## How to provide feedback
Follow the format defined in `AGENTS.md`:
- **Summary**: High-level health index.
- **Critical Fixes (High Priority)**: Must-fix list.
- **Improvements (Medium Priority)**: Standard compliance checks.
- **Strengths**: Positive reinforcement.
