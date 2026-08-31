# Resolver

Read only the branch matching the deliverable.

| Target | Load or inspect | Required outcome check |
|---|---|---|
| Ordinary factual answer | Nothing additional | Answer directly |
| Existing code or repository | Project instructions, relevant source, tests | Behavior and targeted tests |
| New UI or visual change | Project design rules and affected states | Loaded, loading, empty, and error states; narrow and wide layouts when applicable |
| Document, presentation, or data artifact | Format-specific rules and source evidence | Rendered artifact plus content validation |
| Infrastructure or database | Identity contract, context verifier, current documentation | Verified target, classified action, explicit authorization for mutation |
| Publication or external communication | Source evidence, disclosure boundary, canonical destination | Claim review, link verification, explicit publication authorization |
| Review or diagnosis | Relevant source and evidence only | Findings supported by inspectable evidence; no inferred repair |

## Routing principles

- Prefer project-local authority over generic patterns.
- Load conditional rules only after the target is known.
- Do not apply constraints from one runtime or artifact type to another.
- A missing relevant route is a resolver defect; an irrelevant loaded route is context pollution.
- When no branch materially improves the task, load nothing.

