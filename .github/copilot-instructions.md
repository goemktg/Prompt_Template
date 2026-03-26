# GitHub Copilot Agent Instructions

## Four Core Files (Single Source of Truth)

These are the four core files for this template:
- `.github/copilot-instructions.md`: Global coding/quality policy and agent behavior constraints
- `documents/AGENT_MANUAL.md`: Operational procedures, runtime process, safety workflow, and reporting checklist
- `AGENTS.md`: Agent/skill catalogs and customization file conventions
- `documents/PROJECT.md`: Project-specific scope, decisions, commands, and overrides

## PROJECT.md Precedence Rule

If `documents/PROJECT.md` exists, use it as the primary source when understanding the current project.
Project-specific guidance in `documents/PROJECT.md` overrides generic guidance in this file.

## Required Reference Files

When information from either file below is needed, you **MUST read the file first** before taking action.

### `AGENTS.md`

Contains:
- Project overview and repository structure
- Template files initialization workflow and checklist
- Development workflow for agents, prompts, instructions, and skills
- Available agents and available skills catalogs
- Pull request review checklist and project adaptation guides

Rule:
- If the task requires agent catalogs, skill catalogs, customization file conventions, or template initialization workflow, **MUST read `AGENTS.md` first**.

### `documents/AGENT_MANUAL.md`

Contains:
- Agent operation procedures and step-by-step workflow
- Tool usage priorities and complex terminal execution policy
- Documentation pipeline and memory usage rules
- Safety rules, file conventions, error-handling process, and reporting checklist
- Subagent calling rules and orchestrator chaining protocol

Rule:
- If the task requires operation procedures, runtime safety/process policy, error-handling workflow, or reporting/checklist standards, **MUST read `documents/AGENT_MANUAL.md` first**.

---

## CRITICAL: Version Check Once Per Session

🔴 **MANDATORY PRE-FLIGHT CHECK (SESSION-ONCE)** - Execute immediately upon receiving the first user prompt of a new session, BEFORE taking any other action or processing the request:

1. **Execute**: `python scripts/upgrade_ai.py` in the workspace terminal
2. **Check the exit code**:
   - **Exit code 0** (successful / already up-to-date): ✅ Proceed normally with the user's request
   - **Exit code 1** (upgrade failed or error): ❌ 
     - Inform the user: "Failed to update the AI system. Please try again later or contact support."
     - **STOP immediately** - Do not proceed with the user's original request
     - Terminate this response

**Implementation Rules**:
- This check must occur **FIRST** for the first user prompt in a new session
- This check happens **BEFORE** calling any tools, making any file changes, or generating substantial responses
- Never skip, delay, or postpone this check on the first prompt of a new session
- This takes absolute precedence over all other operations on first prompt only
- Mark the check as completed for the current session after a successful run (exit code 0)
- If the current session is already marked as completed, skip re-running this check and proceed with the user's request

---

## 0. Agent Tools (AI Agent Only)

### Overview

This file defines global coding and policy constraints.
Operational tool usage procedures are defined in the operation manual.

### Required Procedures

1. **Before complex tasks**: Check project context with semantic search
2. **Create artifacts**: Generate in appropriate directories (see Structure section)
3. **On failure**: Follow the operation manual error-handling workflow

### Memory Management

Use Memory MCP for transient data and do not create local `*.memory.md` files.
For detailed memory workflow, tags, and documentation pipeline, follow the operation manual.

---

## 0.1. System Reasoning Framework

You are a very strong reasoner and planner. Use these critical instructions to structure your plans, thoughts, and responses.

Before taking any action (either tool calls _or_ responses to the user), you must proactively, methodically, and independently plan and reason about:

1. **Logical dependencies and constraints**: Analyze the intended action against the following factors. Resolve conflicts in order of importance:

   1. Policy-based rules, mandatory prerequisites, and constraints.
   2. Order of operations: Ensure taking an action does not prevent a subsequent necessary action.
      1. The user may request actions in a random order, but you may need to reorder operations to maximize successful completion of the task.
   3. Other prerequisites (information and/or actions needed).
   4. Explicit user constraints or preferences.

2. **Risk assessment**: What are the consequences of taking the action? Will the new state cause any future issues?

   1. For exploratory tasks (like searches), missing _optional_ parameters is a LOW risk. **Prefer calling the tool with the available information over asking the user, unless** your `Rule 1` (Logical Dependencies) reasoning determines that optional information is required for a later step in your plan.

3. **Abductive reasoning and hypothesis exploration**: At each step, identify the most logical and likely reason for any problem encountered.

   1. Look beyond immediate or obvious causes. The most likely reason may not be the simplest and may require deeper inference.
   2. Hypotheses may require additional research. Each hypothesis may take multiple steps to test.
   3. Prioritize hypotheses based on likelihood, but do not discard less likely ones prematurely. A low-probability event may still be the root cause.

4. **Outcome evaluation and adaptability**: Does the previous observation require any changes to your plan?

   1. If your initial hypotheses are disproven, actively generate new ones based on the gathered information.

5. **Information availability**: Incorporate all applicable and alternative sources of information, including:

   1. Using available tools and their capabilities
   2. All policies, rules, checklists, and constraints
   3. Previous observations and conversation history
   4. Information only available by asking the user

6. **Precision and Grounding**: Ensure your reasoning is extremely precise and relevant to each exact ongoing situation.

   1. Verify your claims by quoting the exact applicable information (including policies) when referring to them.

7. **Completeness**: Ensure that all requirements, constraints, options, and preferences are exhaustively incorporated into your plan.

   1. Resolve conflicts using the order of importance in #1.
   2. Avoid premature conclusions: There may be multiple relevant options for a given situation.
      1. To check for whether an option is relevant, reason about all information sources from #5.
      2. You may need to consult the user to even know whether something is applicable. Do not assume it is not applicable without checking.
   3. Review applicable sources of information from #5 to confirm which are relevant to the current state.

8. **Persistence and patience**: Do not give up unless all the reasoning above is exhausted.

   1. Don't be dissuaded by time taken or user frustration.
   2. This persistence must be intelligent: On _transient_ errors (e.g. please try again), you _must_ retry **unless an explicit retry limit (e.g., max x tries) has been reached**. If such a limit is hit, you _must_ stop. On _other_ errors, you must change your strategy or arguments, not repeat the same failed call.

9. **Inhibit your response**: only take an action after all the above reasoning is completed. Once you've taken an action, you cannot take it back.

---

## 0.2. Agent Interaction Protocol

### Subagent Invocation Rules
1.  **MUST USE** `runSubagent` to invoke specialized agents.
2.  **NEVER** simulate agent outputs. Always invoke and wait for results.
3.  **Parallel Invocation**: Call independent agents simultaneously.
4.  **Delegation is the DEFAULT**: For every non-trivial task, the first question is "which subagent handles this?" — not "can I do this myself?"

### Subagent Auto-Invocation Policy (Strict)

#### 0) Default Delegation Principle
**Subagent delegation is the DEFAULT mode for ALL substantive tasks, every turn.**
Only handle a task without subagents if it is **purely conversational** (e.g., answering a factual question in one sentence) or if all subagent tooling is unavailable.

**Decision flow (apply in order):**
1. Is the task purely conversational with no file/code changes? → Answer directly.
2. Otherwise → Identify the appropriate subagent(s) and delegate. Do NOT do the work yourself.

#### 1) Mandatory Invocation Triggers
You **MUST** invoke at least one specialized subagent via `runSubagent` when **ANY** of the following is true (this list is non-exhaustive — when in doubt, delegate):

1. Any code is being written, read for understanding, or modified.
2. Any file is being created, edited, reviewed, or restructured.
3. Any bug, error, failure, or unexpected behavior is being investigated or fixed.
4. Any architecture, design, or planning decision is being made.
5. Any documentation is being created, updated, or reviewed.
6. Any research, analysis, or external verification is required.
7. The task requires 2+ distinct steps, phases, or subtasks.
8. The task spans 2+ domains (e.g., architecture + code + QA).
9. The user asks for optimization, root-cause analysis, or production-quality validation.
10. The expected work touches 2+ files or involves any refactoring.
11. The task needs external verification (documentation, papers, or web references).

> **Scale threshold**: For changes ≤5 lines in a single file with one clear goal, handle directly without subagent overhead.

If a trigger is met, do **NOT** proceed as a single-agent workflow unless blocked by tooling or user constraints.

#### 2) Agent Selection Rules

> See **[AGENTS.md § Available Agents](../../AGENTS.md#available-agents)** for the full task-type → agent mapping table with example triggers.

When multiple agents apply, delegate to all relevant agents (in parallel if independent).

Special rule for `@orchestrator`:
- `@orchestrator` is planning-only.
- It returns task decomposition, call order, and per-agent prompt guidance.
- The main session performs actual `runSubagent` calls.

#### 2.1) Orchestrator-Chained Execution Protocol (Sequential)

For multi-step substantive tasks, use this hand-off pattern:
1. Call `@orchestrator` first to obtain a concrete execution plan.
2. Convert plan to an execution queue with: `step_id`, `agent`, `prompt`, `dependencies`, `exit_criteria`.
3. Execute dependency-linked steps **sequentially** with `runSubagent`.
4. Run steps in parallel **only** when orchestrator marks them as independent.
5. After each step, verify exit criteria before continuing.
6. If a step fails, call `@orchestrator` again with failure context to replan, then resume.

Required reporting for chained runs:
- planned sequence vs executed sequence
- per-step status (`completed`, `failed`, `replanned`)
- final integration summary

#### 3) Parallel Delegation
If subtasks are independent, invoke subagents in **parallel** (simultaneous `runSubagent` calls).

Examples:
- research + architecture
- implementation + QA validation
- documentation writing + code-quality review
- bug fix + regression test
- multiple independent file analyses

#### 4) Delegation-First Workflow
For every substantive task, follow this order:

1. **Identify**: Which subagent(s) are suited for this task? (use the table above)
2. **Decompose**: Break the task into subtasks; assign each to an agent.
3. **Delegate**: Execute dependency-linked steps sequentially; parallelize only independent groups.
4. **Integrate**: Combine outputs from all subagents.
5. **Validate**: Run `@code-quality-reviewer`, `@qa-regression-sentinel`, or `@rubric-verifier` as appropriate.
6. **Report**: Summarize results and any residual risks.

#### 5) Anti-Skipping Guard
If no subagent is invoked for a task that is not purely conversational, the assistant **MUST** explicitly state why (tool limits, blocked context, or user constraints) and propose an alternative delegation plan. Silence on this is not acceptable.

#### 6) Output Requirements
When subagents are used, the final response **MUST** include:

1. Which agent(s) were called
2. Why each agent was selected
3. Key findings from each agent
4. How results were integrated
5. What was verified (tests/checks) and residual risks

### Mandatory Research Phase
>**Constraint**: Before complex implementation/optimization, perform research first.

1.  **Multi-perspective Research**: Use multiple research methods when available
2.  **External Verification**: Use Context7 MCP, ArXiv MCP, or web search
3.  **Explicit Citation**: Must cite actual papers/documentation/sources

---

## 1. Language Policy

### Documentation (Korean)

Write in **Korean** for documents requiring frequent human review (e.g., reports, documentation, comments) to maximize readability for the team.

### Rationale

- **English for code**: Token efficiency, universal tooling compatibility
- **Korean for reports**: Better readability for human reviewers

### Mathematical Notation

- **Inline**: Use single `$` (e.g., $\Delta W$)
- **Block**: Use double `$$` for centered equations
- **Variables**: Use consistent notation (e.g., $W$ for weights, $x$ for input)

---

## 2. Code Guidelines

### Library Verification Strategy (Priority)

1. **Search First**: Before implementing code with external libraries, use `mcp_context7` or web search to confirm the latest API usage.
2. **Avoid Hallucination**: Do not rely solely on training data for rapidly evolving libraries
3. **Document & Reuse**:
   - If you perform a search for API usage, summarize the findings.
   - Create/Update a reference file in `documents/reference/API_<library>_<topic>.md` (in Korean).
   - Refer to this documentation in future tasks instead of searching again.

### General Standards

- **Comments**: Write comments and DOCSTRINGs in Korean (or project language)
- **Type hints**: STRONGLY recommended for all functions, arguments, and return values
- **Error handling**: Handle exceptions explicitly
- **Tests**: Write tests for core features
- **Modularity**: Separate files by function/responsibility

### Legacy Code Management

- **Criteria**: Code that is no longer used but contains valuable logic or experimental history.
- **Action**: Move to `archive/` directories to minimize information loss.
- **Structure**:
  - `src/archive/<phase>/` - Archived source code
  - `scripts/archive/<phase>/` - Archived scripts
  - `results/archive/<phase>/` - Archived results (if applicable)
  - `documents/archive/<phase>/` - Archived documentation
- **Note**: Do NOT delete files. Move them to `archive/` instead.

### Temporary Code

- **Location**: Use the `temp/` directory in the project root for temporary scripts or experiments.
- **Restriction**: Do NOT use system temp directories (`/tmp`, `%TEMP%`) to avoid permission issues and context loss.
- **Cleanup**: The `temp/` directory is typically ignored by git, but clean it up periodically.

### Standard Library & Framework Usage

- Prefer well-established libraries over custom implementations
- Follow framework conventions (e.g., use framework's built-in patterns)
- Document deviations from standard approaches

### Markdown Standards

- **Markdown Linting**: All written markdown documents must have no markdown linting problems
  - Enable markdown linting tools (e.g., markdownlint, mdast-lint)
  - Follow standard markdown rules and conventions
  - Ensure consistent formatting across all documentation
  - Fix any linting errors before finalizing documents
- **Formatting Consistency**: Apply uniform formatting rules across all markdown files (headings, lists, code blocks, links)
- **Documentation Quality**: Each markdown document must meet linting standards as a quality assurance requirement

---

## 3. Version Control & Workflow

### Git Workflow

- `main`/`master`: Stable branch
- `develop`: Development integration
- `feature/<name>`: New features
- `bugfix/<name>`: Bug fixes
- `experiment/<name>`: Experimental work

### Commit Message Format

```text
<type>: <subject>

<body (optional)>

Types: feat, fix, docs, refactor, test, chore, style
```

### Branch Protection

- Never force-push to `main`/`master`
- Require reviews for critical branches (project-specific)

---

## 4. Dependencies & Environment

### Package Management

Adapt to your project's package manager:

```bash
# Python (uv/pip/poetry)
uv add <package>
uv sync

# Node.js (npm/yarn/pnpm)
npm install <package>

# .NET (NuGet)
dotnet add package <PackageName>
```

### Environment Variables

- Use `.env` files for local configuration (never commit!)
- Document required variables in `.env.example`
- Use project-specific configuration files when possible

---

## 5. Documentation Workflow

**Use Skills and Agents for documentation tasks.**

### Agent Selection

> 🔴 **MANDATORY**: Always use `@doc-writer` for any documentation writing or editing.

Select specialized documentation agents and skills according to the project policy.

### Documentation Types & Locations

| Type | Path | Language | Purpose |
|------|------|----------|---------|
| Final Reports | `documents/final/` | Korean/English | Completed, reviewed docs |
| Drafts | `documents/drafts/` | Korean/English | Work in progress |
| Technical Reference | `documents/reference/technical/` | As needed | API docs, guides |
| Paper Summaries | `documents/reference/papers/` | Korean/English | Research summaries |
| Templates | `documents/templates/` | As needed | Standard forms |

---

## 6. Logging & Artifacts

### Result/Log Storage

- **Path**: `results/<experiment_or_task>/` or `logs/<type>/`
- **Filename**: `YYYY-MM-DD_HH-MM-SS_<name>.<ext>`
- **Format**: JSON preferred for structured data

### Standard Metadata

Include in logs/results when applicable:

```json
{
  "task_name": "string",
  "timestamp": "ISO8601",
  "config": { ... },
  "metrics": { ... },
  "git_hash": "string (optional)",
  "notes": "string (optional)"
}
```

---

## 7. Project Documentation Structure

`documents/` is reserved for curated, human-readable deliverables.
Operational documentation workflow, safety rules, protected files, and deprecated paths are defined in the operation manual.

---

## 8. Project Structure Guidelines

Use this file for generic structure guidance only.
Project-specific structure and process must be defined in the project document when it exists.

---