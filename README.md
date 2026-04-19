# Universal Development Template

A standardized template for **any software development project** with **GitHub Copilot** integration and AI-powered workflows.

> **📌 Project-Specific Details**: Add project-specific structure, build instructions, and tech stack documentation under `documents/` as you adapt this template.

## Features

- 🤖 **AI-Optimized**: Pre-configured GitHub Copilot instructions, custom agents, and agent skills
- 📊 **Flexible Structure**: Adaptable to any project type (Web, Game, ML/AI, Modding, etc.)
- 🔄 **Reproducible**: Version control, configuration management, type-safe code practices
- 📝 **Documentation-First**: Structured documentation workflow with templates
- 🧩 **Extensible**: Agent skills for automated workflows and best practices
- 🌐 **Multi-Language**: Support for Korean + English documentation

## Operating Model

This template currently uses a lifecycle-first operating model for non-trivial AI work: `INIT -> ATOMIZE -> PLAN -> EXECUTE -> REPORT -> AWAIT -> FINALIZE`. In practice, the orchestrator coordinates task boundaries and specialist agents handle substantive execution.

## Quick Start

```bash
# Clone your project
git clone <repository-url>
cd <project-directory>

# Install dependencies (adapt to your project)
# Python: uv sync
# Node.js: npm install
# .NET: dotnet restore
# RimWorld Mod: See documents/BUILD_GUIDE.md

# Run your project (adapt to your project)
# Python: uv run python src/main.py
# Node.js: npm start
# .NET: dotnet run
# RimWorld Mod: Copy to mods folder and launch game
```

To register this repository as a local VS Code Copilot plugin on Windows, run `scripts\\install_vscode_plugin.cmd`. The Python entrypoint is `scripts/install_vscode_plugin.py` and updates the VS Code user `settings.json` `chat.pluginLocations` value for this plugin root.

## Project Structure

> **📌 For detailed project structure**: Document the project-specific directory layout under `documents/` as you adapt this template.
>
> **📌 For extending this template**: If [CONTRIBUTING.md](CONTRIBUTING.md) exists, use it to decide which file to edit when adding policies, procedures, or definitions.

This template provides a standardized structure that adapts to any project type:

```text
.
├── .github/                 # Runtime-visible mirrors and instructions
│   ├── instructions/        # Deployed instruction mirrors
│   └── copilot-instructions.md
├── copilot/                 # Runtime-owned Copilot assets
│   ├── agents/              # Custom agents (.agent.md)
│   ├── skills/              # Agent Skills (workflows)
│   ├── hooks.json           # Hook manifest
│   └── mcp.json             # MCP server manifest
├── documents/               # Documentation hub
│   ├── final/               # Published documents
│   ├── drafts/              # Work in progress
│   ├── reference/           # Technical and paper references
│   └── templates/           # Reusable doc templates
├── src/                     # Source code
├── tests/                   # Test files
├── scripts/                 # Automation scripts
└── AGENTS.md                # Agent documentation
```

**Adaptable to**:

- Software development (Web, Desktop, Mobile)
- Research & ML/AI projects
- Game & mod development
- Infrastructure & DevOps

## AI Agents

This template includes pre-configured GitHub Copilot agents for common development tasks:

| Agent | Description |
| :--- | :--- |
| `@orchestrator` | Lifecycle-first coordinator for complex multi-agent workflows |
| `@deep-think-mediator` | Optional mediator for explicit deep-think protocol flows; uses a Gemini-family runtime path only when the host environment provides native Gemini access outside the repo-owned runtime |
| `@dt-council-mediator` | Optional mediator for explicit council protocol flows; uses a Gemini-family runtime path only when the host environment provides native Gemini access outside the repo-owned runtime |
| `@fixer` | Autonomous problem-solving & execution agent |
| `@doc-writer` | Documentation Writer (creates structured docs) |
| `@doc-reviewer` | Documentation Reviewer (quality checks) |
| `@code-generator` | Code generation with best practices |
| `@code-quality-reviewer` | Code quality & standards compliance |
| `@validator` | Verification and validation |
| `@architect` | System architecture & design |
| `@research-gemini` | Implementation-focused research |
| `@research-gpt` | Theory-focused research |
| `@research-claude` | System/Safety-focused research |
| `@planner-*` | Strategic planning (Gemini/GPT/Claude variants) |
| `@idea-generator-*` | Ideation (Gemini/GPT/Claude variants) |

**See [AGENTS.md](AGENTS.md) for full documentation.**

## Agent Skills

Agent Skills are specialized workflows automatically loaded by Copilot:

| Skill | Description |
| :--- | :--- |
| `documentation` | Standardized doc creation and formatting |
| `code-review` | Code quality checklist and best practices |
| `commit-skill` | Commit workflow with explicit confirmation |
| `deep-research` | Recursive research workflow (STORM-style) |
| `deep-think` | Optional mediator-first deep reasoning workflow |
| `data-analysis` | Result visualization and statistical comparison |
| `dt-council` | Optional mediator-first multi-perspective council workflow |
| `lifecycle-runtime-ops` | Verify runtime activation, write lifecycle transitions, and check refresh or cleanup state |
| `skill-extension` | Create and extend agent skills |
| `external-skill-generation` | Generate skills from external documentation |
| `paper-catalog-update` | Refresh the prompt engineering paper catalog |

The baseline path is lifecycle-first orchestration, and mediator or council-style coordination is available as optional explicit overlays rather than the universal default. This repository does not ship a local Gemini MCP backend. If a mediator protocol expects a Gemini-family path, it should use host-provided native Gemini access when available and otherwise return a blocked or degraded result.

**See [AGENTS.md](AGENTS.md) for usage examples.**

## Documentation Workflow

### Document Types

| Type | Location | Purpose |
| :--- | :--- | :--- |
| **Final Reports** | `documents/final/` | Completed, reviewed documents |
| **Drafts** | `documents/drafts/` | Work in progress |
| **Technical Reference** | `documents/reference/technical/` | API docs, guides |
| **Paper Summaries** | `documents/reference/papers/` | Research summaries |
| **Templates** | `documents/templates/` | Standard forms |

### Documentation Guidelines

1. **Write drafts in `documents/drafts/`** - Not ready for publication
2. **Move to `documents/final/`** - After review and approval
3. **Use Memory MCP for notes** - Don't create `*.memory.md` files
4. **Follow project language policy** - See `shared/copilot-instructions.md` (runtime mirror: `.github/copilot-instructions.md`)

## Development Workflow

### Working with Agents

1. **Check [AGENTS.md](AGENTS.md)** - Find the right agent for your task
2. **Invoke agent** - Use `@agent-name` in Copilot chat
3. **Provide context** - Clear requirements and constraints
4. **Review output** - Validate and iterate

### Using Skills

Skills are automatically loaded by Copilot when relevant trigger phrases match a skill definition in `copilot/skills/<name>/SKILL.md`.

Example:

```text
@doc-writer Create a technical guide for feature X.
```

Use `AGENTS.md` and each `SKILL.md` file to confirm the expected trigger conditions and execution mode.

### Memory Management

Use **Memory MCP** (`mcp_memory_*` tools) for transient data:

- Observations/Notes → `mcp_memory_store`
- Prior context lookup → `mcp_memory_search`
- List all memories → `mcp_memory_list`

**DO NOT** create local `*.memory.md` files.

## Project Adaptation Guide

### For Different Project Types

**RimWorld Mod Development**:

- Structure: Add a project-specific guide under `documents/`
- Build: MSBuild, .NET Framework 4.8
- Test: In-game testing with Debug Mode

**ML/AI Research**:

- Add: `configs/`, `results/`, `checkpoints/`
- Tools: PyTorch, TensorFlow, Weights & Biases
- Test: Reproducibility checks, statistical validation

**Web Development**:

- Add: `frontend/`, `backend/`, `api/`, `public/`
- Tools: React, Node.js, Express, Next.js
- Test: Unit tests, integration tests, E2E tests

**Game Development**:

- Add: `assets/`, `scenes/`, `scripts/`, `prefabs/`
- Tools: Unity, Unreal, Godot
- Test: Playtesting, performance profiling

**General Software**:

- Standard structure works out of the box
- Adapt as needed for your tech stack

### Customization Steps

1. **Add project-specific docs under `documents/`** - Capture structure, build, and workflow details for your project
2. **Configure `shared/copilot-instructions.md`** - Set coding standards, then sync `.github/copilot-instructions.md`
3. **Add custom agents** - Create `copilot/agents/<name>.agent.md`
4. **Create skills** - Add `copilot/skills/<name>/SKILL.md`; use `copilot/skills/lifecycle-runtime-ops/SKILL.md` as the runtime-operations reference when adjusting activation, transition, refresh, or cleanup procedures
5. **Update AGENTS.md** - Document your custom agents

## Getting Started

**First-time project setup**:

1. **Read this README** - Understand the template's baseline structure and workflow
2. **Check [AGENTS.md](AGENTS.md)** - Learn about available agents
3. **Review `shared/copilot-instructions.md`** - Understand repository-wide policy and coding rules
4. **Inspect `copilot/agents/` and `copilot/skills/`** - See the active runtime assets in this template
5. **Add project-specific docs under `documents/` as needed** - Capture build, test, and onboarding details for your project

## Documentation

- **[AGENTS.md](AGENTS.md)** - AI agent documentation (must-read!)
- **[shared/copilot-instructions.md](shared/copilot-instructions.md)** - Source-of-truth development guidelines
- **[.github/copilot-instructions.md](.github/copilot-instructions.md)** - Runtime mirror of the development guidelines
- **`documents/`** - Location for project-specific guides, reports, and references

For runtime-owned customization work, check `copilot/skills/lifecycle-runtime-ops/SKILL.md` together with the lifecycle technical references under `documents/reference/technical/`: `runtime-path-contract.md`, `runtime-refresh-runbook.md`, `stale-cleanup-policy.md`, `orchestrator-responsibility-split-map.md`, `lifecycle-validation-guide.md`, plus `lifecycle-state-schema-guide.md` and `lifecycle-acceptance-checklist.md`.

## Reference Repositories

The `references/` directory stores **external code and repositories used as reference** during development.

**Management Principles**:

- ✅ Include: External projects, library examples, prototype code
- ❌ Exclude: Active project code (`src/`), archived versions (`archive/`), documentation (`documents/`)

**Guidelines**:

1. Verify and comply with licenses
2. Document version/date information clearly
3. Reference code is read-only (no direct modifications)
4. Regularly update or remove outdated references

**Use subdirectories under `references/` to organize project-specific external references.**

## Contributing

This is a template project. To use it:

1. Clone or fork this repository
2. Adapt the structure to your project type
3. Add your project-specific guides under `documents/`
4. Customize agents and skills as needed
5. Remove this section and add your project-specific content

## License

[Specify your license]

## Links

- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [Agent Skills Specification](https://agentskills.io/specification)
- [VS Code Copilot Customization](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- [Keep a Changelog](https://keepachangelog.com/)
- [Semantic Versioning](https://semver.org/)

---

**Template Version**: 1.0.1  
**Last Updated**: 2026-04-18
