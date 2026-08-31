# Evidence Harness 0.1 Specification

> **LANE:** Personal agent-operations release  
> **IS:** Public specification for the minimum harness contract  
> **IS NOT:** A production policy, vendor certification, or permission grant  
> **FORBIDDEN CROSS-OVERS:** Private implementations and product-specific authority  
> **SOURCE OF TRUTH:** Tagged versions of this specification  
> **GATE:** Conformance describes observable behavior; it does not claim universal safety

## Required behavior

### 1. Relevance gate

The harness distinguishes deliverable work from ordinary conversation. When no special control is needed, it selects no task-specific reference.

### 2. Narrow routing

For a deliverable, the harness selects only guidance relevant to the target and risk. Unrelated rules must not be loaded merely because they exist.

### 3. Authority declaration

Before implementation or operational verification, the harness identifies the authoritative source for desired state. Generic guidance cannot silently override a project-local contract.

### 4. State sensing

When action depends on external or repository state, the harness observes that state before acting. Missing or conflicting state remains explicit.

### 5. Action classification

Every consequential action is classified as one of:

- `observe`: read-only inspection;
- `export`: bounded creation of a reviewable artifact;
- `mutate`: a reversible or controlled state change requiring appropriate authorization;
- `destructive`: deletion, irreversible reset, or broad overwrite requiring explicit target resolution and authorization.

### 6. Evidence contract

Before acting, the harness defines what evidence would establish success. A completion claim requires the named evidence and must preserve limitations.

### 7. Receipt

The harness emits a receipt containing task identity, selected references, authority, observed state, action class, decision, verification, limitations, and status.

### 8. Adaptation

When a failure repeats, the harness determines whether a missing or misrouted rule would have prevented it. Only demonstrated recurring failures justify promotion into shared guidance.

## Status vocabulary

- `drafted`
- `verified-local`
- `published`
- `live-verified`
- `blocked`
- `deferred`
- `unknown`

`unknown` must never be converted into success because a source was unavailable.

## Conformance boundary

An implementation conforms to 0.1 when its observable decisions satisfy the required behavior above and its completion receipts validate against the published schema. Conformance does not establish correctness, security, or fitness for a particular production environment.

