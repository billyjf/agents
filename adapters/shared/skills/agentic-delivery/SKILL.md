---
name: agentic-delivery
description: Takes a product change from rough intent through the appropriate Designer, Engineer, QA, and SRE gates. Use for end-to-end feature delivery, production-readiness work, implementation from a rough request, or an explicit request to run the agentic delivery pipeline.
---

# Agentic Delivery

Read `references/DELIVERY.md` before acting. Read only the role references needed for the requested phase. Read `references/SCALABILITY.md` when implementation or production readiness is in scope.

## Route the work

1. Start with Designer when behavior, scope, interfaces, or product decisions are unclear.
2. Start with Engineer when an approved specification and acceptance contracts already exist.
3. Start with QA when implementation is complete and the user requests verification, review, regression testing, or a release gate.
4. Start with SRE when QA has passed and the user requests deployment or production-readiness verification.
5. Run the complete sequence for an end-to-end delivery request.

If the harness supports named custom agents, delegate each phase to the matching `designer`, `engineer`, `qa`, or `sre` agent. Otherwise, execute the phase directly using its role reference. Keep the main thread responsible for requirements, decisions, and the final consolidated handoff.

## Enforce the gates

- Do not run write-heavy phases in parallel against the same checkout.
- Do not advance past unresolved high-impact product, data, security, or interface decisions.
- Require Engineer to map every changed functional/API path to an executable contract test.
- Keep QA independent and read-only. Return failed or missing contracts to Engineer, then re-run QA.
- Require SRE to map latency, traffic, errors, and saturation to instrumentation and an owner action.
- Defer only speculative scaling beyond the current operating envelope; record its trigger and next rung.
- Report commands and observations truthfully. Label inference as inference.

## Handoff

Conclude with:

```text
Outcome: <user-visible result>
Phases run: <Designer | Engineer | QA | SRE>
Contracts: <changed paths and executable evidence>
Verification: <commands and material results>
Operations: <signals, deploy, rollback>
Scale: <current envelope, trigger, next rung>
Risks/decisions: <specific items or none known>
```

The phase-specific references define the acceptance standard; do not replace them with a generic code review.
