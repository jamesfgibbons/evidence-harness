# Evidence Harness

> **LANE:** Personal agent-operations release  
> **IS:** A public, installable operating harness for evidence-gated AI work  
> **IS NOT:** A general safety guarantee, autonomous deployment system, or copy of a private production stack  
> **FORBIDDEN CROSS-OVERS:** Credentials, private operations, client material, production identifiers, private prompts, and raw traces  
> **SOURCE OF TRUTH:** This repository's tagged releases  
> **GATE:** Every public release requires tests, hygiene checks, provenance review, and James's explicit approval

Evidence Harness is the public form of the personal control layer I use around AI-assisted work in my own stack.

It addresses a recurring class of failures that model selection and prompt refinement do not solve by themselves: irrelevant context, stale authority, wrong-environment action, unbounded mutation, and completion claims without reproducible evidence.

The harness asks six questions:

1. Does this task need the harness at all?
2. Which narrow rules should load?
3. What source is authoritative?
4. What is the actual state now?
5. What action is permitted?
6. What evidence would make completion true?

The operating loop is:

```text
Route → establish authority → sense state → bound action → verify → receipt → improve
```

## What is included

- An installable directory-based skill at [`skills/evidence-harness`](skills/evidence-harness).
- Focused references for routing, authority/action boundaries, and evidence receipts.
- A small receipt helper implemented with the Python standard library.
- A synthetic infrastructure-context mismatch showing a mutation blocked before execution.
- Conformance tests and a public-hygiene check.

## What is not included

- Private product contracts, repository paths, runbooks, incidents, prompts, traces, or operational identifiers.
- Cloud credentials, environment files, secret handling, or production integrations.
- A promise that an AI system is correct, secure, or autonomous.
- Automatic permission to deploy, publish, message, spend money, or mutate external systems.

## Install the skill

Copy the canonical skill directory into an environment that supports directory-based skills:

```text
skills/evidence-harness/
```

The installed folder must retain `SKILL.md`, `agents/`, `references/`, `scripts/`, and `assets/`.

## Run the synthetic proof

From the repository root:

```bash
python3 skills/evidence-harness/scripts/harness_receipt.py \
  --task examples/synthetic-infra-mismatch/task.json \
  --authority examples/synthetic-infra-mismatch/authority.json \
  --observed examples/synthetic-infra-mismatch/observed.json \
  --output /tmp/evidence-harness-receipt.json
```

The expected result is a blocked receipt because the observed project does not match the authoritative project. No infrastructure command is executed.

## Validate the release

```bash
python3 scripts/release_check.py
```

## Maturity

`0.1.0-preview` is the first public version. The private operating pattern has been used in the author's own stack; the public extraction is new and has not yet earned third-party compatibility or outcome claims.

## Related public work

- Constitutional CMS owns formal publishing-governance and conformance doctrine.
- [VIBEnet Adapter for Codex](https://github.com/jamesfgibbons/vibenet-adapter-codex)
  makes authorized agent lifecycle state observable without exposing prompts,
  responses, reasoning, commands, paths, or raw source identifiers.
- VIBEnet owns perceptual and temporal adapters. Evidence Harness is a gate;
  the Codex adapter is a sensor. Either can be used independently.
- Open Demand OS owns public demand-decision skills.
- jamesfgibbons.com explains and indexes releases from the `jamesfgibbons` namespace.

Those systems remain separate authorities. This repository links to them; it does not copy their contracts.

## License

- Code and skill package: Apache License 2.0.
- Editorial documentation: Creative Commons Attribution 4.0 International.

See [`LICENSE`](LICENSE) for code and [`LICENSE-DOCS`](LICENSE-DOCS) for editorial documentation.
