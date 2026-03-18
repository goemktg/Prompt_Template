# GitHub Copilot Agent Instructions

Refer to `documents/PROJECT.md` for project-specific details.

> **AI Agent Operation Manual**: When operating as an autonomous agent,
> refer to `documents/AGENT_MANUAL.md` if available.

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

Project operations are performed via **MCP tools** (preferred) or CLI fallback.
All tools output in **JSON format** to prevent parsing errors.

### Tool Priority: MCP First

| Priority | Method | When to Use |
|----------|--------|-------------|
| 1 | **MCP Tools** | Default - real-time, integrated |
| 2 | CLI Fallback | MCP unavailable |
| 3 | Manual Execution | Human-only (never for AI agents) |

**MCP Tools (Preferred):**
| Tool | Purpose |
|------|------|
| `mcp_context7_*` | Library documentation lookup |
| `mcp_memory_*` | Store/retrieve agent memory |
| `mcp_arxiv_*` | Academic paper search |
| `mcp_sequentialthinking` | Complex reasoning support |

### Required Procedures

1. **Before complex tasks**: Check project context with semantic search
2. **Create artifacts**: Generate in appropriate directories (see Structure section)
3. **On failure**: Analyze with reasoning → Store findings in Memory MCP

### Memory Management

Use **Memory MCP** (`mcp_memory_*`) for all transient data:
- Observations/Notes → `mcp_memory_store_memory`
- Prior context lookup → `mcp_memory_search`
- List all memories → `mcp_memory_list`
- Memory quality check → `mcp_memory_quality`

**DO NOT** create local `*.memory.md` files. Use Memory MCP exclusively.

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

### Subagent Auto-Invocation Policy (Strict)

#### 1) Mandatory Invocation Triggers
You **MUST** invoke at least one specialized subagent via `runSubagent` when **ANY** of the following is true:

1. The task requires 3+ distinct phases (research, implementation, verification, documentation, etc.).
2. The task spans 2+ domains (for example, architecture + code + QA).
3. The user asks for optimization, root-cause analysis, or production-quality validation.
4. The expected work touches 3+ files or requires non-trivial refactoring.
5. The task needs external verification (documentation, papers, or web references) before implementation.

If a trigger is met, do **NOT** proceed as a single-agent workflow unless blocked by tooling or user constraints.

#### 2) Agent Selection Rules
- Architecture/design ambiguity: use `@architect`
- Bug diagnosis/fix execution: use `@fixer`
- Quality gate/review: use `@code-quality-reviewer`
- Regression/test reliability: use `@qa-regression-sentinel`
- Documentation generation/review: use `@doc-writer` / `@doc-reviewer`
- Research/theory/implementation feasibility: use `@research-gpt` / `@research-gemini` / `@research-claude`

#### 3) Parallel Delegation
If subtasks are independent, invoke subagents in parallel.

Examples:
- research + architecture
- implementation + QA validation
- documentation writing + code-quality review

#### 4) Delegation-First Workflow
For complex tasks, follow this order:

1. Decompose the task.
2. Delegate to specialized subagents.
3. Integrate subagent outputs.
4. Run validation.
5. Report with evidence.

#### 5) Anti-Skipping Guard
If no subagent is invoked for a trigger-matching task, the assistant **MUST** explicitly state why (tool limits, blocked context, or user constraints) and propose an alternative delegation plan.

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

## 0.3. Specialized Agent Protocol

**Use specialists over generalists when available.**

| Task Domain | Specialist Agent | Notes |
| :--- | :--- | :--- |
| Planning | `@planner-*` | Resource/timeline planning |
| Rubric-based verification | `@rubric-verifier` | Multi-perspective quality checks |
| Mathematical correctness | `@math-reviewer` | Equation/derivation/consistency validation |
| Experience curation | `@experience-curator` | Extract reusable patterns from history |

See `AGENTS.md` for full agent list and descriptions.

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

### Available Agents

| Agent | Purpose |
|-------|------|
| `@doc-writer` | Create documentation |
| `@doc-reviewer` | Review documentation |
| `@research-*` | Research tasks |

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

**Template Files Initialization**: If `.template.md` files exist, refer to the **"Template Files Initialization"** section in `AGENTS.md` for customization workflow and cleanup procedures.

**Publish-First Approach: Documents as deliverables only**

The `documents/` directory is RESERVED for human-readable, curated reports.
Raw logs, scratchpads, and intermediate data must LIVE IN MEMORY (MCP) or `logs/`.

```text
documents/
├── PROJECT.md          # 🟢 Project overview & status (if applicable)
├── AGENT_MANUAL.md     # 🟢 AI Agent operation manual (if applicable)
├── final/              # 🟢 PUBLISHED: Completed, verified reports
│   └── <TOPIC>_FINAL.md
├── drafts/             # 🟡 DRAFTS: Curated but not yet final
│   └── <TOPIC>_DRAFT.md
├── reference/          # 🔵 REFERENCE: External papers/docs
│   ├── papers/         # Academic papers summaries
│   ├── technical/      # API docs, technical guides
│   └── API_<library>_<topic>.md  # Library usage reference
└── templates/          # ⚪ TEMPLATES: Standard forms
```

### 🚫 STRICTLY PROHIBITED in `documents/`
- **Raw Logs / Scratchpads**: Use Memory MCP (`mcp_memory_store_memory`)
- **Daily Updates / TODOs**: Use Memory MCP or `manage_todo_list`
- **"Just in case" Notes**: If it's not worth curating, it's not a document.

### The Pipeline: Capture → Curate → Publish

1.  **Capture (Memory Layer)**
    - Agent stores raw observations, errors, and intermediate thoughts in Memory MCP.
    - *Action*: `mcp_memory_store_memory(content="Implementation note...", tags=["dev", "note"])`

2.  **Curate (Draft Layer)**
    - Agent synthesizes multiple memory entries into a structured draft.
    - *Action*: Create `documents/drafts/FEATURE_ANALYSIS_DRAFT.md`

3.  **Publish (Final Layer)**
    - Human or Reviewer Agent approves the draft. Moves to `final/`.
    - *Action*: `mv documents/drafts/x.md documents/final/x.md`

### Directory Rules
- **final/**: Truth. Reviewed. Permanent.
- **drafts/**: Work in progress. Semantically structured.
- **reference/**: External knowledge sources.
- **templates/**: Standard forms for new documents.

### Protected Files

**⚠️ CRITICAL: Never modify README.md**

The `README.md` file in the project root is a **universal development template** designed to work across all software projects. It is intentionally generic and framework-agnostic.

**Rules**:
- ❌ **DO NOT** edit README.md to add project-specific content
- ✅ **DO** add all project-specific details to `documents/PROJECT.md`
- ✅ **DO** refer users to `documents/PROJECT.md` for actual project information

**Rationale**: README.md serves as a reusable template for future projects. Project-specific content belongs in `documents/PROJECT.md`.

### Deprecated Paths → Memory MCP

| ❌ Deprecated | ✅ Use Instead |
|--------------|----------------|
| `documents/notes/` | `mcp_memory_store_memory` with tags |
| `documents/issues/` | `mcp_memory_store_memory` (tag: `issue`) |
| `documents/development/` | `mcp_memory_store_memory` |
| `documents/todo.md` | `manage_todo_list` tool |
| `*.memory.md` files | `mcp_memory_*` tools |

**Exception**: Major retrospectives/post-mortems go to `documents/final/`

---

## 8. Project Structure Guidelines

Adapt this structure to your project type. Common patterns:

### Software Development (General)

```text
.
├── src/                # Source code
│   ├── core/           # Core functionality
│   ├── utils/          # Utilities
│   └── archive/        # Archived code
├── tests/              # Test files
├── scripts/            # Build/deployment scripts
├── docs/               # Generated documentation (API docs, etc.)
├── documents/          # Curated documentation (see section 7)
├── results/            # Execution results (if applicable)
├── logs/               # Application logs
└── temp/               # Temporary files (gitignored)
```

### RimWorld Mod Development

```text
.
├── About/              # Mod metadata (About.xml)
├── Defs/               # Game definitions (XML)
├── Patches/            # Harmony patches (XML)
├── Source/             # C# source code (if any)
├── Textures/           # Graphics assets
├── Sounds/             # Audio assets
├── reference_codes/    # Reference mods for implementation study
└── documents/          # Development documentation
```

### Research/Experiment Projects

```text
.
├── src/                # Experiment code
│   └── experiments/    # Experiment implementations
├── configs/            # Configuration files
├── results/            # Experiment outputs
│   └── archive/        # Old results
├── documents/          # Research documentation
└── scripts/            # Automation scripts
```

---