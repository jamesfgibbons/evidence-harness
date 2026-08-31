---
name: evidence-harness
description: Apply an evidence-gated operating harness to code, content, visual, and infrastructure deliverables. Use when a task needs selective context loading, authoritative-source checks, action classification, bounded execution, verification, and a completion receipt. Do not use for casual conversation or simple factual answers.
metadata:
  short-description: Govern agent work with evidence and boundaries
---

# Evidence Harness

Use an evidence-gated control pattern around AI-assisted work: load only the rules the task needs, establish which source is authoritative, sense actual state before consequential action, preserve human authority, and require evidence before claiming completion.

This skill does not grant permission to mutate an external system. It does not replace project-local instructions, security controls, or human authorization.

## First gate

Decide whether the request is a deliverable or operational task.

- For casual conversation, translation, or a simple factual answer, load no harness references.
- For code, content, visual, document, data, or infrastructure work, continue.
- For a request that only asks for explanation or diagnosis, inspect and report; do not infer permission to implement or publish.

## Route narrowly

Read [the resolver](references/resolver.md) and select only the branch relevant to the task. Do not load every available reference merely because the harness exists.

Then identify project-local instructions and the source that defines desired state. A repository contract, schema, or user decision outranks generic harness guidance for its own scope. Report material conflicts rather than blending them.

## Declare the operating envelope

Before implementation or verification work, state:

- the target and intended outcome;
- the authoritative source;
- the files, services, or people in scope;
- where ephemeral and durable artifacts may be written;
- the action class: `observe`, `export`, `mutate`, or `destructive`;
- the evidence required to establish success.

Read [authority and action boundaries](references/authority-and-action.md) when the task touches an external system, shared repository, credentials, production data, publication, messaging, money, deletion, or another person's work.

## Sense before acting

When action depends on current state, verify that state directly. Do not treat remembered names, cached instructions, architecture plausibility, or a downstream symptom as current evidence.

If the authoritative source is missing, stale, contradictory, or inaccessible, preserve `unknown` or `blocked`. Never convert source failure into a synthetic zero, green result, or permission to proceed.

## Execute within scope

Make the smallest change that satisfies the outcome. Preserve unrelated user work and avoid widening a diagnostic into an implementation, an implementation into a deployment, or a local artifact into a publication.

Pause immediately before an externally consequential action when the required authorization has not been supplied. An earlier approval for planning or implementation does not automatically authorize publishing, deploying, messaging, purchasing, deleting, or changing visibility.

## Verify and issue a receipt

Read [verification and receipts](references/verification-and-receipts.md) for implementation, publication, or infrastructure work.

A completion claim must identify reproducible evidence. If the named verification did not run or did not pass, report the narrower state actually achieved.

Use `scripts/harness_receipt.py` when a machine-readable receipt improves reviewability. A receipt records the selected references, authority, observed state, action class, decision, verification, limitations, and final status; it does not manufacture proof.

## Improve from demonstrated failures

When an operator identifies a recurring failure:

1. Find the rule or reference that should have prevented it.
2. If the rule existed, correct routing or enforcement.
3. If no rule existed, add the narrowest reusable control supported by the failure.
4. Add a behavioral test when the control can be observed deterministically.

Do not promote one preference or isolated example into a universal rule.

## Completion language

Use exact states such as `drafted`, `verified-local`, `published`, `live-verified`, `blocked`, `deferred`, or `unknown`. Use `published` or `live-verified` only when the same update includes the relevant external evidence.
