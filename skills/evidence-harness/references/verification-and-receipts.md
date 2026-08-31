# Verification and receipts

Use this reference when a task changes an artifact, repository, external system, or public surface.

## Define evidence before action

Name the smallest evidence that would demonstrate the intended outcome. Examples include a focused test, schema validation, rendered mobile and desktop states, an exact response field, a tagged release, or a public URL resolving to the reviewed artifact.

Architecture plausibility, successful command exit, and confident prose are not outcome evidence by themselves.

## Evidence states

- `pass`: the named check ran and met its criterion.
- `fail`: the check ran and did not meet its criterion.
- `unknown`: the source or check was unavailable or inconclusive.
- `not_applicable`: the check does not apply, with a reason.

Never turn `unknown` into `pass` or zero.

## Completion receipt

A useful receipt records:

- task identifier and intended outcome;
- selected references;
- authoritative source and expected state;
- observed state and observation time;
- action class and authorization state;
- decision and blocking reasons;
- verification checks and results;
- created or changed artifacts;
- limitations and unresolved questions;
- final status.

The receipt must distinguish local verification from publication or live verification.

## Claim discipline

- `drafted`: created but not fully verified.
- `verified-local`: required local checks passed.
- `published`: the approved artifact exists at its canonical external location.
- `live-verified`: the intended live behavior was checked after publication or deployment.
- `blocked`: a named unmet condition prevents progress.
- `deferred`: intentionally postponed with an owner or re-entry condition.
- `unknown`: insufficient evidence to classify safely.

