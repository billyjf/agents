# From idea to production, with an agentic engineering team

This repository is a portable operating system for AI-native software delivery. It gives Claude Code four specialists with explicit responsibilities, handoffs, and evidence-based quality gates:

```text
rough idea
   |
   v
DESIGNER -> decision-ready specification
   |
   v
ENGINEER -> smallest complete implementation + contract tests
   |
   v
QA       -> independent functional verification
   |
   v
SRE      -> observable, operable, reversible production release
   |
   v
production evidence + next decisions
```

The governing principle is simple: move quickly by making "done" unambiguous. A feature is not finished when code exists. It is finished when its behavior is specified, its boundaries are tested, its failure modes are visible, and its release can be operated safely.

## What is included

- [`CLAUDE.md`](CLAUDE.md) is the team charter and end-to-end orchestrator.
- [`.claude/agents/DESIGNER.md`](.claude/agents/DESIGNER.md) turns rough intent into a decision-ready specification.
- [`.claude/agents/ENGINEER.md`](.claude/agents/ENGINEER.md) implements the smallest complete solution and owns the test contract.
- [`.claude/agents/QA.md`](.claude/agents/QA.md) verifies behavior independently, using functional and API contracts as the coverage floor.
- [`.claude/agents/SRE.md`](.claude/agents/SRE.md) makes the release observable and operable through the four golden signals.
- [`SCALABILITY.md`](SCALABILITY.md) records the next justified scaling rung without burdening today's product with hypothetical complexity.

These are real Claude Code project subagents. Clone or copy the files into a repository, start Claude Code at the repository root, and ask it to run the delivery pipeline for a feature. Claude Code discovers project agents from `.claude/agents/`.

## Example invocation

```text
Take this product bet from idea to a production-ready pull request using the
delivery pipeline in CLAUDE.md: <describe the outcome and constraints>.
```

You can also invoke a specialist directly:

```text
Use the designer agent to turn this rough request into an implementable spec.
Use the qa agent to verify this pull request against its behavior contracts.
Use the sre agent to review production readiness and golden-signal coverage.
```

## The philosophy

**Production-ready now; scale-ready when evidence says so.** The current product receives complete behavior, security, tests, observability, deployment, rollback, and documentation. Speculative scale machinery is kept out of the implementation. The next bottleneck, trigger, and migration are recorded in `SCALABILITY.md` so growth is deliberate instead of reactive.

**Functional confidence over vanity metrics.** Line coverage can reveal untested code, but it cannot prove a user journey or integration contract works. Every changed functional or API path gets an executable contract, including important failure behavior. Coverage percentage is a diagnostic, never the definition of quality.

**Simple systems recover faster.** Prefer the fewest moving parts that satisfy today's requirements. Make boundaries explicit, changes reversible, failures visible, and technical debt small enough to burn down continuously.

**Agents accelerate judgment; they do not replace it.** The pipeline preserves assumptions, alternatives, evidence, and unresolved risks so a senior reviewer can make a fast, informed decision. It is designed for AI-native teams that want their quality bar to compound with every feature.

