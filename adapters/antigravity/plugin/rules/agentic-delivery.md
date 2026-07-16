# Agentic delivery

Use the `agentic-delivery` skill for end-to-end product work. When the user names Designer, Engineer, QA, or SRE, activate the matching role skill and preserve its handoff contract.

Infosec is an optional read-only role, not an automatic delivery phase. Activate the `infosec` skill only when the user explicitly requests Infosec, a security audit, vulnerability assessment, supply-chain review, secret scan, or bounded penetration test. Keep any active testing inside the user's explicitly authorized targets and techniques.

Run the phases sequentially when they depend on one another. Do not allow multiple write-heavy phases to edit the same checkout concurrently. Treat repository-local instructions and commands as authoritative for the project.
