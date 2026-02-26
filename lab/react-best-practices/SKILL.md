---
name: react-best-practices
description: Comprehensive React performance optimization guidelines. Use this skill when writing, reviewing, or refactoring React components and hooks to ensure optimal performance patterns across any hosting environment (Google Cloud, etc.).
license: MIT
---

# React Best Practices

A comprehensive performance optimization guide for modern React applications. Contains 45 rules across 8 categories, prioritized by impact to guide automated refactoring and code generation.

## When to use this skill
Use this skill when we are:
- Writing new React components or hooks.
- Implementing data fetching strategies (client or server-side).
- Reviewing code specifically for performance bottlenecks.
- Refactoring existing React code to improve responsiveness.
- Optimizing bundle size or interaction metrics (INP, LCP).

## How to use it

### General Principles
- **Read the Rules**: Consult the `rules/` directory for detailed "Correct vs Incorrect" examples for each category below.
- **Priority First**: Address "CRITICAL" and "HIGH" impact items (waterfalls and bundle size) before micro-optimizations.
- **Context Matters**: Some rules (like server-side patterns) depend on your specific environment (e.g., SSR vs SPA).

### Core Categories

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Eliminating Waterfalls | CRITICAL | `async-` |
| 2 | Bundle Size Optimization | CRITICAL | `bundle-` |
| 3 | Server-Side Performance | HIGH | `server-` |
| 4 | Client-Side Data Fetching | MEDIUM-HIGH | `client-` |
| 5 | Re-render Optimization | MEDIUM | `rerender-` |
| 6 | Rendering Performance | MEDIUM | `rendering-` |
| 7 | JavaScript Performance | LOW-MEDIUM | `js-` |
| 8 | Advanced Patterns | LOW | `advanced-` |

## Quick Reference

### 1. Eliminating Waterfalls (CRITICAL)
- `async-defer-await`: Move await into branches where actually used.
- `async-parallel`: Use `Promise.all()` for independent operations.
- `async-suspense-boundaries`: Use Suspense to stream or transition content.

### 2. Bundle Size Optimization (CRITICAL)
- `bundle-barrel-imports`: Import directly, avoid heavy barrel files.
- `bundle-dynamic-imports`: Use dynamic imports (`React.lazy` or equivalent) for heavy components.
- `bundle-conditional`: Load modules only when a specific feature is activated.

### 3. Server-Side Performance (HIGH)
- `server-serialization`: Minimize data passed between server and client boundaries.
- `server-parallel-fetching`: Flow data through components to maximize parallel fetches.

### 4. Re-render Optimization (MEDIUM)
- `rerender-memo`: Extract expensive sub-trees into memoized components.
- `rerender-functional-setstate`: Use functional `setState` for stable callbacks.
- `rerender-transitions`: Use `startTransition` for non-urgent state updates.

## Review Checklist
- ✅ Are asynchronous operations parallelized where possible?
- ✅ Are we avoiding massive "barrel" imports that bloat the bundle?
- ✅ Is expensive work memoized or moved outside the render loop?
- ✅ Are state updates prioritized using Transitions if they affect responsiveness?
- ✅ Is the data flow minimized between server/client boundaries?

## How to provide feedback
- Point out specific rules by name (e.g., "This violates `async-parallel`").
- Provide code diffs showing the "Correct" vs "Incorrect" transformation.
- If a rule is inapplicable to the current framework (e.g., Vite vs Next.js), explain why.

## Notes
- Adapted from core industry best practices.
- Version: 1.0.0
- Supports: Antigravity, Gemini CLI, OpenCode, Copilot.
