# AGENTS.md

## Scope & References

**Scope**:

- Catalog of available Agents and Skills
- Conventions for Agent definitions and customization files
- Development workflow for creating new Agents/Skills

**Out of Scope**:

- Global normative policies (See `.github/copilot-instructions.md`)
- Runtime operational procedures and execution checklists (See `documents/AGENT_MANUAL.md`)

**References**:

- **Manual**: `documents/AGENT_MANUAL.md` (Workflows)
- **Policy**: `.github/copilot-instructions.md` (Rules)

## Project Overview

This is a universal project template designed for various types of development projects. It provides:

- **Custom Agents**: Specialized AI agents for diverse development tasks (architecture planning, autonomous debugging, refactoring, research, documentation)
- **Agent Skills**: Reusable workflows for common operations (documentation, code review, research)
- **Infrastructure**: Standardized logging, task tracking, and dynamic context maintenance
- **Flexibility**: Adaptable to software development, research, mod development, and more

## Repository Structure

```text
.
├── .github/
│   ├── agents/              # Custom agent definitions (.agent.md)
│   ├── skills/              # Agent Skills (folders with SKILL.md)
│   ├── prompts/             # Reusable prompt templates (.prompt.md)
│   └── copilot-instructions.md  # Global Copilot instructions
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
├── reference_codes/         # Reference code from external projects
│   └── [external mods/libs] # For implementation reference
├── results/                 # Execution results (if applicable)
├── logs/                    # Application logs
└── temp/                    # Temporary files (gitignored)
```

## Development Workflow

### Working with Agents, Skills, and Prompts

#### Agent Files (`*.agent.md`)

Location: `.github/agents/`

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

Location: `.github/` or configured folders

Modular instruction sets that can be combined. Configure via `chat.instructionsFilesLocations` setting.

#### Agent Skills (`skills/*/SKILL.md`)

Location: `.github/skills/<skill-name>/SKILL.md`

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

1. Create `.github/agents/<name>.agent.md` with proper frontmatter
2. Define the agent's purpose, tools, and instructions
3. Test the agent with sample prompts

**For Skills:**

1. Create `.github/skills/<skill-name>/SKILL.md`
2. Add YAML frontmatter with `name` and `description`
3. Write clear instructions and examples
4. Optionally add bundled assets (scripts, templates)

**For Prompts:**

1. Create `.github/prompts/<name>.prompt.md`
2. Add frontmatter with `agent`, `tools`, and `description`
3. Write the prompt template with clear instructions

## Skill Routing

This section is the single source of truth for skill-to-execution mapping. The main prompt should detect that a skill applies, then consult this section instead of embedding the full routing table inline.

| Skill | Trigger Keywords | Execution Mode | Reason |
| :--- | :--- | :--- | :--- |
| `commit-skill` | commit, save changes with git | **Main agent direct (Tier 1)** | Interactive protocol requires user confirmation between steps; subagent cannot pause for I/O |
| `documentation` | write doc, create report, publish | **Delegate → `@doc-writer` (Tier 2)** | Substantive work; specialist subagent produces higher quality output |
| `code-review` | review changes, review before merge | **Delegate → `@code-quality-reviewer` (Tier 2)** | Substantive work; dedicated review subagent |
| `deep-research` | research, investigate (multi-source) | **Delegate → `@research-gpt` / `@research-gemini` / `@research-claude` (Tier 2)** | Substantive work; multi-source research subagents |
| `data-analysis` | analyze results, compare metrics | **Delegate → `search_subagent` (built-in) + main agent (Tier 2)** | Substantive work; exploration + synthesis pattern |
| `skill-extension` | create new skill, new SKILL.md | **Delegate → `@code-generator` (Tier 2)** | Substantive work; structured file generation |
| `external-skill-generation` | import external skill | **Tier 1 gate + Tier 2 delegation** | Security review gates (steps 1, 3, 6) run in main session (Tier 1). Substantive extraction and rewrite (steps 2, 4, 5) delegate to `@code-generator` via `runSubagent`. Main session holds approval authority between phases. |
| `paper-catalog-update` | update prompt paper catalog, run catalog update procedure, improve catalog update procedure | **Delegate → `@prompt-plan-master` (Tier 2)** | Substantive work; maintains the paper catalog and supports prompt planning from curated papers |
| `copilot-eval-benchmark` | benchmark copilot, score customized copilot, swe-bench verified import | **Main agent direct (Tier 1/2 hybrid)** | Local Copilot stack cannot be fully headless; use semi-automated run-sheet + scoring pipeline |
| **Prompt planning (direct agent)** | design prompt, plan prompt, 프롬프트 설계, 프롬프트 전략 | **Delegate → `@prompt-plan-master` (Tier 2)** | Research-grounded prompt planning; returns prompt drafts/rationale for downstream writers |

## Available Agents

Use this table to identify which agent to call for each task type. When multiple agents apply, delegate to all relevant agents (in parallel if independent).

> **Pre-selection**: Read the gate result from `.github/copilot-instructions.md § 0-GATE` first, then use this table to choose the agent. Use `@orchestrator` only for complex multi-step work; do not use it as a universal router.

| Task Type | Agent | Description | Example Triggers |
| :--- | :--- | :--- | :--- |
| **Complex orchestration** | `@orchestrator` | Strategic planner. Returns execution blueprint; main session performs actual subagent calls. Planning-only — never writes code or edits files. **Call FIRST** when: task needs 3+ subagent steps, spans 3+ domains, has dependency ordering, or produces artifacts requiring downstream validation. | "plan this", "multi-phase task", "coordinate agents" |
| **New code / feature implementation** | `@code-generator` | Code generation with best practices and type safety. | "implement X", "add feature Y", "write a function for Z" |
| **Bug / error / failure diagnosis & fix** | `@fixer` | Autonomous problem-solving & execution agent. Diagnoses issues, implements fixes, executes code/tests, and verifies solutions. | "fix this", "error in", "not working", "debug" |
| **Architecture / design planning** | `@architect` | Architecture Planner. Designs system architecture and technical solutions. | "design", "how should I structure", "best approach for" |
| **Code review / quality gate** | `@code-quality-reviewer` | Code Quality Reviewer. Ensures code standards compliance. | "review my code", "is this good?", "check for issues" |
| **Regression / test reliability** | `@qa-regression-sentinel` | Execution-based quality verification, reproduction scripts, and flaky test detection. | "run tests", "check for regressions", "flaky test" |
| **Documentation writing** | `@doc-writer` | Documentation Writer. Creates well-structured documentation from requirements. | "write docs", "document this", "create README" |
| **Documentation review** | `@doc-reviewer` | Documentation Reviewer. Reviews documentation for clarity and completeness. | "review this doc", "check documentation" |
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
| **Research-backed prompt planning** | `@prompt-plan-master` | Generates prompt drafts from the internal paper database and returns planning rationale/citations. It does not author final documents; `@doc-writer` consumes its output to write docs. | "write a prompt for", "which prompting technique", "select prompt technique", "prompt planning", "prompt blueprint", "프롬프트 설계", "프롬프트 전략", "prompt for agent", "prompt template" |

## Available Skills

| Skill | Description | Execution Mode |
| :--- | :--- | :--- |
| `documentation` | Standardized documentation creation and formatting | **Delegate → `@doc-writer`** |
| `code-review` | Code quality checklist and best practices enforcement | **Delegate → `@code-quality-reviewer`** |
| `deep-research` | Recursive research workflow (STORM-style) | **Delegate → `@research-gpt` / `@research-gemini` / `@research-claude`** |
| `data-analysis` | Result visualization and statistical comparison | **Delegate → `search_subagent` (built-in) + main agent** |
| `skill-extension` | Create and extend agent skills | **Delegate → `@code-generator`** |
| `paper-catalog-update` | Monthly update workflow for prompt engineering paper catalog (freshness check, scoring, add/retire, metadata sync) | **Delegate → `@prompt-plan-master`** |
| `external-skill-generation` | Generate skills from external documentation | **Tier 1 gate + Tier 2 delegation** (`@code-generator` for extraction/rewrite phases) |
| `commit-skill` | Commit workflow with diff-based message generation and explicit user confirmation gate before `git commit` | **Main agent direct** (interactive gate) |
| `copilot-eval-benchmark` | Semi-automated scoring workflow for customized local Copilot, including optional SWE-bench Verified task import | **Main agent direct** |

## Adding Custom Agents

To add project-specific agents:

1. Define agent roles and capabilities in this file
2. Create `.github/agents/<name>.agent.md` with proper frontmatter
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

Refer to `documents/PROJECT.md` for project-specific agent configurations and workflows.

## Related Resources

- [Agent Skills Specification](https://agentskills.io/specification) - Official Agent Skills standard
- [GitHub Awesome Copilot](https://github.com/github/awesome-copilot) - Curated Copilot resources
- [VS Code Copilot Customization](https://code.visualstudio.com/docs/copilot/customization/agent-skills) - Official documentation
- [GitHub Copilot Documentation](https://docs.github.com/en/copilot) - Complete Copilot guide
- Project Documentation:
  - [`documents/PROJECT.md`](documents/PROJECT.md) - Project overview and status
  - [`documents/AGENT_MANUAL.md`](documents/AGENT_MANUAL.md) - AI Agent operation manual
  - [`.github/copilot-instructions.md`](.github/copilot-instructions.md) - Development guidelines
