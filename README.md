# Agentic delivery: idea to production

This repository is a portable operating system for AI-native software delivery. It gives Claude Code, Codex, and Google Antigravity the same four named roles, quality gates, and handoff language while adapting the files to each harness's native format.

```text
rough idea
   |
   v
Designer -> decision-ready specification
   |
   v
Engineer -> smallest complete implementation + contract tests
   |
   v
QA       -> independent functional verification
   |
   v
SRE      -> observable, operable, reversible release
   |
   v
production evidence + next decisions
```

The governing principle is simple: move quickly by making "done" unambiguous. A feature is finished when its behavior is specified, its boundaries are tested, its failure modes are visible, and its release can be operated safely.

## The play

Maintain the shared team in this repository. Install a generated, versioned snapshot into each product repository. Run every harness from the product repository.

Do not make a product depend at runtime on a sibling `../agents` checkout. Do not manually copy prompts between repositories. `bin/agents-install` is the boundary: it reads the canonical material here, renders each harness's adapter, and records exactly what it installed.

There are two useful installation scopes:

- **Project install:** portable and commit-ready. The roles travel with that repository and are available to teammates and automation after cloning.
- **Global install:** personal convenience. The roles are available from any repository on the current machine, but teammates do not inherit them.

Project installation is the default and the recommended baseline. A global install can coexist with it; project-local definitions provide the project-specific snapshot.

## Canonical source

Edit these files when changing the team:

- [`CLAUDE.md`](CLAUDE.md) defines the delivery charter, phase gates, definition of done, and final handoff.
- [`.claude/agents/DESIGNER.md`](.claude/agents/DESIGNER.md) defines the Designer role.
- [`.claude/agents/ENGINEER.md`](.claude/agents/ENGINEER.md) defines the Engineer role.
- [`.claude/agents/QA.md`](.claude/agents/QA.md) defines the QA role.
- [`.claude/agents/SRE.md`](.claude/agents/SRE.md) defines the SRE role.
- [`SCALABILITY.md`](SCALABILITY.md) defines the evidence-based scaling ladder.
- [`adapters/shared/skills/agentic-delivery/SKILL.md`](adapters/shared/skills/agentic-delivery/SKILL.md) defines portable orchestration for skill-based harnesses.
- [`VERSION`](VERSION) identifies the snapshot release.

Claude's files remain the readable canonical role format because they are already valid Claude Code project agents and make this repository itself a working demonstration. The installer derives Codex TOML agents, shared Agent Skills, Antigravity rules/plugins, and installed reference snapshots from them.

Generated files in product repositories say they are generated. Change the source here, bump `VERSION`, and reinstall instead of editing generated snapshots by hand.

## Install into a product repository

Preview first:

```bash
bin/agents-install ../jekyll/bulkbarcode.app --dry-run
```

Install all three harness adapters:

```bash
bin/agents-install ../jekyll/bulkbarcode.app
```

Verify that the installation matches this release:

```bash
bin/agents-install ../jekyll/bulkbarcode.app --check
```

The target must already exist. The installer uses the exact directory supplied; it does not silently move upward to the Git root. That means a monorepo can install a specialized pipeline inside one application subtree.

The resulting product tree looks like this:

```text
bulkbarcode.app/
├── CLAUDE.md                         # existing content preserved; managed import appended
├── AGENTS.md                         # existing content preserved; managed policy appended
├── .claude/agents/
│   ├── designer.md
│   ├── engineer.md
│   ├── qa.md
│   └── sre.md
├── .codex/agents/
│   ├── designer.toml
│   ├── engineer.toml
│   ├── qa.toml
│   └── sre.toml
└── .agents/
    ├── agentic-delivery.lock.json
    ├── pipeline/                     # pinned charter, roles, scale notes, version
    ├── rules/agentic-delivery.md     # Antigravity workspace rule
    └── skills/
        ├── agentic-delivery/
        ├── designer/
        ├── engineer/
        ├── qa/
        └── sre/
```

The `.agents/skills` directory intentionally follows the open Agent Skills shape used by both Codex and Antigravity. Claude uses its native `.claude/agents` definitions. Codex additionally receives native `.codex/agents` TOML definitions so a role can run as an isolated custom agent instead of only as instructions in the main thread.

## Add project-specific truth

The shared team knows how to deliver software; it does not guess how a particular repository works. After installation, add product facts above the managed block in `CLAUDE.md` and `AGENTS.md`:

```markdown
# Project context

## Product

- Primary user and critical journey
- Current architecture and important boundaries

## Commands

- Install: `<command>`
- Dev: `<command>`
- Focused tests: `<command>`
- Full regression: `<command>`
- Lint/type/build: `<commands>`

## Production

- Runtime and deployment path
- Monitoring platform and alert destination
- Secret/configuration source
- Migration and rollback procedure
- Data, privacy, tenant, or billing risks
```

Do not edit between these markers:

```text
<!-- agentic-delivery:begin -->
...
<!-- agentic-delivery:end -->
```

Reinstallation updates only that managed block and preserves everything outside it.

## What happens in each harness

The role names and contracts are portable. The runtime primitive and invocation syntax are harness-specific.

| Intent | Claude Code | Codex | Antigravity IDE |
| --- | --- | --- | --- |
| Durable repo guidance | `CLAUDE.md` | `AGENTS.md` | `.agents/rules/*.md` |
| Named isolated role | `.claude/agents/*.md` | `.codex/agents/*.toml` | Invoke the matching Agent Skill/workflow |
| Portable workflow | Main agent delegates using the charter | `.agents/skills/agentic-delivery` | `.agents/skills/agentic-delivery` |
| Direct phase | “Use the QA agent” | “Spawn the QA agent” or `$qa` | “Use the qa skill” |
| Full pipeline | “Run the delivery pipeline” | `$agentic-delivery` | “Use the agentic-delivery skill” |

There is deliberately no claim that a universal `@qa` command exists. The human vocabulary stays stable—Designer, Engineer, QA, SRE—while the installed adapter translates it into the harness's supported mechanism.

### Claude Code mechanics

Start Claude from the target directory:

```bash
cd ../jekyll/bulkbarcode.app
claude
```

Claude loads the target's `CLAUDE.md`, which imports the installed delivery charter. It discovers the four project agents under `.claude/agents/`. Invoke a phase directly:

```text
Use the qa agent to run the independent QA gate on the current implementation.
Map every functional and API path to executable evidence. Do not edit files.
```

Or invoke the sequence:

```text
Run this change through the agentic delivery pipeline. Start at the earliest
applicable phase, stop on a failed gate, and return the consolidated handoff.
```

Claude's main conversation coordinates the work. Each named subagent gets a focused context and returns its result to the main conversation.

### Codex mechanics

Start Codex from the target directory:

```bash
cd ../jekyll/bulkbarcode.app
codex
```

Codex loads `AGENTS.md`, discovers project skills under `.agents/skills`, and discovers custom roles under `.codex/agents`. Invoke QA either as a skill in the current thread:

```text
Use $qa to run the independent QA gate on the current implementation.
```

Or explicitly request isolation:

```text
Spawn the qa custom agent to verify the current implementation. Wait for its
result and summarize the contract matrix and release blockers.
```

Invoke the complete coordinator with:

```text
Use $agentic-delivery to take this change through the applicable gates.
```

The installed `AGENTS.md` block allows Codex to delegate when the named role is useful. QA's Codex custom agent is configured read-only; the write-capable phases retain normal workspace-write isolation and the parent session's approval controls.

### Antigravity IDE mechanics

Open the target directory as the Antigravity workspace. Antigravity discovers `.agents/rules` and `.agents/skills`. Ask for a role by its stable name:

```text
Use the qa skill to run the independent QA gate on the current implementation.
```

Or ask for the coordinator:

```text
Use the agentic-delivery skill and begin at QA. Stop before SRE if QA fails.
```

Antigravity presents the roles as skills/workflows rather than assuming Claude's custom-subagent frontmatter. The same role body, acceptance standard, and handoff are preserved.

## First Bulk Barcode QA run

From this repository:

```bash
bin/agents-install ../jekyll/bulkbarcode.app --dry-run
bin/agents-install ../jekyll/bulkbarcode.app
bin/agents-install ../jekyll/bulkbarcode.app --check
```

Review what was installed before committing it:

```bash
git -C ../jekyll status --short -- bulkbarcode.app
git -C ../jekyll diff -- bulkbarcode.app/CLAUDE.md bulkbarcode.app/AGENTS.md bulkbarcode.app/.agents bulkbarcode.app/.claude bulkbarcode.app/.codex
```

Add Bulk Barcode's real build, test, deploy, and risk notes above the managed blocks. Then start the chosen harness with `../jekyll/bulkbarcode.app` as its working directory and use this QA request:

```text
Run the QA phase on the current Bulk Barcode implementation.

Independently enumerate every changed or user-critical functional/API path,
map each path to an executable contract test, run the relevant focused and
full regression checks, and report PASS, FAIL, or BLOCKED. Do not modify files.
For each gap, give severity, evidence, user impact, and the smallest corrective
action. Distinguish commands actually run from inference.
```

That request intentionally starts at QA. It does not rerun Designer or Engineer unless QA finds a failed/missing contract and the user asks Engineer to correct it.

## Global installation

Install personal copies for all repositories on the current machine:

```bash
bin/agents-install --global
bin/agents-install --global --check
```

Global destinations are:

```text
~/.claude/agents/                         Claude roles
~/.codex/agents/                          Codex roles
~/.agents/skills/                         Codex skills
~/.gemini/config/plugins/agentic-delivery Antigravity IDE plugin
```

Use global scope for personal consistency. Use project scope when the setup should travel with the repository. The two scopes can coexist; reinstall both after changing a canonical role if you depend on both.

## Installer commands and safety

```text
bin/agents-install [TARGET]
bin/agents-install [TARGET] --harness claude,codex,antigravity
bin/agents-install [TARGET] --dry-run
bin/agents-install [TARGET] --check
bin/agents-install [TARGET] --force
bin/agents-install --global
```

- `TARGET` defaults to the current directory.
- `--harness` defaults to `all` and accepts a comma-separated subset.
- `--dry-run` performs conflict checks and prints the planned writes.
- `--check` performs no writes and exits nonzero for missing/stale content.
- `--force` replaces modified or unmanaged generated files. It does not erase content outside managed instruction blocks.

The lock file stores the package version, selected harnesses, a content fingerprint, and the hash of every generated file. On update, the installer overwrites a generated file only when it still matches the previously installed hash. If somebody hand-edited a generated role, installation stops and names the conflict. Reconcile the change into this source repository before using `--force`.

The installer does not install dependencies, run project tests, commit files, change permissions for the coding harness, or access production systems.

## Updating the team

1. Edit the canonical charter, role, scale, or orchestration source in this repository.
2. Bump `VERSION`.
3. Validate locally.
4. Preview the target update with `--dry-run`.
5. Re-run the installer for each project/global scope.
6. Run `--check` in CI or before the next agent session.
7. Commit the generated project snapshot with the product repository when portability matters.

Because the target contains a pinned snapshot, existing projects do not change merely because this repository changes. Updates are deliberate and reviewable.

## Verify this repository

Run the installer regression suite and basic source checks before publishing a new version:

```bash
python3 -m py_compile bin/agents-install
python3 -m unittest discover -s tests -v
git diff --check
```

The regression suite covers fresh project and global installs, existing-instruction preservation, idempotence, harness subsets, lock accumulation, drift detection, and forced recovery. Release validation should also render the generated skills in a temporary project and run the current Agent Skills validator against all five skill folders.

## Delivery philosophy

**Production-ready now; scale-ready when evidence says so.** The current product receives complete behavior, security, tests, observability, deployment, rollback, and documentation. Speculative scale machinery stays out of the implementation. The next bottleneck, trigger, and migration belong in `SCALABILITY.md`.

**Functional confidence over vanity metrics.** Every changed functional or API path receives an executable contract, including important failure behavior. Line coverage can reveal blind spots, but it does not prove that a user journey or integration contract works.

**Simple systems recover faster.** Prefer the fewest moving parts that satisfy today's requirements. Make boundaries explicit, changes reversible, failures visible, and technical debt small enough to burn down continuously.

**Agents accelerate judgment; they do not replace it.** The pipeline preserves assumptions, alternatives, evidence, and unresolved risks so a senior reviewer can make a fast, informed decision.

## Harness documentation

- [Claude Code custom subagents](https://code.claude.com/docs/en/sub-agents)
- [Codex custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Codex skills](https://learn.chatgpt.com/docs/build-skills)
- [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Antigravity Agent Skills](https://antigravity.google/docs/skills)
- [Antigravity rules and workflows](https://antigravity.google/docs/rules-workflows)
- [Antigravity plugins](https://antigravity.google/docs/plugins)
