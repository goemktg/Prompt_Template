---
name: large-change-governance
description: 'Repository-wide structural large change governance with 4-phase workflow: RESEARCH → CONFIRM → IMPLEMENT → VERIFY. Triggers: large change, major refactor, cross-domain change, multi-file restructure, architectural overhaul, introduce new workflow.'
---

# large-change-governance

## Usage

Use this skill when a task involves repository-wide structural large changes that span multiple files, directories, or domains. This includes architectural redesigns, new workflow introductions, cross-domain refactors, and policy overhauls.

## Responsibility

This skill owns the change governance process:

- Scope: phased workflow enforcement, research-first mandate, user confirmation gates, verification requirements.
- Out of scope: domain-specific implementation details (delegated to specialist agents).

This is a **process wrapper**, not a domain specialist. It orchestrates domain agents (`@master-prompt-writer`, `@architect`, `@code-generator`, `@doc-writer`, `@orchestrator`) based on change type.

## Trigger Heuristics

**Triggers (any of these apply):**

- Changes spanning 3+ files across 2+ directories
- Estimated 50+ line modifications
- Public interface or API changes
- Cross-domain changes (e.g., code + docs + config)
- New workflow or policy introduction
- User explicitly requests "plan first" or "research first"
- Structural reorganization of directories or file ownership

**Non-Triggers (skip this workflow):**

- Single-file typo or wording fixes
- Isolated bug fixes confined to one module
- Simple table row updates or list additions
- Routine commits following existing patterns
- Documentation edits under 20 lines in a single file

**Borderline cases**: When uncertain, default to triggering Phase 1. It is safer to perform research that turns out to be unnecessary than to skip research on a change that needed it.

## Protocol

### Phase 1: RESEARCH

**Objective**: Produce a change plan report before any implementation.

**Execution Subject**: Domain-appropriate subagent (e.g., `@master-prompt-writer` for prompt assets, `@architect` for code architecture, `@doc-writer` for documentation structure).

**Steps**:

1. Survey related documents, policies, and existing implementations
2. Identify all affected files and sections
3. Analyze risks and dependencies
4. Produce a draft report at `documents/drafts/<topic>-<date>.md`

**Outputs**:

- Report path
- Key recommendations summary (5-8 bullets)
- Target file/section list
- Risk assessment

### Phase 2: CONFIRM

**Objective**: Obtain explicit user approval before implementation.

**Execution Subject**: Main session (Tier 1 interactive gate).

**Gate Protocol**:

```text
┌──────────────────────────────────────────────────────┐
│              USER CONFIRMATION GATE                   │
├──────────────────────────────────────────────────────┤
│ 1. Present report path                               │
│ 2. Display key changes summary                       │
│ 3. Request explicit approval: "Proceed?"            │
├──────────────────────────────────────────────────────┤
│ Approval: yes, proceed, approve, confirm             │
│ Rejection: no, cancel, stop                          │
│ Revision: specific modification requests             │
├──────────────────────────────────────────────────────┤
│ On approval → Phase 3                                │
│ On rejection → Terminate, preserve report            │
│ On revision → Return to Phase 1, update report       │
└──────────────────────────────────────────────────────┘
```

**Revision Loop**: Maximum 3 revision cycles before escalation warning.

### Phase 3: IMPLEMENT

**Objective**: Execute the approved plan.

**Execution Subject**: Domain-specialist subagents based on change type:

| Change Type | Primary Agent |
|-------------|---------------|
| Prompt / policy assets | `@master-prompt-writer` |
| Code architecture | `@architect` → `@code-generator` |
| Documentation structure | `@doc-writer` |
| Multi-domain complex | `@orchestrator` → subagents |

**Rules**:

- Follow the report's Implementation Plan section
- Check file ownership before each edit
- Record each file modification in Memory MCP
- On unexpected conflicts, return to Phase 2 for re-approval

### Phase 4: VERIFY

**Objective**: Validate implementation and update documentation.

**Execution Subject**: Main session → `@doc-reviewer` (for markdown validation), domain reviewers as needed.

**Steps**:

1. Verify all planned changes were completed
2. Run appropriate validation (`@doc-reviewer` for markdown, `@code-quality-reviewer` for code)
3. Append "Implementation Results" section to the original report
4. Move report from `documents/drafts/` to `documents/final/` if approved

**Report Update Contents**:

- Actual modified file list (vs. planned)
- Issues discovered and resolutions
- Future recommendations

## Emergency Override

If extraordinary circumstances require bypassing this workflow:

1. User must explicitly state: "Override large-change governance"
2. Log the override with `[GOVERNANCE OVERRIDE]` tag in Memory MCP
3. After completion, create a minimal post-hoc report in `documents/drafts/`

**Partial Failure Handling**:

| Condition | Action |
|-----------|--------|
| Phase 1 fails (research blocked) | Report `[RESEARCH BLOCKED]`, provide partial findings, request user guidance |
| Phase 2 times out (no user response) | Preserve state in Memory MCP, resume when user re-engages |
| Phase 3 partial completion | Log completed files, mark remaining work, return to Phase 2 with updated scope |
| Phase 4 validation fails | Do not promote report, list failures, request remediation cycle |

## Output Contract

Each workflow execution produces:

- Research report (Phase 1)
- Approval record (Phase 2)
- File modification log (Phase 3)
- Verification verdict with review evidence (Phase 4)

## Self-Application Note

This governance workflow was itself developed using this protocol:

- Phase 1: [large-change-governance-workflow-2026-04.md](../../../documents/drafts/large-change-governance-workflow-2026-04.md)
- Phase 2: User confirmation obtained
- Phase 3: Creation of this SKILL.md and policy updates
- Phase 4: `@doc-reviewer` validation — CONDITIONAL (run lcg-review-2026-04-09, 93/100)

## Exit Criteria

A large change is complete when:

- All four phases have been executed
- Report is finalized in `documents/final/`
- Verification evidence is documented
- No blocking issues remain open
