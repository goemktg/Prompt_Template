# AGENTS.md

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

## Setup Commands

Execution and dependency commands are managed in these files:

- Global command conventions: `.github/copilot-instructions.md`
- Project-specific commands: `documents/PROJECT.md`

This file does not define runnable commands to avoid duplication.

## Template Files Initialization

If `.template.md` files exist in `documents/`, follow these steps:

### Customization Workflow

1. **Review `.template.md` files** in `documents/`:
   - `PROJECT.template.md` - Project overview and status
   - `CHANGELOG.template.md` - Version history
   - `QUICKSTART.template.md` - Quick start guide

2. **Gather project information** (if needed):
   - Prompt user for project-specific details:
     - Project name and description
     - Technology stack and key dependencies
     - Team members and roles (if applicable)
     - Project objectives and scope
     - Any other relevant project context
   - Document this information clearly for use in the next step

3. **Create project-specific files**:
   - Using gathered information, create corresponding `.md` file (without `.template` suffix)
   - Fill in all sections with appropriate project-specific content
   - Tailor documentation to your project's needs and conventions

4. **Clean up template files**:
   - Delete all `.template.md` files after creating their corresponding `.md` files

### Checklist

- [ ] Review all `.template.md` files in `documents/`
- [ ] Gather project-specific information from user input
- [ ] Create `documents/PROJECT.md` from `PROJECT.template.md`
- [ ] Create `documents/QUICKSTART.md` from `QUICKSTART.template.md`
- [ ] Create `documents/CHANGELOG.md` from `CHANGELOG.template.md`
- [ ] Delete all `.template.md` files

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

## Available Agents

Use this table to identify which agent to call for each task type. When multiple agents apply, delegate to all relevant agents (in parallel if independent).

| Task Type | Agent | Description | Example Triggers |
| :--- | :--- | :--- | :--- |
| **Complex orchestration** | `@orchestrator` | Strategic planner. Returns execution blueprint; main session performs actual subagent calls. Planning-only — never writes code or edits files. | "plan this", "multi-phase task", "coordinate agents" |
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
| **Codebase exploration / Q&A** | `@Explore` | Fast read-only codebase exploration and Q&A. | "where is X defined?", "how does Y work?" |

## Available Skills

| Skill | Description |
| :--- | :--- |
| `documentation` | Standardized documentation creation and formatting |
| `code-review` | Code quality checklist and best practices enforcement |
| `deep-research` | Recursive research workflow (STORM-style) |
| `data-analysis` | Result visualization and statistical comparison |
| `skill-extension` | Create and extend agent skills |
| `external-skill-generation` | Generate skills from external documentation |

## Pull Request Guidelines

### Code Review Checklist

For agent files (`*.agent.md`):

- [ ] Has YAML frontmatter
- [ ] Has `name` field (lowercase with hyphens)
- [ ] Has non-empty `description` field in single quotes
- [ ] File name follows pattern `<name>.agent.md`

For skills (`skills/*/SKILL.md`):

- [ ] Folder contains a SKILL.md file
- [ ] SKILL.md has YAML frontmatter
- [ ] Has `name` field matching folder name
- [ ] Has non-empty `description` field (10-1024 characters)
- [ ] Any bundled assets are referenced in SKILL.md

For general code:

- [ ] Type hints on all functions (if applicable)
- [ ] Documentation/comments in project language (Korean/English)
- [ ] Error handling implemented
- [ ] Tests added for new features
- [ ] No hardcoded paths or credentials

### Project-Specific Checklists

**RimWorld Mod Development:**

- [ ] XML patches have `success="Always"` attribute
- [ ] XPath expressions are accurate
- [ ] Mod dependencies declared in About.xml
- [ ] Load order specified in `loadAfter`

**Research/ML Projects:**

- [ ] Random seeds are fixed
- [ ] All hyperparameters in config files
- [ ] No data leakage between train/test splits
- [ ] Model in `.eval()` mode during validation

**Web Development:**

- [ ] API endpoints documented
- [ ] Input validation implemented
- [ ] Security headers configured
- [ ] Rate limiting considered

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
