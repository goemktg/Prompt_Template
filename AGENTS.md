# AGENTS.md

## Scope & References

**Scope**:

- Catalog of available Agents and Skills
- Conventions for Agent definitions and customization files
- Development workflow for creating new Agents/Skills

**Out of Scope**:

- Global normative policies (See `shared/copilot-instructions.md`)
- Runtime execution details that belong to the active policy, skill, or agent asset

**References**:

- **Constitution**: `constitution.md` (Immutable governance principles)
- **Policy**: `shared/copilot-instructions.md` (Rules)
- **Instruction Files**: `shared/instructions/*.instructions.md` (Surface-specific authoring rules)

**Authority Boundary**:

- Global policy lives in `shared/copilot-instructions.md`.
- Surface-specific authoring rules live in `shared/instructions/` and deployed instruction mirrors.
- This file owns agent and skill catalog information, routing, and repository structure guidance.

## Project Overview

This is a universal project template designed for various types of development projects. It provides:

- **Custom Agents**: Specialized AI agents for diverse development tasks (architecture planning, autonomous debugging, refactoring, research, documentation)
- **Agent Skills**: Reusable workflows for common operations (documentation, code review, research)
- **Infrastructure**: Standardized logging, task tracking, and dynamic context maintenance
- **Flexibility**: Adaptable to software development, research, mod development, and more

Repository-wide coordination follows a lifecycle-first operating model: `INIT -> ATOMIZE -> PLAN -> EXECUTE -> REPORT -> AWAIT -> FINALIZE`. The orchestrator-first main session owns coordination boundaries, while specialist agents perform substantive `EXECUTE` work. Mediator or council-style mechanisms are optional protocol overlays, not the default baseline.

## Repository Structure

```text
.
├── constitution.md              # Thin immutable governance principles
├── shared/
│   ├── copilot-instructions.md  # Source-of-truth global Copilot instructions
│   └── instructions/            # Source-of-truth instruction files
├── .github/
│   ├── instructions/            # Deployed instruction mirrors for workspace/runtime visibility
│   └── prompts/                 # Reusable prompt templates (.prompt.md)
├── copilot/
│   ├── agents/                  # Runtime-owned agent definitions (.agent.md)
│   ├── skills/                  # Skill definitions and bundled assets (auto-applied)
│   ├── hooks.json               # Runtime hook manifest (optional)
│   ├── hooks/                   # Runtime hook scripts (optional)
│   └── mcp.json                 # Runtime MCP configuration
├── src/                     # Source code (adapt to your project)
├── tests/                   # Test files
├── scripts/                 # Automation scripts
├── documents/               # Curated documentation
│   ├── final/               # Published reports
│   ├── drafts/              # Work in progress
│   ├── reference/           # External references
│   │   ├── papers/          # Academic paper summaries
│   │   └── technical/       # API docs, technical guides
│   ├── templates/           # Document templates
│   └── skills/              # Human-readable skill references (optional)
├── references/              # Reference repositories and external examples
│   └── [external projects]  # For implementation and governance reference
├── results/                 # Execution results (if applicable)
├── logs/                    # Application logs
└── temp/                    # Temporary files (gitignored)
```

## Development Workflow

### Working with Agents, Skills, and Prompts

#### Agent Files (`*.agent.md`)

Location: `copilot/agents/`

Custom agent definitions with specialized behaviors and tool access.

**Required Frontmatter:**

- `name`: Agent identifier (lowercase with hyphens)
- `description`: What the agent does (wrapped in single quotes)

**Optional Frontmatter:**

- `tools`: Array of tool names/patterns the agent can use
- `argument-hint`: Describes expected input format
- `model`: Preferred LLM model
- `infer`: Enable inference mode

Example:

```yaml
---
name: my-agent
description: 'Description of what the agent does and when to use it.'
tools:
  - read
  - search
  - execute
  - memory/*
---

# Agent Instructions
...
```

#### Prompt Files (`*.prompt.md`)

Location: `.github/prompts/`

Reusable prompt templates. Configure via `chat.promptFilesLocations` setting.

**Frontmatter:**

- `agent`: Agent name to use
- `tools`: Array of tools to use
- `description`: Short description

Example:

```yaml
---
agent: 'agent'
tools: ['codebase', 'githubRepo']
description: 'Generate a new configuration file'
---

Your goal is to create a new configuration...
```

#### Instruction Files (`*.instructions.md`)

Source-of-truth location: `shared/instructions/`

Deployed mirror location: `.github/instructions/`

Modular instruction sets that can be combined. Configure via `chat.instructionsFilesLocations` setting.

#### Agent Skills (`skills/*/SKILL.md`)

Skills are auto-applied from `copilot/skills/<skill-name>/SKILL.md`.

Skills can include bundled assets (scripts, templates, data files) in their respective directories.

- Each skill is a folder containing a `SKILL.md` file
- SKILL.md must have `name` field (lowercase with hyphens, matching folder name)
- SKILL.md must have `description` field (wrapped in single quotes, 10-1024 chars)
- Skills can include bundled assets (scripts, templates, data files)
- Skills follow the [Agent Skills specification](https://agentskills.io/specification)

Example:

```yaml
---
name: my-skill
description: 'Description of the skill and when it should be loaded.'
---

# My Skill

## Usage
...

## Protocol
...
```

### Adding New Resources

**For Agents:**

1. Create `copilot/agents/<name>.agent.md` with proper frontmatter
2. Define the agent's purpose, tools, and instructions
3. Test the agent with sample prompts

**For Skills:**

1. Create `copilot/skills/<skill-name>/SKILL.md`
2. Add YAML frontmatter with `name` and `description`
3. Write clear instructions and examples
4. Optionally add bundled assets (scripts, templates, data files) in the skill's directory

**For Prompts:**

1. Create `.github/prompts/<name>.prompt.md`
2. Add frontmatter with `agent`, `tools`, and `description`
3. Write the prompt template with clear instructions

## Skill Routing

This section is the single source of truth for skill-to-execution mapping. The main prompt should detect that a skill applies, then consult this section instead of embedding the full routing table inline.

Baseline operating model: repository-wide orchestration follows `INIT -> ATOMIZE -> PLAN -> EXECUTE -> REPORT -> AWAIT -> FINALIZE`. Skill routing plugs specialists and overlays into that lifecycle; it does not replace the lifecycle itself.

Current implementation order: lifecycle first by default, with implemented mediator and council overlays available as explicit protocol hops when a task calls for them and the relevant protocol assets/runtime backends are present.

| Skill | Trigger Keywords | Execution Mode | Reason |
| :--- | :--- | :--- | :--- |
| `commit-skill` | commit, save changes with git | **Main agent direct (Tier 1)** | Interactive protocol requires user confirmation between steps; subagent cannot pause for I/O |
| `documentation` | write doc, create report, publish | **Delegate → `@doc-writer` (Tier 2)** | Substantive work; specialist subagent produces higher quality output |
| `code-review` | review source code, code review, review code before merge | **Delegate → `@code-quality-reviewer` (Tier 2)** | Substantive work; dedicated review subagent |
| `deep-research` | research, investigate (multi-source) | **Delegate → `@research-gpt` / `@research-gemini` / `@research-claude` (Tier 2)** | Substantive work; multi-source research subagents |
| `deep-think` | deep-think, multi-hypothesis reasoning, structured refinement, mediator triage | **Delegate → `@deep-think-mediator` (Tier 2)** | Uses the implemented mediator-first deep-think overlay when the task explicitly calls for that reasoning protocol. |
| `data-analysis` | analyze results, compare metrics | **Delegate → `search_subagent` (built-in) + main agent (Tier 2)** | Substantive work; exploration + synthesis pattern |
| `dt-council` | dt-council, model council, diverse perspectives, mediator redirect | **Delegate → `@dt-council-mediator` (Tier 2)** | Uses the implemented council mediator overlay for explicit multi-perspective council protocol work. |
| `lifecycle-runtime-ops` | verify runtime activation, write lifecycle transition, hydrate lifecycle state, refresh runtime, cleanup runtime artifacts | **Delegate → `@executor` (Tier 2)** | Operational protocol runs existing repo-local runtime scripts and bounded workspace-state checks without widening scope |
| `skill-extension` | create new skill, new SKILL.md | **Delegate → `@code-generator` (Tier 2)** | Substantive work; structured file generation |
| `external-skill-generation` | import external skill | **Tier 1 gate + Tier 2 delegation** | Security review gates (steps 1, 3, 6) run in main session (Tier 1). Substantive extraction and rewrite (steps 2, 4, 5) delegate to `@code-generator` via `runSubagent`. Main session holds approval authority between phases. |
| `paper-catalog-update` | update prompt paper catalog, run catalog update procedure, improve catalog update procedure | **Delegate → `@master-prompt-writer` (Tier 2)** | Substantive work; maintains the paper catalog and supports prompt planning from curated papers |
| `copilot-eval-benchmark` | benchmark copilot, score customized copilot, swe-bench verified import | **Main agent direct (Tier 1/2 hybrid; no SKILL.md file)** | Local Copilot stack cannot be fully headless; use semi-automated run-sheet + scoring pipeline without a loadable SKILL.md asset |
| **Prompt planning (direct agent)** | design prompt, plan prompt, 프롬프트 설계, 프롬프트 전략 | **Delegate → `@master-prompt-writer` (Tier 2)** | Research-grounded prompt engineering; always directly authors prompt assets (no plan-only mode) |
| **Prompt analysis / technique report** | analyze prompt, prompt technique report, prompt paper analysis, 프롬프트 기법 분석 | **Delegate → `@master-prompt-writer` (Tier 2), then `@doc-writer` for `documents/` finalization** | Domain expertise required; 2-step handoff: @master-prompt-writer produces content, @doc-writer formats and publishes to `documents/` |

### Prompt-Analysis Routing Clarification

> **Prompt-analysis, prompt-technique, and prompt-paper deliverables are NOT ordinary documentation routing.**
>
> - **First**: `@master-prompt-writer` produces the analytical content (technique evaluation, paper-backed analysis, evidence-based recommendations).
> - **Then**: If the final artifact must be a publication document under `documents/`, `@doc-writer` takes the fact sheet and applies formatting, Korean prose, and template compliance.
> - **Rationale**: `@doc-writer` lacks prompt-paper domain expertise; `@master-prompt-writer` lacks `documents/` publication authority.

## Available Agents

Use this table to identify which agent to call for each task type. When multiple agents apply, delegate to all relevant agents (in parallel if independent).

> **Pre-selection**: Read the gate sequence and lifecycle framing from `shared/copilot-instructions.md § 0-SKILL`, `§ 0-INTENT`, `§ 0-GATE`, and `§ 0.2 Lifecycle-First Operating Model` first, including whether the direct-answer carveout is still available. In this repository, user commands are assumed to arrive in an orchestrator-invoked main-session context. Use `@orchestrator` only when explicit sequencing, dependency management, or resumable multi-step coordination is needed; do not use it as a universal router.
>
> **Domain Priority Reminder**: Prompt assets (`@master-prompt-writer`) > General docs (`@doc-writer`) > Code review (`@code-quality-reviewer`). The word "review" alone does NOT default to code-review — check artifact type.

| Task Type | Agent | Description | Example Triggers |
| :--- | :--- | :--- | :--- |
| **Complex orchestration** | `@orchestrator` | Thin lifecycle coordination contract for the orchestrator-first main session. It frames work, sequences specialists, emits delegation/TODO artifacts, and keeps `AWAIT` and resumable progress explicit, while substantive `EXECUTE` work stays with specialist subagents. Runtime sync/state enforcement belongs to runtime-owned surfaces, not the agent file. | "plan this", "multi-phase task", "coordinate agents" |
| **Deep-think protocol mediation** | `@deep-think-mediator` | Thin protocol hop between `@orchestrator` and an available deep-think reasoning asset. It hosts protocol-local sequencing, returns normalized results, and can emit redirect metadata for council escalation without becoming a shadow orchestrator. | "deep-think this", "multi-hypothesis reasoning", "escalate to deep analysis" |
| **Council protocol mediation** | `@dt-council-mediator` | Thin protocol hop between `@orchestrator` and an available council reasoning asset. It keeps council-local sequencing and synthesis packaging out of the orchestrator while preserving lifecycle-first control in the caller. | "run council analysis", "extended council reasoning", "cross-model council" |
| **New code / feature implementation** | `@code-generator` | Code generation with best practices and type safety. | "implement X", "add feature Y", "write a function for Z" |
| **Bug / error / failure diagnosis & fix** | `@fixer` | Autonomous problem-solving & execution agent. Diagnoses issues, implements fixes, executes code/tests, and verifies solutions. | "fix this", "error in", "not working", "debug" |
| **Architecture / design planning** | `@architect` | Architecture Planner. Designs system architecture and technical solutions. | "design", "how should I structure", "best approach for" |
| **Code review / quality gate** | `@code-quality-reviewer` | Code Quality Reviewer. Reviews **source code files only** (`.py`, `.ts`, `.js`, `.java`, `.c`, `.cpp`, etc.) for bugs, style, and standards compliance. Does NOT review documentation, prompt assets, or markdown files. | "review my code", "check this function", "PR code review", "is this code correct?", "code quality check" |
| **Regression / test reliability** | `@qa-regression-sentinel` | Execution-based quality verification, reproduction scripts, and flaky test detection. | "run tests", "check for regressions", "flaky test" |
| **Documentation writing** | `@doc-writer` | Documentation Writer (documentation only — not prompt assets). **Directly authors and edits** documentation files from requirements. Must write files itself, not return drafts for the main session to apply. Prompt authoring requests must be routed to `@master-prompt-writer`. | "write docs", "document this", "create README" |
| **Documentation review** | `@doc-reviewer` | Documentation Reviewer. Performs a single review pass and returns structured findings only; the caller owns fixes and re-invocation. | "review this doc", "check documentation" |
| **Shell / runtime execution** | `@executor` | Execution specialist for shell-native commands and runtime tasks. Uses terminal execution for shell-native tools and routes Python execution through pylance-mcp-server/pylanceRunCodeSnippet instead of terminal Python by default. | "run this command", "execute build", "install dependency", "run tests in terminal" |
| **Theory / concept research** | `@research-gpt` | Theory-focused research (Concepts, Prior Work). | "explain theory behind", "what is X", "prior work on" |
| **Implementation / API research** | `@research-gemini` | Implementation-focused research (Code, API, Hardware). | "how to implement X with library Y", "API usage for" |
| **System / safety / risk research** | `@research-claude` | System/Safety-focused research (Complexity, Constraints). | "risks of", "constraints for", "safety analysis" |
| **Quantitative / feasibility planning** | `@planner-gemini` | Feasibility & Resource Planning (Quantitative). | "is this feasible?", "estimate resources for" |
| **Architecture / strategy planning** | `@planner-gpt` | Architecture & Strategy Planning (Structural). | "plan the architecture", "design strategy for" |
| **Risk / QA planning** | `@planner-claude` | Risk & QA Planning (Safety). | "what could go wrong?", "risk assessment" |
| **Math / equation verification** | `@math-reviewer` | Mathematical verification of research paper implementations. | "verify formula", "check math", "is this equation correct?" |
| **Rubric-based quality verification** | `@rubric-verifier` | Multi-perspective quality verification with rubrics and independent critics. | "validate against criteria", "multi-perspective check" |
| **Idea validation (methodology/theory)** | `@validator` | Verification and validation of code, configs, and outputs. | "validate this idea", "is this approach correct?" |
| **Creative / UX / divergent ideas** | `@idea-generator-claude` | UX, Safety & Divergent Thinking Ideas. | "brainstorm ideas for", "alternative approaches" |
| **Feasibility-focused ideas** | `@idea-generator-gemini` | Feasibility & Resource Optimization Ideas. | "what's a cost-effective way to", "optimize resource usage" |
| **Architecture-focused ideas** | `@idea-generator-gpt` | System Architecture & Business Strategy Ideas. | "what's the best system design for", "scalable architecture" |
| **Research lineage / citation** | `@citation-tracer` | Builds research lineage via DFS citation chaining. Identifies foundational papers. | "find foundational papers for", "citation chain for" |
| **Pattern extraction from history** | `@experience-curator` | Learns from project history. Extracts reusable patterns from logs, failures, and reviews. | "what did we learn?", "extract patterns from" |
| **Codebase exploration / Q&A** | `search_subagent` (built-in) | VS Code built-in codebase exploration tool. Fast read-only search and Q&A. Not a custom agent file. | "where is X defined?", "how does Y work?", "find files matching" |
| **Research-backed prompt engineering** | `@master-prompt-writer` | Designs, creates, edits, and **analyzes** prompt assets (`.agent.md`, `SKILL.md`, `.prompt.md`, `copilot-instructions.md`) grounded in the internal paper database. Also handles **routing policy improvements**, **agent/skill customization**, and **prompt-technique analysis**. Always directly authors files — no plan-only mode. Invokes `@doc-reviewer` for validation before completion and owns any fix-and-re-review loop triggered by review findings. General project docs (not prompt assets) remain `@doc-writer`'s responsibility. | "write a prompt for", "which prompting technique", "select prompt technique", "prompt planning", "prompt blueprint", "프롬프트 설계", "프롬프트 전략", "prompt for agent", "prompt template", **"analyze routing"**, **"improve agent instructions"**, **"fix routing logic"**, **"review prompt asset"**, **"agent definition"**, **"skill file analysis"** |

## Project-Specific Agent Surfaces

These agents extend the repository with optional mediator layers while keeping lifecycle-first orchestration as the baseline:

| Agent | File | Role |
| :--- | :--- | :--- |
| `@deep-think-mediator` | `copilot/agents/deep-think-mediator.agent.md` | First-hop mediator for deep-think-style protocol execution. Returns either normalized deep-think results or redirect metadata for council escalation, and uses a Gemini-family runtime path only when the host environment provides native Gemini access outside the repo-owned runtime. |
| `@dt-council-mediator` | `copilot/agents/dt-council-mediator.agent.md` | Council-local mediator that sequences an available council protocol without taking over lifecycle ownership from `@orchestrator`, and uses a Gemini-family runtime path only when the host environment provides native Gemini access outside the repo-owned runtime. |

## Available Skills

| Skill | Description | Execution Mode |
| :--- | :--- | :--- |
| `documentation` | Standardized documentation creation and formatting (subagent directly writes/edits files) | **Delegate → `@doc-writer`** |
| `code-review` | Source-code review checklist for correctness, regressions, and maintainability | **Delegate → `@code-quality-reviewer`** |
| `deep-research` | Recursive research workflow (STORM-style) | **Delegate → `@research-gpt` / `@research-gemini` / `@research-claude`** |
| `deep-think` | Mediator-first deep reasoning workflow for explicit deep-think protocol tasks | **Delegate → `@deep-think-mediator`** |
| `data-analysis` | Result visualization and statistical comparison | **Delegate → `search_subagent` (built-in) + main agent** |
| `dt-council` | Mediator-first multi-perspective council workflow for explicit council protocol tasks | **Delegate → `@dt-council-mediator`** |
| `lifecycle-runtime-ops` | Repeatable lifecycle runtime operations using existing repo-local verification, state, refresh, and cleanup scripts | **Delegate → `@executor`** |
| `skill-extension` | Create and extend agent skills | **Delegate → `@code-generator`** |
| `paper-catalog-update` | Monthly update workflow for prompt engineering paper catalog (freshness check, scoring, add/retire, metadata sync) | **Delegate → `@master-prompt-writer`** |
| `external-skill-generation` | Generate skills from external documentation | **Tier 1 gate + Tier 2 delegation** (`@code-generator` for extraction/rewrite phases) |
| `commit-skill` | Commit workflow with diff-based message generation and explicit user confirmation gate before `git commit` | **Main agent direct** (interactive gate) |
| `copilot-eval-benchmark` | Semi-automated scoring workflow for customized local Copilot, including optional SWE-bench Verified task import | **Main agent direct (Tier 1/2 hybrid; no SKILL.md file)** |

Lifecycle-first orchestration remains the default. Mediator and council overlays are implemented as explicit optional protocol layers, not universal routing, and are used only when the relevant protocol assets and runtime backends are present.

## Adding Custom Agents

To add project-specific agents:

1. Define agent roles and capabilities in this file
2. Create `copilot/agents/<name>.agent.md` with proper frontmatter
3. Reference agents in tasks using `@agent-name`
4. Use `runSubagent` to invoke specialized agents
5. Document agent protocols and expected outputs

## Project-Specific Adaptations

### RimWorld Mods

- **Focus**: XML patching, C# Harmony patches, asset management
- **Key Agents**: `@doc-writer`, `@code-quality-reviewer`, `@validator`
- **Common Skills**: `documentation`, `code-review`
- **Testing**: Manual in-game testing, log analysis

### Research Projects

- **Focus**: Experiment tracking, result analysis, paper summaries
- **Key Agents**: `@research-*`, `@math-reviewer`, `@citation-tracer`
- **Common Skills**: `deep-research`, `data-analysis`, `documentation`
- **Testing**: Reproducibility checks, statistical validation

### Web Development

- **Focus**: API design, frontend/backend separation, deployment
- **Key Agents**: `@architect`, `@code-generator`, `@qa-regression-sentinel`
- **Common Skills**: `code-review`, `documentation`
- **Testing**: Unit tests, integration tests, E2E tests

### Game Development

- **Focus**: Asset pipelines, gameplay systems, performance optimization
- **Key Agents**: `@architect`, `@fixer`, `@code-quality-reviewer`
- **Common Skills**: `code-review`, `documentation`
- **Testing**: Playtesting, performance profiling

### General Software

- **Focus**: Feature development, bug fixing, refactoring
- **Key Agents**: `@orchestrator`, `@fixer`, `@code-generator`
- **Common Skills**: `code-review`, `documentation`
- **Testing**: Unit tests, integration tests

Refer to the project-specific documentation under `documents/` for agent configuration patterns and workflow anchors.

## Related Resources

- [Agent Skills Specification](https://agentskills.io/specification) - Official Agent Skills standard
- [GitHub Awesome Copilot](https://github.com/github/awesome-copilot) - Curated Copilot resources
- [VS Code Copilot Customization](https://code.visualstudio.com/docs/copilot/customization/agent-skills) - Official documentation
- [GitHub Copilot Documentation](https://docs.github.com/en/copilot) - Complete Copilot guide
- Project Documentation:
  - `documents/` - Project-specific overview and status documentation
  - [`constitution.md`](constitution.md) - Immutable governance principles and ownership boundaries
  - [`shared/copilot-instructions.md`](shared/copilot-instructions.md) - Source-of-truth development guidelines
