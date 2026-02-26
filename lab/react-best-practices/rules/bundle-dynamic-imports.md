---
title: Dynamic Imports for Heavy Components
impact: CRITICAL
impactDescription: directly affects TTI and LCP
tags: bundle, dynamic-import, code-splitting, react-lazy
---

## Dynamic Imports for Heavy Components

Use dynamic imports (`React.lazy` for SPAs or `next/dynamic` for Next.js) to lazy-load large components not needed on initial render.

**Incorrect (heavy component bundles with main chunk):**

```tsx
import { HeavyEditor } from './heavy-editor'

function ContentPanel({ data }: { data: string }) {
  return <HeavyEditor value={data} />
}
```

**Correct (loads on demand):**

```tsx
import React, { Suspense } from 'react'

const HeavyEditor = React.lazy(() => import('./heavy-editor'))

function ContentPanel({ data }: { data: string }) {
  return (
    <Suspense fallback={<p>Loading editor...</p>}>
      <HeavyEditor value={data} />
    </Suspense>
  )
}
```

*Note: In Next.js, use `next/dynamic` with `{ ssr: false }` for client-only heavy components.*
