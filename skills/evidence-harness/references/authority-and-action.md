# Authority and action boundaries

Use this reference for shared repositories, infrastructure, databases, credentials, publication, messaging, spending, deletion, or external systems.

## Authority order

Use the narrowest source that legitimately governs the decision:

1. The user's explicit instruction for the current task.
2. Project-local policy, contract, or schema.
3. Verified current external state.
4. Maintained workflow guidance.
5. General knowledge or remembered context.

Do not let a lower source silently override a higher one. When two applicable high-authority sources conflict, stop the affected action and report the conflict.

## Action classes

### `observe`

Read-only inspection that does not intentionally alter the target. Examples include reading source, listing status, inspecting schema, and viewing logs. Some tools still create local caches or audit records; disclose material side effects.

### `export`

Creation of a bounded, reviewable artifact without changing the source system. Examples include a local report, sanitized fixture, or draft release candidate. State where the artifact is written and whether it is ephemeral or durable.

### `mutate`

A state change such as editing shared source, changing configuration, deploying, publishing, messaging, or writing to a database. Confirm that the request authorizes the exact target and consequence immediately before action when risk warrants it.

### `destructive`

Deletion, irreversible reset, broad overwrite, history rewrite, or another action that is difficult to recover. Resolve the exact target with read-only checks, prefer recoverable alternatives, and require explicit authorization.

## Boundaries

- Planning a mutation does not authorize performing it.
- Creating a private draft does not authorize publication.
- Access to credentials does not authorize reading or using them.
- A successful dry run does not prove the live operation succeeded.
- Human approval is part of the control architecture, not a failure of autonomy.

