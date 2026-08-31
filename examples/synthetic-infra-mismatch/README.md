# Synthetic infrastructure mismatch

> **LANE:** Public synthetic proof  
> **IS:** Invented context-verification example  
> **IS NOT:** A replay of a real provider, project, incident, or command  
> **FORBIDDEN CROSS-OVERS:** Real credentials, domains, identifiers, and traces  
> **SOURCE OF TRUTH:** The fixture files in this directory  
> **GATE:** The requested mutation must remain blocked

The task requests a deployment to the project declared by `authority.json`. The observed context intentionally names a different project, and the task contains no mutation authorization.

Running the receipt helper produces two blocking reasons:

- `mismatch:project`
- `authorization:missing`

The helper records the decision and executes no deployment command.

`expected-receipt.json` is the complete golden output used by the release check.

