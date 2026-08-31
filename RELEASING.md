# Releasing

> **LANE:** Public release procedure  
> **IS:** Candidate sequence for an approved release  
> **IS NOT:** Standing permission to publish  
> **FORBIDDEN CROSS-OVERS:** Skipping provenance, history, founder, website, or LinkedIn gates  
> **SOURCE OF TRUTH:** `RELEASE_APPROVAL.md` and the private publication receipt  
> **GATE:** Stop before repository creation until exact approval is recorded

1. Freeze the reviewed candidate commit.
2. Run `python3 scripts/release_check.py` from a clean checkout.
3. Run the private portfolio publication gate against current tree and full history.
4. Complete `RELEASE_APPROVAL.md` and record James's exact approval.
5. Create the public repository from the reviewed tree.
6. Verify default branch, repository description, topics, licenses, and public files.
7. Tag the exact approved commit as `v0.1.0` and attach the validated skill archive and checksum.
8. Verify the README, skill link, archive, checksum, and synthetic proof from a fresh clone.
9. Publish the separately reviewed jamesfgibbons.com release page.
10. Publish LinkedIn copy only after every canonical link resolves.

Any mismatch stops the sequence. A website or social deadline never overrides the gate.

